import torch
import torch.nn as nn
from model.model import Model
from tokenizer.tokenizer import GPT4Tokenizer
from dataset.dataset import RedFlagDataset
from utils.utils import data_split
import pickle
import pandas as pd

VOCAB_SIZE = 1024
D_MODEL = 256
MAX_SEQ_LEN = 256
TRAIN_TEST_SPLIT = 0.85

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

df = pd.read_csv('./dataset/dist/preprocessed_df.csv')

dataset = RedFlagDataset(df, tokenizer, MAX_SEQ_LEN)
train_ds, test_df = data_split(df, TRAIN_TEST_SPLIT)

