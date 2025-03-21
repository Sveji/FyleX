import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from model.model import Model
from tokenizer.tokenizer import GPT4Tokenizer
from dataset.dataset import RedFlagDataset
from utils.utils import data_split
from train.train import train_step
import pickle
import pandas as pd
from torch.nn.utils.rnn import pad_sequence

def redflag_collate_fn(batch):
    encoded_batch, label_batch = zip(*batch)

    padded_encoded = pad_sequence(encoded_batch, batch_first=True, padding_value=0)

    labels = torch.stack(label_batch)

    return padded_encoded, labels

VOCAB_SIZE = 1024
D_MODEL = 256
MAX_SEQ_LEN = 256
TRAIN_TEST_SPLIT = 0.85
BATCH_SIZE = 32
# Setup device agnostic code
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using: {device}")

# Load the tokenizer
with open("tokenizer_corpus.txt", "r") as f:
    content = f.read()

tokenizer = GPT4Tokenizer()

# Train the tokenizer (if mandatory) and save the merges
# tokenizer.fit(content, VOCAB_SIZE)
# 
# with open("merges.pkl", "wb") as f:
#     pickle.dump(tokenizer.merges, f)

# Load the merges dictionary
with open("merges.pkl", "rb") as f:
    merges = pickle.load(f)

tokenizer.load(merges, VOCAB_SIZE)

# Load the dataset and split into train and test
df = pd.read_csv('./dataset/dist/preprocessed_df.csv')
train_ds = df.iloc[:15000]
test_ds = df.iloc[15000:]

train_dataset = RedFlagDataset(train_ds, tokenizer, MAX_SEQ_LEN)
test_dataset = RedFlagDataset(test_ds, tokenizer, MAX_SEQ_LEN)

# Create the iterative data loaders
train_dataloader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    collate_fn=redflag_collate_fn
)

test_dataloader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    collate_fn=redflag_collate_fn
)

# Load the model
model = Model(D_MODEL, VOCAB_SIZE, MAX_SEQ_LEN).to(device)

# Setup training hyperparameters
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters())
lr = 3e-4
epochs = 4

train_step(model, loss_fn, optimizer, epochs, train_dataloader, test_dataloader, device)