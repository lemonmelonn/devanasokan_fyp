import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/preparation/modeldata.csv")

# Select only the columns we need
df = df[['verse', 'label']]

# Split the data into features and target variable
X = df['verse']
y = df['label']

# Split the data into training and testing sets (70% training, 30% testing)
X_train, X_val_test, y_train, y_val_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Further split the validation and test sets (15% validation, 15% testing)
X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size=0.5, random_state=42)

# Save the training, validation, and test sets to CSV files
train_df = pd.DataFrame({'verse': X_train, 'label': y_train})
train_df.to_csv("C:/Users/User/Documents/devanasokan_fyp/modeldata/train.csv", index=False)
val_df = pd.DataFrame({'verse': X_val, 'label': y_val})
val_df.to_csv("C:/Users/User/Documents/devanasokan_fyp/modeldata/val.csv", index=False)
test_df = pd.DataFrame({'verse': X_test, 'label': y_test})
test_df.to_csv("C:/Users/User/Documents/devanasokan_fyp/modeldata/test.csv", index=False)