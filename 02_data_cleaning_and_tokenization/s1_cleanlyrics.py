import pandas as pd
import re
import contractions
import unicodedata

### Issues to clean
# foreign scripts
# Special symbols
# Dashes between words


df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/englishsongs.csv", encoding='utf-8-sig')

print(df.shape)

# Change all words to lower-case
df["lyrics"] = df["lyrics"].str.lower()


# Handle brackets and ad-libs
def clean_lyrics(text):

    # Remove contents with squared brackets
    text = re.sub(r'\[.*?\]', '', text)

    # Remove '(' and ')' characters but keep the text between them
    text = re.sub(r'[()]', '', text)

    # Expand contractions
    contractions.fix(text)

    # Handle trailing apostrophes in colloquial words
    text = re.sub(r"(\w+)'", r"\1", text)

    # 4. Final Cleanup: Fix whitespace
    # We collapse multiple spaces into one, but we DO NOT touch the dashes (hyphens).
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
    

df["lyrics"] = df["lyrics"].apply(clean_lyrics)

# Save as csv
print(f"Saving dataframe size {df.shape} to csv")
df.to_csv("./storage/cleanedlyrics.csv", index=False)