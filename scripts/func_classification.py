import os

# Указываем использовать первую видеокарту
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# os.environ['TORCH_USE_CUDA_DSA'] = "1"
# os.environ['CUDA_LAUNCH_BLOCKING'] = "1"

import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

DEVICE = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

def classify_question_llm(question, tokenizer, model, classes):
    inputs = tokenizer(question, return_tensors='pt', padding=True, truncation=True).to(DEVICE)
    outputs = model(**inputs)
    predicted_class = outputs.logits.argmax(dim=-1).item()
    return classes[predicted_class]

def prepare_classificator():
    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-multilingual-cased')
    model = AutoModelForSequenceClassification.from_pretrained('./models/class.model').to(DEVICE)
    classes = pd.read_pickle('./models/classes.pickle')
    
    return tokenizer, model, classes

if __name__ == '__main__':
    pass