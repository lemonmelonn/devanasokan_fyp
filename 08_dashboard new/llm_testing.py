from functions import get_llm_explanation

import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response["message"]["content"])

# explanation = get_llm_explanation("4kV4N9D1iKVxx1KLvtTpjS", "explicit.csv")
# print(explanation)