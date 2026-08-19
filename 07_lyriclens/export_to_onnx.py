from pathlib import Path
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_id = "devanasokan/bert-lyrics-classifier"
output_dir = Path("./onnx_model")
output_dir.mkdir(exist_ok=True)

print("Downloading BERT model & tokenizer from Hugging Face...")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)
model.eval()

print("Exporting to ONNX format...")
dummy_text = "This is a test lyric verse"
inputs = tokenizer(
    dummy_text,
    return_tensors="pt",
    max_length=512,
    truncation=True,
    padding="max_length"
)

onnx_path = output_dir / "model.onnx"

torch.onnx.export(
    model,
    (inputs["input_ids"], inputs["attention_mask"]),
    str(onnx_path),
    input_names=["input_ids", "attention_mask"],
    output_names=["logits"],
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "sequence_length"},
        "attention_mask": {0: "batch_size", 1: "sequence_length"},
        "logits": {0: "batch_size"},
    },
    opset_version=14,
)

tokenizer.save_pretrained(output_dir)
print(f"🎉 Model exported successfully to: {output_dir.resolve()}")