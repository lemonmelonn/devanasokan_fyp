import pandas as pd
import re

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/structured_lyrics.csv", encoding='utf-8-sig')

print(df.shape)

# Split lyrics into different verses and choruses
def tokenize_lyrics(text):
    if not isinstance(text, str):
        return []
    
    tokens = re.split(r'(\[.*?\])', text)
    clean_tokens = [item.strip() for item in tokens if item.strip() and not (item.strip().startswith('[') and item.strip().endswith(']'))]
    print(clean_tokens)
    return clean_tokens

# Create a list of tokens for each song
df['tokens'] = df['structured_lyrics'].apply(tokenize_lyrics)

tokens_df = df[['song_id', 'tokens']].explode('tokens')

# Insert a new column 'token_id' at the first position
tokens_df.insert(0, 'token_id', range(1, len(tokens_df) + 1))

tokens_df.to_csv('./storage/lyrics_tokens.csv', index=False, encoding='utf-8-sig')