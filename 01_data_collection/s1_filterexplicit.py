import pandas as pd
import re

df = pd.read_csv("C:/Users/User/Downloads/fypsongs/spotify_dataset.csv")

print(df.shape)
print(df.columns)

# Filter out explicit songs
df = df[df['Explicit'] == "No"]

df.to_csv("./storage/noexplicit.csv", index=False)
