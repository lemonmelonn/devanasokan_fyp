import os
import lyricsgenius
from dotenv import load_dotenv
from tqdm import tqdm

tqdm.pandas()

# Load environment variables from .env
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
genius = lyricsgenius.Genius(
    ACCESS_TOKEN,
    timeout=15, 
    retries=3
)

def get_structured_lyrics():
    try:
        # It is MUCH better to search using both Artist and Title
        # to avoid getting the wrong song or a cover version.
        song = genius.search_song("Pavazha malli", "Sai Abyankar")
        
        if song:
            return song.lyrics
        else:
            return None
    except Exception as e:
        print(f"Error fetching song: {e}")
        return None
    
print(get_structured_lyrics())

