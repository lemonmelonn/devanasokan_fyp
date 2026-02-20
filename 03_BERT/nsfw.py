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
classifier = pipeline("text-classification", model="keatrean/swearwords-detection-model")

# Another model for stricter detection
# martin-ha/moderate-bert
# Profanity/toxicity: original/bert-base-toxic-comment-classification
# Sexual pattern: michellejieli/NSFW_text_classification

# 3. Load your song data
df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/lyrics_tokens.csv", encoding='utf-8-sig')

def label_verse(text):
        if pd.isna(text) or len(str(text)) < 3:
            return "neutral", 0.0
        
        # Run the model
        result = classifier(str(text))[0]
        
        # result typically looks like: {'label': 'LABEL_1', 'score': 0.98}
        # Note: Check the model's specific labels once it runs to map them (e.g., LABEL_1 = sexual)
        return result['label'], round(result['score'], 4)

# 6. APPLY TO DATASET
print("Labeling verses... this may take a moment.")
# This expands the results into two new columns: 'sexual_label' and 'sexual_score'
df[['sexual_label', 'sexual_score']] = df['tokens'].apply(
    lambda x: pd.Series(label_verse(x))
)

# # 7. Save
df.to_csv('lyrics_sexual_analysis.csv', index=False)
print("Analysis complete! File saved as 'lyrics_sexual_analysis.csv'.")