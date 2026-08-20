from ast import With
import re
import os
import pandas as pd
from dotenv import load_dotenv
import lyricsgenius
import contractions
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import ollama

from csv_functions import add_verses, update_clean_verse, update_song_info, update_verse_label_score
from spotify_functions import get_song_details

# Load environment variables from .env
load_dotenv()

# Initialize Genius API client
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
genius = lyricsgenius.Genius(
    ACCESS_TOKEN,
    timeout=15, 
    retries=3
)

# Load the model from Hugging Face Hub using the pipeline API
def load_model_from_hf():
    classifier = pipeline(
        "text-classification",
        model="devanasokan/bert-lyrics-classifier",
    )
    print("Trained BERT model loaded from Hugging Face Hub.")
    return classifier

# Function to detect if a song is explicit based on Spotify metadata
def detect_explicit(songdetails):
    if songdetails is None:
        print("No song details provided.")
        return None
    
    if explicit := songdetails.get("explicit"):
        print(f"Explicit: {explicit}")
        return True
    else:
        print(f"Explicit: {explicit}")
        return False

# Function to fetch lyrics for a given track and artist
def get_structured_lyrics(artist, track):
    try:
        # Search using both track name and artist name to avoid getting the wrong song or a cover version.
        song = genius.search_song(track, artist)

        if song:
            return song.lyrics
        else:
            return None
    except Exception as e:
        print(f"Error fetching {track} by {artist}: {e}")
        return None
    

# Split lyrics into verses based on [Section ...] markers
def split_verses(song_id, fullsong):

    # Fix brackets that span multiple lines
    def fix_multiline_brackets(text):
        if not isinstance(text, str):
            return text
        
        # Replace newlines inside square brackets with spaces
        fixed_text = re.sub(
            r'\[(.*?)\]',
            lambda match: '[' + re.sub(r'\s*\n\s*', ' ', match.group(1)).strip() + ']',
            text,
            flags=re.DOTALL
        )
        
        return fixed_text
    
    fixed_song = fix_multiline_brackets(fullsong)

    # Function to split lyrics into verses
    def split_lyrics_sections(lyrics):
        if not isinstance(lyrics, str):
            return []
        
        # Split based on [Section ...]
        parts = re.split(r'\[(.*?)\]', lyrics)
        
        sections = []
        
        # parts structure: [text_before, label1, text1, label2, text2, ...]
        for i in range(1, len(parts), 2):
            section_name = parts[i]
            section_text = parts[i+1].strip()
            
            if section_text:  # avoid empty sections
                sections.append((section_name, section_text))
        
        return sections
    
    split_song = split_lyrics_sections(fixed_song)

    verses = []
    verse_id = 1
    for _, verse_text in split_song:
        verses.append(verse_text)
        add_verses(song_id, verse_id, _, verse_text, "verselabels.csv")
        verse_id += 1
        print(f"Verse: {verse_text[:30]}...\n")  # Print the first 30 characters of each verse for verification

    # Save as df
    df = pd.DataFrame({"ori_verse": verses})

    # Format verses into a single line (separated by commas)
    df['verse'] = df['ori_verse'].apply(lambda x: ', '.join(x.splitlines()))

    # Check if only one verse exists
    # If yes, split them into multiple verses after 8 lines
    if len(df) == 1:
        single_verse = df.iloc[0]['verse']
        lines = single_verse.splitlines()
        if len(lines) > 8:
            # Split into multiple verses of 8 lines each
            split_verses = [lines[i:i + 8] for i in range(0, len(lines), 8)]
            df = pd.DataFrame({"verse": ['\n'.join(v) for v in split_verses]})
            print(f"Split single verse into {len(split_verses)} verses.")
        else:
            print("Single verse has 8 or fewer lines; no splitting needed.")

    return df


