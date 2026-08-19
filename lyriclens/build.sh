#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install dependencies (Notice: NO torch, only onnxruntime and transformers for tokenizing)
pip install -r requirements.txt

# 2. Automatically download and export the model to ONNX right on the Render server during build time
python lyriclens/export_to_onnx.py