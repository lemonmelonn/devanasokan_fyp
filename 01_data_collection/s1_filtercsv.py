import pandas as pd
import re

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/datasource/top-10k-spotify-songs-2025-07-detailed.csv")

print(df.shape)

# Keep necessary columns
columns = ['rank', 'track_name', 'artist_names', 'album_name', 'popularity', 'release_date','explicit', 'lyrics']
df = df[columns]

# Filter out explicit songs
df = df[df['explicit'] == 0]

# Replace all types of newlines (\r\n or \n) with a comma and a space
# regex=True allows us to catch the hidden newline characters
df['lyrics'] = df['lyrics'].str.replace(r'\r\n|\r|\n', ', ', regex=True)

# Remove songs with no lyrics
df.dropna(subset=["lyrics"], inplace=True)

# Replace double commas (including those with spaces between them)
# \s* matches any amount of whitespace
df['lyrics'] = df['lyrics'].str.replace(r',\s*,', ',', regex=True)

def clean_search_params(track_name, artist_names):
    # Ensure inputs are strings to avoid errors with NaN values
    track_name = str(track_name) if pd.notnull(track_name) else ""
    artist_names = str(artist_names) if pd.notnull(artist_names) else ""
    
    # 1. Clean Artist Names: Take only the first artist
    primary_artist = artist_names.split('|')[0]
    
    # 2. Clean Track Name: Remove extra info in parentheses or brackets
    clean_track = re.split(r' \-| –| —', track_name)[0]
    clean_track = re.sub(r'\(.*?\)|\[.*?\]', '', clean_track).strip()

    # # 3. Final Cleanup: Remove trailing punctuation often left behind
    # clean_track = clean_track.strip(string.punctuation + ' ')
    
    # Return as a Series so we can create two columns at once
    return pd.Series([clean_track, primary_artist])

# Apply the function to create 'clean_track_name' and 'clean_primary_artist'
df[['clean_track_name', 'clean_primary_artist']] = df.apply(
    lambda row: clean_search_params(row['track_name'], row['artist_names']), axis=1
)

noexplicit = df

print(noexplicit.shape)

noexplicit.to_csv("./storage/noexplicit.csv", index=False)
