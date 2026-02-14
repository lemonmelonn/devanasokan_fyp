import pandas as pd
import re

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/songs_with_structure.csv", encoding='utf-8-sig')

print(df.shape)

# Split lyrics into different sentences
def tokenize_lyrics(text):
    if not isinstance(text, str):
        return []
    
    # \w matches any alphanumeric character (English and Korean)
    # - matches the hyphen/dash
    # This keeps "yeah-yeah" as one token and preserves Korean words
    tokens = re.split(r'(\[.*?\])', text)
    clean_tokens = [item.strip() for item in tokens if item.strip() and not (item.strip().startswith('[') and item.strip().endswith(']'))]
    print(clean_tokens)
    return clean_tokens

# 1. Create a list of tokens for each song
df['tokens'] = df['structured_lyrics'].apply(tokenize_lyrics)

tokens_df = df[['token_id', 'tokens']].explode('tokens')

tokens_df.to_csv('lyrics_tokens.csv', index=False)