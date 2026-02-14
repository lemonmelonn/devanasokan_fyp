import pandas as pd

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/nonenglishsongs.csv")

print(df.shape)

unique_counts = df['language'].value_counts()

print("--- UNIQUE VALUES AND COUNTS ---")
print(unique_counts)