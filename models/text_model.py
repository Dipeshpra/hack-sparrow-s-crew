from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

model_name = "roberta-base-openai-detector"
model = RobertaForSequenceClassification.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)

def detect_text_fake(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=1)
    score = round(probabilities[0][1].item() * 100, 2)
    explanation = f"Model confidence that text is machine-generated: {score}%"
    return score, explanation
