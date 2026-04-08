import pandas as pd
import re

# Load dataset
df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/englishverses.csv", encoding='utf-8-sig')
print("Initial shape:", df.shape)

# Tokenization
import spacy
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

# Efficient batch processing
df['tokens'] = [ [token.text for token in doc] 
                         for doc in nlp.pipe(df['lyrics'], batch_size=1000)]

# Save output
print("After cleaning:", df.shape)
df.to_csv('lyrics_tokens.csv', index=False)