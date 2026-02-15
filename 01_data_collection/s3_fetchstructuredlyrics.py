import os
import pandas as pd
import lyricsgenius
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/englishsongs.csv", encoding='utf-8-sig')

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
    
df_sample = df.head(10).copy()
df_sample['structured_lyrics'] = df_sample.apply(get_structured_lyrics, axis=1)

# Insert a new column 'token_id' at the first position
df_sample.insert(0, 'song_id', range(1, len(df_sample) + 1))

df = df_sample[['song_id', 'clean_track_name', 'clean_primary_artist', 'artist_names', 'structured_lyrics']]

# Save the new data
df.to_csv('./storage/structured_lyrics.csv', index=False, encoding="utf-8-sig")