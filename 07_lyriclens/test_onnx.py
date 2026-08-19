import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

model_dir = "./onnx_model"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
session = ort.InferenceSession(f"{model_dir}/model.onnx")

id2label = {0: "SAFE", 1: "UNSAFE"}

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def test_prediction(text):
    encoded = tokenizer(
        text,
        return_tensors="np",
        truncation=True,
        max_length=512,
        padding=True
    )
    ort_inputs = {
        "input_ids": encoded["input_ids"].astype(np.int64),
        "attention_mask": encoded["attention_mask"].astype(np.int64),
    }
    logits = session.run(None, ort_inputs)[0]
    probs = softmax(logits)[0]
    pred_idx = int(np.argmax(probs))
    return id2label.get(pred_idx, "SAFE"), float(probs[pred_idx])

# Run a test classification
label, score = test_prediction("I love you, baby!")
print(f"Prediction Result: {label} (Confidence: {score:.4f})")