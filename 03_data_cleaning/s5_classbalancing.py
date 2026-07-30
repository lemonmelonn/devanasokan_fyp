import pandas as pd

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/preparation/finalverses.csv")

print("Before class balancing:", df.shape)

# Balance the dataset by undersampling the majority class
df_majority = df[df['label'] == 0]
df_minority = df[df['label'] == 1]
df_majority_downsampled = df_majority.sample(n=len(df_minority), random_state=42)
df = pd.concat([df_majority_downsampled, df_minority])

# Save output
print("After class balancing:", df.shape)
df.to_csv('C:/Users/User/Documents/devanasokan_fyp/modeldata/balanceddata.csv', index=False, encoding='utf-8-sig')




