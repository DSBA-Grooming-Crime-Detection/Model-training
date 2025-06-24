import torch
import torch.nn.functional as F
from transformers import BartTokenizerFast, BartForSequenceClassification
import os

MODEL_PATH = os.environ.get("MODEL_PATH")

print("MODEL_PATH:", MODEL_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = BartTokenizerFast.from_pretrained(MODEL_PATH)
model = BartForSequenceClassification.from_pretrained(MODEL_PATH).to(device)
model.eval()

def detect_risk(messages: list[dict], max_len=512) -> float:
    full_text = " ".join([msg["text"].strip() + " </s>" for msg in messages if "text" in msg])

    inputs = tokenizer(
        full_text,
        return_tensors='pt',
        truncation=True,
        max_length=max_len,
        padding='max_length',
        add_special_tokens=False
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=-1).squeeze().cpu().numpy()
        grooming_prob = float(probs[1])  # class 1 = 그루밍

    return round(grooming_prob, 4)
