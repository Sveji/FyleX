import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset
from tokenizer.tokenizer import GPT4Tokenizer

class RedFlagDataset(Dataset):
    def __init__(self, df: pd.DataFrame, tokenizer: GPT4Tokenizer, max_seq_len: int = 256):
        super().__init__()
        self.df = df
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len

    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        item = self.df.iloc[idx]
        encoded = self.tokenizer.encode(item[:self.max_seq_len])
        return encoded

        