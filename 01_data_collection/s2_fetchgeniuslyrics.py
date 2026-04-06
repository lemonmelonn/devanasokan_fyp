import os
import pandas as pd
import lyricsgenius
from dotenv import load_dotenv
from tqdm import tqdm

tqdm.pandas()

# Load environment variables from .env
load_dotenv()

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/noexplicit.csv", encoding='utf-8-sig')

print(df.shape)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
genius = lyricsgenius.Genius(
    ACCESS_TOKEN,
    timeout=15, 
    retries=3
)

def get_structured_lyrics(row):
    try:
        # It is MUCH better to search using both Artist and Title
        # to avoid getting the wrong song or a cover version.
        song = genius.search_song(row['clean_track_name'], row['clean_primary_artist'])
        
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
print(df.shape)
df.to_csv('./storage/geniuslyrics.csv', index=False, encoding="utf-8-sig")