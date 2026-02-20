import os

# 1. Point the script to your new folder
# Ensure HF_HOME is set before importing Hugging Face libraries so the
# hub uses this folder for downloads/caching instead of the default user cache.
os.environ['HF_HOME'] = os.path.join(os.getcwd(), 'my_bert_models')
os.makedirs(os.environ['HF_HOME'], exist_ok=True)

import pandas as pd
from transformers import pipeline

# 2. Load the Pre-trained Zero-Shot Classifier
# The first time you run this, it will show a progress bar for the download
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Another model for stricter detection
# martin-ha/moderate-bert
# Profanity/toxicity: original/bert-base-toxic-comment-classification
# Sexual pattern: michellejieli/NSFW_text_classification

# 3. Load your song data
df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/lyrics_tokens.csv", encoding='utf-8-sig')

# 4. Define your labels
# These are the categories BERT will try to fit your lyrics into
candidate_labels = ["young children", "adults"]

# 5. Define the labeling function
def label_verse(text):
    # This helps BERT 'think' by giving it a sentence to complete
    hypothesis = "The target audience for this song verse is {}."
    result = classifier(text, candidate_labels, hypothesis_template=hypothesis)
    
    # result['labels'][0] is the label with the highest probability score
    return result['labels'][0]

# 6. Run the labeling
print(f"Starting to label {len(df)} verses. Please stay patient...")
df['label'] = df['tokens'].apply(label_verse)

# 7. Save your results
df.to_csv('labeled_lyrics_output.csv', index=False)
print("Success! Open 'labeled_lyrics_output.csv' to see the results.")