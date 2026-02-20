import os
import shutil

# 1. Define your path explicitly using a raw string
my_local_path = r'C:/Users/User/Documents/devanasokan_fyp/my_bert_models'

# 2. Set ALL relevant environment variables BEFORE importing transformers
os.environ['HF_HOME'] = my_local_path
os.environ['HF_DATASETS_CACHE'] = os.path.join(my_local_path, 'datasets')
os.environ['TRANSFORMERS_CACHE'] = os.path.join(my_local_path, 'models')
os.environ['HUGGINGFACE_HUB_CACHE'] = os.path.join(my_local_path, 'hub')

# Create the folder if it doesn't exist
os.makedirs(my_local_path, exist_ok=True)

# 3. Now import the library
from transformers import pipeline

print("Attempting to load NSFW model...")

try:
    # 4. Use 'cache_dir' to double-force the path
    classifier = pipeline(
        "text-classification", 
        model="Zohair101/Foul-Language-Detection-DH", 
        cache_dir=my_local_path
    )
    print("Model loaded successfully!")
    
    # Test it
    test_result = classifier("I love sunshine")
    print(f"Test Result: {test_result}")

except Exception as e:
    print(f"Error: {e}")