import pandas as pd

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/02_LLMLabelling/labeled_songs.csv")

print(df.shape)

unique_counts = df['label'].value_counts()

print("--- UNIQUE VALUES AND COUNTS ---")
print(unique_counts)