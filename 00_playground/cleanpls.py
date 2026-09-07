import pandas as pd

# 1. Load the data (using low_memory=False to stop the warning)
file_path = "C:/Users/User/Documents/devanasokan_fyp/storage/splitverses.csv"
df = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False)

print(f"Original shape: {df.shape}")
print(df.columns)

remove_keywords = ["tamil pop", "chinese", "indonesian pop", "hindi"]

for keyword in remove_keywords:
    df = df[~df['artist_genres'].str.contains(keyword, case=False, na=False)]


print(f"Cleaned shape: {df.shape}")
df.to_csv('./storage/splitversesnew.csv', index=False, encoding="utf-8-sig")
