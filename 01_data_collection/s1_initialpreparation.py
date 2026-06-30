import pandas as pd
import re

# Load dataset
df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/datasource/top-10k-spotify-songs-2025-07-detailed.csv")
print("Initial shape:", df.shape)

# Remove duplicates track_name and artist_names combos
df = df.drop_duplicates(subset=['track_name', 'artist_names'], keep='first')
print("After removing duplicates:", df.shape)

# Remove genres that are not relevant (no lyrics)
remove_keywords = ['sleep', 'white noise', 'healing hz', 'calming instrumental', 'space music', 'binaural', 'water', 
                   'rain', 'dark ambient', 'color noise', 'environmental', 'sound', 'ambient lo-fi', 'shush', 'neoclassical', 
                   'background music', 'contemporary classical', 'ocean', 'gabber', 'meditation', 'krushfunk', 'dariacore', 
                   'musica de fondo', 'solfeggio product', 'pop violin', 'classical piano', 'asmr', 'georgian polyphony', 
                   'traditional folk', 'protopunk', 'georgian folk', 'french soundtrack', 'compositional ambient', 
                   'ambient house', 'deep euro house', 'israeli folk', 'brazilian ccm', 'renaissance', 'musica infantil', 
                   'hardwave', 'gym phonk', 'ukrainian phonk', 'hardcore', 'hardcore techno', 'background piano', 
                   'traditional blues', 'memphis soul', 'instrumental soul', 'brass band', 'glitch beats', 'world', 
                   'tropical alternativo', 'new tribe', 'psychedelic soul', 'ballet', 'hymns', 'instrumental lullaby', 
                   "preschool children's music", 'piano worship', 'piano cover', 'focus', '528hz', 'electroacoustic', 
                   'cool jazz', 'subliminal product', 'organic house', 'chamber music', 'liminal space', 'impressionism']

for keyword in remove_keywords:
    df = df[~df['artist_genres'].str.contains(keyword, case=False, na=False)]
print("After removing genres:", df.shape)


# Get clean track and artist names (easier for Genius API)
def clean_search_params(track_name, artist_names):
    # Ensure inputs are strings to avoid errors with NaN values
    track_name = str(track_name) if pd.notnull(track_name) else ""
    artist_names = str(artist_names) if pd.notnull(artist_names) else ""
    
    # Clean Artist Names: Take only the first artist
    primary_artist = artist_names.split('|')[0]
    
    # Clean Track Name: Remove extra info in parentheses or brackets
    clean_track = re.split(r' \-| –| —', track_name)[0]
    clean_track = re.sub(r'\(.*?\)|\[.*?\]', '', clean_track).strip()

    # Return as a Series so we can create two columns at once
    return pd.Series([clean_track, primary_artist])

# Apply the function to create 'clean_track_name' and 'clean_primary_artist'
df[['clean_track_name', 'primary_artist']] = df.apply(
    lambda row: clean_search_params(row['track_name'], row['artist_names']), axis=1
)

# List of important columns
main_cols = ['rank', 'track_name', 'clean_track_name', 'artist_names', 'primary_artist', 
             'explicit', 'artist_genres', 'main_genres', 'lyrics']

# Create and save main dataframe
df_main = df[main_cols].copy()
print("Final main shape:", df_main.shape)
df_main.to_csv("./storage/songlist.csv", index=False)

# Create and save supporting dataframe (keep rank)
df_support = df.drop(columns=[col for col in main_cols if col != 'rank'])
print("Final supporting shape:", df_support.shape)
df_support.to_csv("./storage/supportingdata.csv", index=False)


