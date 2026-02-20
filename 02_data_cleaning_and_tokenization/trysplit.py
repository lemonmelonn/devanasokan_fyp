import pandas as pd
import re

# TO DO

# Keep only one copy of chorus (the longest one?)
# Settle mixed formats for apostrophies (straight and curly)
# Remove byte order and unicode

# Repeating lyrics, some have extra brackets, but still same words
# Some lyrics are same but got extra abit at the end, how to handle (ex: Die with a smile line 4 and 7)
# HOW TO HANDLE ADLIBS IN BRACKETS???
# Add comma between lines in a verse (DONE)

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/structured_lyrics.csv", encoding='utf-8-sig')

print(df.shape)

# Split lyrics into different verses and choruses
def split_lyrics(text):
    if not isinstance(text, str):
        return []
    
    tokens = re.split(r'(\[.*?\])', text)
    clean_tokens = [item.strip() for item in tokens if item.strip() and not (item.strip().startswith('[') and item.strip().endswith(']'))]
    return clean_tokens

# Create a list of verses for each song
df['verses'] = df['structured_lyrics'].apply(split_lyrics)
verse_df = df[['song_id', 'verses']].explode('verses')

# Change all words to lower-case
verse_df["verses"] = verse_df["verses"].str.lower()

verse_df['verses'] = verse_df['verses'].apply(
    lambda x: ", ".join([line.strip() for line in x.splitlines() if line.strip()])
)

# Remove verses that are exactly the same
verse_df = verse_df.drop_duplicates('verses')

# Insert a new column 'verse_id' at the first position
verse_df.insert(0, 'verse_id', range(1, len(verse_df) + 1))

print(verse_df.shape)

verse_df.to_csv('./storage/lyrics_verses.csv', index=False, encoding='utf-8-sig')