import pandas as pd
import re

# Load dataset
df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/datasource/top-10k-spotify-songs-2025-07-detailed.csv")
print("Initial shape:", df.shape)


# Remove songs that have certain words (in a list) in genre
remove_keywords = ["white noise", "sleep", "native american music", "tamil", "bangla", "turkish"] # can add more languages
for keyword in remove_keywords:
    df = df[~df['artist_genres'].str.contains(keyword, case=False, na=False)]
print("After removing:", df.shape)


# Get clean track and artist names (easier for Genius API)
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

# Remove lyrics columns (Since collection will happen later)
df = df.drop(columns=['lyrics'])

# Split supporting data from essential data?


# Save output
print("Final shape:", df.shape)
df.to_csv("./storage/songlist.csv", index=False)
