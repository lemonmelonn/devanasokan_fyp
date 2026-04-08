import pandas as pd
import spacy
from tqdm import tqdm

# Load dataset
df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/cleanverses.csv", encoding='utf-8-sig')
print("Initial shape:", df.shape)

# Tokenization
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

# Ensure 'total' is set so the progress bar knows the limit
df['tokens'] = [
    [token.text for token in doc] 
    for doc in tqdm(
        nlp.pipe(df['lyrics']), 
        total=len(df), 
        desc="Tokenizing Lyrics"
    )
]

# Remove stopwords
df['tokens'] = df['tokens'].apply(lambda tokens: [token for token in tokens if token.lower() not in nlp.Defaults.stop_words])

# Save output
print("After tokenizing:", df.shape)
df.to_csv('./storage/tokenverses.csv', index=False, encoding='utf-8-sig')