import torch
import torch.nn as nn
import math

class InputEmbeddings(nn.Module):
    def __init__(self, d_model: int, vocab_size: int) -> None:
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, d_model)

    def forward(self, x):
        return self.embedding(x) * math.sqrt(self.d_model)
    
class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, seq_len: int, dropout: float) -> None:
        super().__init__()
        self.d_model = d_model
        self.seq_len = seq_len
        self.dropout = nn.Dropout(dropout)
        pe = torch.zeros(seq_len, d_model)
        position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)) 
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0) 
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + (self.pe[:, :x.shape[1], :]).requires_grad_(False) 
        return self.dropout(x)

class AttBiLSTM(nn.Module):
    def __init__(self, d_model, hidden_size, num_layers):
        super().__init__()
        self.lstm = nn.LSTM(d_model, hidden_size, num_layers, bidirectional=True, batch_first=True)
        self.attention = nn.Linear(hidden_size * num_layers, hidden_size * num_layers)
        self.linear = nn.Linear(hidden_size * num_layers, 1)
    def forward(self, x):
        output, _ = self.lstm(x)
        attention_scores = self.attention(output)
        att_weights = torch.softmax(attention_scores, dim = 1)
        x = torch.sum(att_weights * attention_scores, dim = 1)
        x = self.linear(x)
        return x

        

class Model(nn.Module):
    def __init__(self, d_model: int, vocab_size: int, seq_len: int):
        super().__init__()
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.input_embedding = InputEmbeddings(d_model, vocab_size)
        self.pos_enc = PositionalEncoding(d_model, seq_len, 0.1)
        self.att = AttBiLSTM(d_model = d_model, hidden_size=128, num_layers=2)

    def forward(self, x):
        x = self.input_embedding(x)
        # x = self.pos_enc(x)
        x = self.att(x)
        return x
    
def test_model():
    d_model = 128
    vocab_size = 1024
    seq_len = 512
    model = Model(d_model = d_model, vocab_size=vocab_size, seq_len=seq_len)
    inp = torch.randint(0, vocab_size, (1, seq_len), dtype=torch.long)
    model(inp)


# test_model()