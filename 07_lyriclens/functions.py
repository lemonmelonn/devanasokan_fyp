# functions.py
from ast import With
import re
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import lyricsgenius
import contractions
from transformers import AutoTokenizer, pipeline
import onnxruntime as ort

# from spotify_functions import get_song_details

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
        framework="pt"
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
        # Search for the song using the Genius API
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

    records = []
    verse_id = 1
    for section_name, verse_text in split_song:
        records.append(
            {
                "song_id": str(song_id),
                "verse_id": str(verse_id),
                "section": section_name,
                "ori_verse": verse_text,
                "clean_verse": "",
                "label": "",
                "score": "",
            }
        )
        verse_id += 1
        print(f"Verse: {verse_text[:30]}...\n")

    return records


# Clean the verses by removing unwanted characters, fixing contractions, and normalizing text
def clean_verses(verse_records):
    if not verse_records:
        return []

    print(f"Number of verses to clean: {len(verse_records)}")

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

    for verse_row in verse_records:
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

        verse_row["clean_verse"] = cleaned_text
        cleaned_verses.append(cleaned_text)

    return verse_records


# Get model output for each verse and assign labels
def get_model_output(classifier, verse_records):
    label_list = []
    
    # Initialize tokenizer for the BERT model
    tokenizer = AutoTokenizer.from_pretrained("devanasokan/bert-lyrics-classifier")
    MAX_TOKENS = 512
    STRIDE = 256  # Overlap between chunks
    
    def predict_with_sliding_window(text, classifier, tokenizer, max_tokens=512, stride=256):
        """
        Split long text into overlapping chunks and aggregate predictions.
        Returns the aggregated label and confidence score.
        """
        # Tokenize the full text
        tokens = tokenizer.encode(text, add_special_tokens=False)
        
        # If text fits in one chunk, predict directly
        if len(tokens) <= max_tokens:
            result = classifier(text)
            return result[0]["label"], result[0]["score"]
        
        print(f"Long verse detected: {len(tokens)} tokens (max: {max_tokens}). Using sliding window...")
        
        # Split into overlapping chunks
        chunk_predictions = []
        
        for i in range(0, len(tokens), stride):
            chunk_tokens = tokens[i:i + max_tokens]
            
            # Skip very small chunks at the end
            if len(chunk_tokens) < 50:
                continue
            
            # Decode chunk back to text
            chunk_text = tokenizer.decode(chunk_tokens)
            
            print(f"  Processing chunk {len(chunk_predictions) + 1}: {len(chunk_tokens)} tokens")
            
            try:
                result = classifier(chunk_text)
                chunk_predictions.append({
                    "label": result[0]["label"],
                    "score": result[0]["score"]
                })
            except Exception as e:
                print(f"  Error processing chunk: {e}")
                continue
        
        if not chunk_predictions:
            # Fallback: truncate to max length
            print(f"  Failed to process chunks. Truncating to {max_tokens} tokens...")
            truncated_tokens = tokens[:max_tokens]
            truncated_text = tokenizer.decode(truncated_tokens)
            result = classifier(truncated_text)
            return result[0]["label"], result[0]["score"]
        
        # Aggregate predictions using voting
        # Count LABEL_1 (UNSAFE) vs LABEL_0 (SAFE)
        unsafe_count = sum(1 for p in chunk_predictions if p["label"] == "LABEL_1")
        safe_count = len(chunk_predictions) - unsafe_count
        
        # Determine aggregated label (majority vote)
        aggregated_label = "LABEL_1" if unsafe_count > 0 else "LABEL_0"
        
        # Average confidence score across chunks
        aggregated_score = sum(p["score"] for p in chunk_predictions) / len(chunk_predictions)
        
        print(f"  Aggregated: {safe_count} SAFE, {unsafe_count} UNSAFE → {aggregated_label} (confidence: {aggregated_score:.4f})")
        
        return aggregated_label, aggregated_score

    # Loop through each verse and get model output
    for row in verse_records:
        verse = (row.get("clean_verse") or "").strip()
        if not verse:
            row["label"] = ""
            row["score"] = ""
            continue

        try:
            # Get prediction from the model (with sliding window for long verses)
            label, score = predict_with_sliding_window(verse, classifier, tokenizer, MAX_TOKENS, STRIDE)

            # Map model labels to human-readable labels
            if label == "LABEL_0":
                label = "SAFE"
            elif label == "LABEL_1":
                label = "UNSAFE"
            else:
                label = "UNKNOWN"

            row["label"] = label
            row["score"] = float(score)
            label_list.append(label)
            
        except Exception as e:
            print(f"Error predicting verse: {e}")
            row["label"] = "ERROR"
            row["score"] = ""

    print(f"Labels assigned: {label_list}")

    # Determine overall song label based on individual verse labels
    ovr_label = "UNSAFE" if "UNSAFE" in label_list else "SAFE"
    return verse_records, ovr_label