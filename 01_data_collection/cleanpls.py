import pandas as pd

# 1. Load the data (using low_memory=False to stop the warning)
file_path = "C:/Users/User/Documents/devanasokan_fyp/storage/geniuslyrics.csv"
df = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False)

print(f"Original shape: {df.shape}")
print(df.columns)

# Check for types of values in 'language' column
print(df['language'].unique())

print(f"Cleaned shape: {df.shape}")
df.to_csv('./storage/geniuslyricsnew.csv', index=False, encoding="utf-8-sig")
