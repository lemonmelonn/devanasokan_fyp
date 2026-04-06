import pandas as pd
from langdetect import detect
from tqdm import tqdm

tqdm.pandas()

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/verses.csv")

print(df.shape)

# Need to find a better way to detect language
def detect_lang(text):
    try:
        return detect(text)
    except:
        return "unknown"
    
df["language"] = df["verses"].progress_apply(detect_lang)

# Filter english songs
eng_df = df[df["language"] == "en"]
print(f"Saving dataframe size {eng_df.shape} to csv")
eng_df.to_csv("./storage/englishverses.csv", index=False, encoding="utf-8-sig")

# Filter non-english songs
noeng_df = df[df["language"] != "en"]
print(f"Saving dataframe size {noeng_df.shape} to csv")
noeng_df.to_csv("./storage/nonenglishverses.csv", index=False, encoding="utf-8-sig")
