from transformers import BertTokenizer, BertModel
import torch

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# read sentences from a text file 
with open("app_permission.txt", "r") as text_file:
    sentences = text_file.readlines()
    sentences = [sentence.strip() for sentence in sentences]


# Tokenize and encode the sentences
inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")

# Get the BERT model outputs
outputs = model(**inputs)

# Extract the pooled output (sentence embeddings)
sentence_embeddings = outputs.pooler_output

print("Sentence embeddings:", sentence_embeddings)