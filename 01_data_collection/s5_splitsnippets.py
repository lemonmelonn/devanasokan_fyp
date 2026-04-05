import pandas as pd
import re

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/clean_lyrics.csv", encoding='utf-8-sig')

print(df.shape)
print(df.columns)

# CREATE DATAFRAME FOR FULL SONG ------------------------------------------------------------
fulldf = df

def combine_lines_with_commas(text):
    if not isinstance(text, str):
        return ""

    # Split into lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Join with commas
    combined = ", ".join(lines)

    # Clean up spacing and duplicate commas
    combined = re.sub(r",\s*,+", ", ", combined)
    combined = re.sub(r"\s+", " ", combined).strip()

    return combined

fulldf['lyrics_flat'] = fulldf['lyrics'].apply(combine_lines_with_commas)
fulldf = fulldf.drop(columns=['lyrics'])

# Save output
print(fulldf.shape)
fulldf.to_csv('./storage/structured_fullsongs.csv', index=False, encoding='utf-8-sig')

# CREATE DATAFRAME FOR VERSES ------------------------------------------------------------

# Split lyrics into different verses and choruses
def split_lyrics(text):
    if not isinstance(text, str) or text.strip() == "":
        return []

    # Split by verse boundaries (double newlines)
    chunks = re.split(r"\n\s*\n", text)

    clean_tokens = []

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        # Remove extra spaces
        chunk = re.sub(r"\s+", " ", chunk)

        # Remove trailing commas
        chunk = re.sub(r",\s*$", "", chunk)

        clean_tokens.append(chunk)

    return clean_tokens

# Create a list of verses for each song
df['verses'] = df['lyrics'].apply(split_lyrics)
verse_df = df[['song_id', 'rank', 'track_name', 'track_id', 'artist_names',
       'artist_ids', 'album_name', 'album_id', 'popularity', 'duration',
       'explicit', 'release_date', 'album_type', 'isrc', 'copies',
       'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
       'duration_ms', 'time_signature', 'total_artist_followers',
       'avg_artist_popularity', 'artist_genres', 'main_genres',
       'clean_track_name', 'clean_primary_artist', 'language', 'verses']].explode('verses')


# Remove verses that are exactly the same
verse_df = verse_df.drop_duplicates('verses')

# Insert a new column 'verse_id' at the first position
verse_df.insert(0, 'verse_id', range(1, len(verse_df) + 1))

# Save output
print(verse_df.shape)
verse_df.to_csv('./storage/structured_verses.csv', index=False, encoding='utf-8-sig')