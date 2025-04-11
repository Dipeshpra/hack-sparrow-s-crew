from transformers import ViTForImageClassification, ViTFeatureExtractor
from PIL import Image
import torch

model_name = "google/vit-base-patch16-224"
model = ViTForImageClassification.from_pretrained(model_name)
feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)

def detect_image_fake(filepath):
    image = Image.open(filepath).convert("RGB")
    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=1)
    # Using a dummy threshold for deepfake estimation
    score = round(probabilities[0].max().item() * 100, 2)
    explanation = f"Highest class confidence (generic class): {score}%. Used for deepfake approximation."
    return score, explanation
