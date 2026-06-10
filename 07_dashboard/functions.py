import re
import os
from dotenv import load_dotenv
import lyricsgenius
import contractions
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Load environment variables from .env
load_dotenv()

# Initialize Genius API client
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
genius = lyricsgenius.Genius(
    ACCESS_TOKEN,
    timeout=15, 
    retries=3
)

# Load the model and tokenizer from local folder
def load_model():
    # Load the model and tokenizer from your local folder
    path = "./05_model_training/my_final_model"
    model = AutoModelForSequenceClassification.from_pretrained(path)
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased") # Ensure tokenizer has been saved

    # Create a 'pipeline' (the easiest way to use the model)
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return classifier


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
def split_verses(fullsong):

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
    for _, verse_text in split_song:
        verses.append(verse_text)

    # Save as df
    df = pd.DataFrame({"ori_verse": verses})

    # Format verses into a single line (separated by commas)
    df['verse'] = df['ori_verse'].apply(lambda x: ', '.join(x.splitlines()))

    return df


# Clean the verses by removing unwanted characters, fixing contractions, and normalizing text
def clean_verses(full_song):

    df = split_verses(full_song)

    # Remove lyrics with unkown script
    def contains_unknown_script(text):
        # Check for characters outside the basic Latin and common punctuation
        return bool(re.search(r'[^\x00-\x7F]', text))

    df = df[~df['verse'].apply(contains_unknown_script)]

    # Remove rows where 'lyrics' is NaN after cleaning
    df = df.dropna(subset=["verse"])

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

    # Apply cleaning
    df['lyrics'] = df['verse'].apply(clean_lyrics)

    # Fix words that end with in'
    df['lyrics'] = df['lyrics'].str.replace(
        r"\b(\w+?)in['’]",
        r"\1ing",
        regex=True
    )

    # Handle vocables
    def normalize_vocables(text):
        return re.sub(r'\b(\w{2,})(-\1)+\b', r'\1', text)

    df['lyrics'] = df['lyrics'].apply(normalize_vocables)

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

    df['lyrics'] = df['lyrics'].apply(replace_shortened_words)

    # Lowercase all lyrics
    df['lyrics'] = df['lyrics'].str.lower()

    return df


# Loop verses through the model and print results
def get_model_output(classifier, verses_list):
    for verse in verses_list:
        result = classifier(verse)
        print(f"Input: {verse} -> Prediction: {result}")

# get_model_output(classifier, verses)


# TESTING

classifier = load_model()

artist = "Ariana Grande"
track = "7 rings"

full_song = get_structured_lyrics(artist, track)
print(full_song[:100])

verses = clean_verses(full_song)
for verse in verses["lyrics"]:
    get_model_output(classifier, [verse])
    print("\n---\n")