# Clean the verses by removing unwanted characters, fixing contractions, and normalizing text
def clean_verses(song_id):

    # Read from verselabels.csv
    df = pd.read_csv("verselabels.csv", dtype={"song_id": "str"}, keep_default_na=False)
    song_df = df[df["song_id"] == str(song_id)]
    print(f"Number of verses for Song ID {song_id}: {len(song_df)}")

    if "clean_verse" in song_df.columns:
        uncleaned_verse = song_df[
            song_df["clean_verse"].isna() |
            (song_df["clean_verse"].astype(str).str.strip() == "")
        ]
    else:
        uncleaned_verse = song_df

    print(f"Number of uncleaned verses for Song ID {song_id}: {len(uncleaned_verse)}")

    cleaned_verses = []

    # Remove lyrics with unkown script
    def contains_unknown_script(text):
        # Check for characters outside the basic Latin and common punctuation
        return bool(re.search(r'[^\x00-\x7F]', text))


    # Clean lyrics function
    def clean_lyrics(text):
        if not isinstance(text, str):
            return ""

        # Normalize apostrophes
        text = text.replace("’", "'")

        # Convert adlibs: (adlib) → , adlib,
        text = re.sub(r"\s*\((.*?)\)", r", \1,", text)

        # Fix merged words
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

        # Apply contractions (easier for model training)
        try:
            text = contractions.fix(text)
        except:
            pass

        # Remove double commas
        text = re.sub(r",\s*,+", ", ", text)

        # Clean spaces around commas
        text = re.sub(r"\s+,", ",", text)
        text = re.sub(r",\s+", ", ", text)

        # Remove commas at the start of lines
        text = re.sub(r"^\s*,", "", text, flags=re.MULTILINE)

        # Remove double commas that are side by side
        text = re.sub(r",\s*,", ", ", text)

        # Remove trailing commas in each line
        text = re.sub(r",\s*$", "", text, flags=re.MULTILINE)

        return text.strip()

    # Handle vocables
    def normalize_vocables(text):
        return re.sub(r'\b(\w{2,})(-\1)+\b', r'\1', text)

    # Handle shortened words using mapping
    shortened_mapping = {
        "'til": "until",
        "til'": "until",
        "'Til": "Until",
        "'Till": "Until",
        "tryna": "trying to",
        "Tryna": "Trying to",
        "whatchu": "what you",
        "Whatchu": "What you",
        "wit'": "with",
        "fuckin ": "fucking",
        "'bout": "about",
        "'cause": "because",
        "B4": "Before",
        "'em": "them",
        " ya": " you"
    }

    def replace_shortened_words(text):
        for short, full in shortened_mapping.items():
            text = text.replace(short, full)
        return text

    for _, verse_row in uncleaned_verse.iterrows():
        verse_id = verse_row.get("verse_id")
        text = verse_row.get("ori_verse", "")
        print(f"Original verse: {str(text)[:30]}...")

        if contains_unknown_script(str(text)):
            print(f"Verse contains unknown script, skipping cleaning: {str(text)[:30]}...")
            cleaned_text = str(text)
        else:
            cleaned_text = clean_lyrics(str(text))

            # Fix words that end with in'
            cleaned_text = re.sub(
                r"\b(\w+?)in['’](?=\W|$)",
                r"\1ing",
                cleaned_text
            )

            cleaned_text = normalize_vocables(cleaned_text)
            cleaned_text = replace_shortened_words(cleaned_text)
            cleaned_text = cleaned_text.lower()

            # Remove line breaks
            cleaned_text = cleaned_text.strip().replace("\n", " ")

        if verse_id is not None:
            update_clean_verse(song_id, verse_id, cleaned_text, "verselabels.csv")

        cleaned_verses.append(cleaned_text)

    return "\n\n".join(cleaned_verses)


# Loop verses through the model and print results
# def get_model_output(classifier, verses_list):
#     print(f"Number of verses: {len(verses_list)}")
#     verses = []
#     labels = []
#     scores = []
#     for verse in verses_list:
#         result = classifier(verse)
#         verses.append(verse)
#         labels.append(result[0]["label"])
#         scores.append(result[0]["score"])

