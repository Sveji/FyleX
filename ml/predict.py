import re
import unicodedata
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
with open("merges.pkl", "rb") as f:
    merges = pickle.load(f)
tokenizer.load(merges, VOCAB_SIZE)

def predict(text):
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
    
    sap = {}
    for i, clause in enumerate(clauses):
        sap[clause] = predictions[i]

    return sap

text = """

Dear Valued Client,

We are pleased to inform you that your account has been pre-approved for an exclusive financial windfall. You are among the lucky few to receive access to this once-in-a-lifetime opportunity. Our investors have achieved incredible returns, and now it’s your turn to profit, starting today.

For a limited time only, we are offering you the chance to invest a small initial amount that guarantees you returns of up to 500% in just 7 days. This is a high-return opportunity, but don’t wait – the window will close in 48 hours!

To take part, you must follow these simple steps:

    Deposit $500 into our secure account using the details provided.
    Provide your personal details and bank account information to ensure your returns are credited properly.
    Wait for your funds to grow exponentially.

This is a unique opportunity that has been tailored just for you. Only a handful of clients will be allowed to take advantage of this, and once it’s gone, it’s gone for good.

Act now to secure your future wealth!

Best regards,
Robert Johnson
Financial Consultant
Wealth Strategies Group
Phone: (888) 456-7890
Email: r.johnson@wealthstrategiesgroup.com
"""

print(predict(text))