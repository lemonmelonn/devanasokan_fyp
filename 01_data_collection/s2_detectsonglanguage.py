import pandas as pd
from transformers import pipeline
from tqdm import tqdm

tqdm.pandas()

# Load dataset
df = pd.read_csv("./storage/songlist.csv")
print("Initial shape:", df.shape)


# Load model
lang_detector = pipeline("text-classification", 
                         model="papluca/xlm-roberta-base-language-detection")

# Function to detect language and confidence
def detect_language(text):
    try:
        if not isinstance(text, str) or text.strip() == "":
            return "unknown", 0.0
        
        result = lang_detector(text[:512])  # truncate long text
        label = result[0]['label']
        score = result[0]['score']
        
        return label, score
    
    except:
        return "unknown", 0.0

# Detect language of lyrics
df[['language', 'confidence']] = df['lyrics'].progress_apply(
    lambda x: pd.Series(detect_language(x))
)


# Filter english songs
# Keep unknown as well, for missing lyrics
eng_df = df[(df["language"] == "en") | (df["language"] == "unknown") | (df["confidence"] <= 0.7)]
print(f"Saving dataframe size {eng_df.shape} to csv")
eng_df.to_csv("./storage/englishsongs.csv", index=False, encoding="utf-8-sig")

# Filter non-english songs
noeng_df = df[~df.index.isin(eng_df.index)]
print(f"Saving dataframe size {noeng_df.shape} to csv")
noeng_df.to_csv("./storage/nonenglishsongs.csv", index=False, encoding="utf-8-sig")

