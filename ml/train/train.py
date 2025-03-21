import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
from utils.utils import accuracy_fn
from test.test import test_step

def train_step(model: nn.Module, loss_fn: nn.Module, optimizer: nn.Module, epochs: int, train_dataloader: DataLoader, test_dataloader: DataLoader, device) -> None:
    best_test_acc = 0
    for epoch in tqdm(range(epochs)):
        model.train()
        train_loss = 0
        train_acc = 0


        for batch, (X, y) in enumerate(train_dataloader):
            X = X.to(device)
            y = y.to(device)
            logits = model(X).squeeze(dim=1)
            
            loss = loss_fn(logits, y) 
            
            train_loss += loss.item()
            train_acc += accuracy_fn(y, torch.round(torch.sigmoid(logits)))  
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Averaging the loss and accuracy
        train_loss /= len(train_dataloader)
        train_acc /= len(train_dataloader)

        print(f"\nEpoch {epoch+1}/{epochs} - Train loss: {train_loss:.5f} | Train acc: {train_acc:.2f}%")
        test_acc = test_step(model, loss_fn, test_dataloader, device)
        if test_acc > best_test_acc:
            best_test_acc = test_acc
            torch.save(model.state_dict(), './pretrained-model')
            print(f"Model improved! Saved to ./model")