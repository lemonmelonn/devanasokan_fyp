import os
import pandas as pd
import lyricsgenius
from dotenv import load_dotenv
from tqdm import tqdm

tqdm.pandas()

# Load environment variables from .env
load_dotenv()

# Load dataset
df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/englishsongs.csv", encoding='utf-8-sig')
# print("\nInitial shape:", df.shape, "\n")
print("\nInitial shape: (6679,11)\n")

# Initialize Genius API client
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
genius = lyricsgenius.Genius(
    ACCESS_TOKEN,
    timeout=15, 
    retries=3
)

# Function to fetch lyrics for a given track and artist
def get_structured_lyrics(row):
    try:
        # Search using both track name and artist name to avoid getting the wrong song or a cover version.
        song = genius.search_song(row['clean_track_name'], row['primary_artist'])
        
        if song:
            return song.lyrics
        else:
            return None
    except Exception as e:
        print(f"Error fetching {row['clean_track_name']}: {e}")
        return None
    
df['genius_lyrics'] = df.progress_apply(get_structured_lyrics, axis=1)

# Insert a new column 'song_id' at the first position
df.insert(0, 'song_id', range(1, len(df) + 1))

# Save output
print("Final shape:", df.shape)
df.to_csv('./storage/geniuslyrics.csv', index=False, encoding="utf-8-sig")
