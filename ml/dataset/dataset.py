import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset

class RedFlagDataset(Dataset):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df

    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        
        