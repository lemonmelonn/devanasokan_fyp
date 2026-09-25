# push_dataset.py
from huggingface_hub import login, upload_file, whoami
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the Hugging Face token from environment variables
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Login to Hugging Face Hub
login(token=HF_TOKEN)
print(whoami())  # Check if logged in successfully

# Your dataset repo ID on Hugging Face Hub
repo_id = "devanasokan/song-appropriateness"

# List of local CSV files to upload, and what to call them in the repo
files_to_upload = {
    "./preparation/finalverses.csv": "verses-with-appropriateness-labels.csv",
}

for local_path, repo_path in files_to_upload.items():
    upload_file(
        path_or_fileobj=local_path,
        path_in_repo=repo_path,
        repo_id=repo_id,
        repo_type="dataset",
        commit_message=f"Upload {repo_path}",
    )
    print(f"Uploaded {local_path} -> https://huggingface.co/datasets/{repo_id}/blob/main/{repo_path}")