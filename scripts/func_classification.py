import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

def classify_question_llm(question, tokenizer, model, classes):
    inputs = tokenizer(question, return_tensors='pt', padding=True, truncation=True).to(DEVICE)
    outputs = model(**inputs)
    predicted_class = outputs.logits.argmax(dim=-1).item()
    return classes[predicted_class]

def prepare_classificator():
    tokenizer = AutoTokenizer.from_pretrained('./models/distilbert-base-multilingual-cased')
    model = AutoModelForSequenceClassification.from_pretrained('./models/class.model').to(DEVICE)
    classes = pd.read_pickle('./models/classes.pickle')
    
    return tokenizer, model, classes

if __name__ == '__main__':
    pass