#     # Save as df
#     # Only saving the last record, must find out why
#     df = pd.DataFrame({"ori_verse": verses, "label": labels, "score": scores})
#     df.to_csv("model_output.csv", index=False)


def get_model_output(classifier, song_id, CSV_FILE):

    # 1. Load CSV
    df = pd.read_csv(CSV_FILE, dtype={"song_id": str, "verse_id": str, "label": str}, keep_default_na=False)
    df["score"] = pd.to_numeric(df["score"], errors="coerce")

    # 2. Filter song by song_id
    song_df = df[df["song_id"] == str(song_id)].copy()

    print(f"Number of verses: {len(song_df)}")

    label_list = []
    # 3. Loop through each verse in that song
    for idx, row in song_df.iterrows():

        verse = row["clean_verse"]

        # skip empty / uncleaned verses
        if pd.isna(verse) or verse.strip() == "":
            continue

        result = classifier(verse)

        # Get label and map to "SAFE" or "UNSAFE"
        label = result[0]["label"]
        if label == "LABEL_0":
            label = "SAFE"
        elif label == "LABEL_1":
            label = "UNSAFE"
        else:
            label = "UNKNOWN"
        # Append label to list for later use
        label_list.append(label)

        # Get the score
        score = result[0]["score"]

        verse_id = row["verse_id"]

        # 4. Update original dataframe using BOTH keys
        df.loc[
            (df["song_id"] == str(song_id)) &
            (df["verse_id"] == verse_id),
            ["label", "score"]
        ] = [label, score]

    # 5. Save once at the end (important)
    df.to_csv(CSV_FILE, index=False)

    # Get overall label for the song
    if "UNSAFE" in label_list:
        ovr_label = "UNSAFE"
    else:
        ovr_label = "SAFE"

    print("Update complete")
    return ovr_label

# LLM prompt for explicit songs
def create_prompt_explicit(lyrics):
    prompt = f"""
    You are a helpful assistant that explains why a song is classified as explicit based on its lyrics. 
    The song lyrics are delimited by triple quotes below. 
    Please provide a concise explanation of which specific words, phrases, or themes in the lyrics contribute to the explicit classification. 
    Focus on identifying content that may be considered inappropriate for younger audiences, such as profanity, sexual content, violence, or drug references.

    Lyrics:
    \"\"\"
    {lyrics}
    \"\"\"

    Explanation:
    """
    return prompt

# LLM prompt for non-explicit songs
def create_prompt_nonexplicit(lyrics):
    prompt = f"""
    You are a helpful assistant that explains why a song is classified as non-explicit based on its lyrics. 
    The song lyrics are delimited by triple quotes below. 
    Please provide a concise explanation of why the lyrics do not contain content that would be considered explicit. 
    Focus on identifying the absence of profanity, sexual content, violence, or drug references, and highlight any themes or language that contribute to the song being suitable for younger audiences.

    Lyrics:
    \"\"\"
    {lyrics}
    \"\"\"

    Explanation:
    """
    return prompt

# Get overall explanation from LLM
def get_llm_explanation(song_id, CSV_FILE):

    # Get song lyrics from csv file using song_id
    df = pd.read_csv(CSV_FILE, dtype={"song_id": str}, keep_default_na=False)
    song_row = df[df["song_id"] == str(song_id)].iloc[0]
    llm_info = song_row.get("llm_info", "")

    # Check if lyrics exist
    if pd.isna(llm_info) or llm_info.strip() == "":
        if CSV_FILE == "songinfo.csv":
            lyrics = song_row.get("lyrics", "")
            prompt = create_prompt_explicit(lyrics)
            response = ollama.chat(
                model="llama3",   # change if needed
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            llm_info = response["message"]["content"].strip()
        else:
            prompt = create_prompt_nonexplicit(lyrics)
        
        # Save explanation to csv
        # update_song_info(song_id, llm_info, CSV_FILE)

        # Return explanation and save to csv
        return llm_info
        
    else:
        # Return existing explanation from csv
        return llm_info
