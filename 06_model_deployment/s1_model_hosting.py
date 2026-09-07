# Model Deployment
from huggingface_hub import login, upload_folder, whoami
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, pipeline

# Load environment variables from .env
load_dotenv()

# Get the Hugging Face token from environment variables
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Login to Hugging Face Hub
login(token=HF_TOKEN)
print(whoami())  # Check if logged in successfully

# Model repository ID on Hugging Face Hub
repo_id = "devanasokan/bert-lyrics-classifier"

# Push model folder to HF Hub repo
upload_folder(
    folder_path="./05_model_training/my_final_bert",
    repo_id=repo_id,
    repo_type="model",
    commit_message="Upload BERT model"
)

print(f"Model pushed to: https://huggingface.co/{repo_id}")

# Push tokenizer to HF Hub repo
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
tokenizer.push_to_hub(repo_id)

print(f"Tokenizer pushed to: https://huggingface.co/{repo_id}")

