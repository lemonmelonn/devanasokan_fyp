import pandas as pd
from langdetect import detect

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/noexplicit.csv")

print(df.shape)

def detect_lang(text):
    try:
        return detect(text)
    except:
        return "unknown"
    
print("dfgh")
df["language"] = df["lyrics"].apply(detect_lang)
print("dfgh")


# Filter english songs
eng_df = df[df["language"] == "en"]
print(f"Saving dataframe size {eng_df.shape} to csv")
eng_df.to_csv("./storage/englishsongs.csv", index=False, encoding="utf-8-sig")

# Filter non-english songs
noeng_df = df[df["language"] != "en"]
print(f"Saving dataframe size {noeng_df.shape} to csv")
noeng_df.to_csv("./storage/nonenglishsongs.csv", index=False, encoding="utf-8-sig")
