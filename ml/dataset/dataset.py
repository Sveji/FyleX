import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset
from tokenizer.tokenizer import GPT4Tokenizer
from torch.nn.utils.rnn import pad_sequence

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
        try:
            text = item['raw_text']
            label = item['binary']
        except KeyError as e:
            print(f"Missing key: {e}")
            raise

        encoded = self.tokenizer.encode(text)[:self.max_seq_len]
        encoded_tensor = torch.tensor(encoded, dtype=torch.long)
        label_tensor = torch.tensor(label, dtype=torch.float)

        return encoded_tensor, label_tensor


        