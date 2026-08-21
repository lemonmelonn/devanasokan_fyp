# Testing Deployed Model
from transformers import pipeline

# Model repository ID on Hugging Face Hub
repo_id = "devanasokan/bert-lyrics-classifier"

# Import the pipeline for text classification
classifier = pipeline(
    "text-classification",
    model=repo_id,
)

test_input = ["She taught me love (Love), She taught me patience (Patience)",
              "How she handles pain (Pain), That shit's amazin' (Yeah, she's amazin')",
              "Only wanna do it once, real bad, Gon' make that shit last",
              "God forbid somethin' happens, Least this song is a smash (Song is a smash)"]

# Test the deployed model with sample inputs
for input_text in test_input:
    result = classifier(input_text)
    print(f"Input: {input_text}\nResult: {result}\n")

