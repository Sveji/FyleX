import re
import torch
from torch.nn.utils.rnn import pad_sequence
from model.model import Model
from tokenizer.tokenizer import GPT4Tokenizer
import pickle

VOCAB_SIZE = 1024
D_MODEL = 256
MAX_SEQ_LEN = 256


def preprocess_legal_text(text):
    clauses = re.split(r'(?<=\.)\s+|(?<=;)\s+|\n+', text)
    
    return clauses

model = Model(D_MODEL, VOCAB_SIZE, MAX_SEQ_LEN)
state_dict = torch.load('./pretrained-model')
model.load_state_dict(state_dict)
tokenizer = GPT4Tokenizer()
with open("./merges.pkl", "rb") as f:
    merges = pickle.load(f)
tokenizer.load(merges, VOCAB_SIZE)

def prediction(text):
    clauses = preprocess_legal_text(text)

    encoded_clauses = []
    
    for clause in clauses:
        token_ids = tokenizer.encode(clause)
        encoded_tensor = torch.tensor(token_ids, dtype=torch.long)
        encoded_clauses.append(encoded_tensor)
    
    padded_encoded = pad_sequence(encoded_clauses, batch_first=True, padding_value=0)
    
    with torch.inference_mode():
        model.eval()
        output = model(padded_encoded)
    
    output = torch.sigmoid(output)
    
    predictions = (output > 0.5).long()
    
    sap = []
    for i, clause in enumerate(clauses):
        if predictions[i].item() == 1:
            sap.append(clause)

    return sap
