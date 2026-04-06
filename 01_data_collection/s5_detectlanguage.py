import pandas as pd
from transformers import pipeline
from tqdm import tqdm

tqdm.pandas()

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/cleanverses.csv")

print(df.shape)

# Load model
lang_detector = pipeline("text-classification", 
                         model="papluca/xlm-roberta-base-language-detection")

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
    

# df['language'] = df['lyrics'].progress_apply(detect_language)
df[['language', 'confidence']] = df['lyrics'].progress_apply(
    lambda x: pd.Series(detect_language(x))
)


# Filter english songs
eng_df = df[df["language"] == "en"]
print(f"Saving dataframe size {eng_df.shape} to csv")
eng_df.to_csv("./storage/englishverses.csv", index=False, encoding="utf-8-sig")

# Filter non-english songs
noeng_df = df[df["language"] != "en"]
print(f"Saving dataframe size {noeng_df.shape} to csv")
noeng_df.to_csv("./storage/nonenglishverses.csv", index=False, encoding="utf-8-sig")
