from nltk.tokenize import word_tokenize 
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import torch
from torch.utils.data import random_split
from torch.utils.data import Dataset
import pandas as pd
import joblib
from tqdm import tqdm

def tokenize(input: str) -> list:
    """
    Tokenizes the input string into lowercase words.

    Args:
    - input (str): The text input that needs to be tokenized.

    Returns:
    - list: A list of lowercase tokens (words).
    """
    return word_tokenize(input.lower())

def train_vectorizer(dataset: pd.DataFrame, col: str, max_features: int = 10000) -> CountVectorizer:
    """
    Trains a CountVectorizer on a specific column of the dataset.

    Args:
    - dataset (pd.DataFrame): The pandas DataFrame containing the text data.
    - col (str): The name of the column in the DataFrame to use for vectorization.

    Returns:
    - CountVectorizer: The trained CountVectorizer instance.
    """
    vectorizer = CountVectorizer(tokenizer=tokenize, max_features=max_features)
    vectorizer.fit(dataset[col])

    vocab = vectorizer.vocabulary_
    vocab["<PAD>"] = len(vocab)  

    vectorizer.vocabulary_ = vocab

    return vectorizer

def save_vectorizer(vectorizer: CountVectorizer, filename: str) -> None:
    """
    Save a trained vectorizer object to a file using joblib.

    This function serializes and saves a fitted CountVectorizer to a specified file
    with a `.joblib` extension. The saved file can later be loaded for use in 
    transforming new text data.

    Parameters:
    -----------
    vectorizer : CountVectorizer
        A fitted CountVectorizer instance to be saved. It should have been trained on
        some text data before passing it to this function.
    
    filename : str
        The name of the file where the vectorizer will be saved. The `.joblib` 
        extension will be automatically appended to this filename.

    Returns:
    --------
    None
    """
    joblib.dump(vectorizer, f'{filename}.joblib')

def load_vectorizer(filename: str) -> CountVectorizer:
    """
    Load a previously saved vectorizer from a file.

    This function deserializes and loads a saved CountVectorizer object from a file
    with the `.joblib` extension. The loaded vectorizer can then be used to transform
    new text data.

    Parameters:
    -----------
    filename : str
        The path to the `.joblib` file where the vectorizer is stored.

    Returns:
    --------
    CountVectorizer
        The deserialized CountVectorizer object that was saved to the specified file.
    """
        
    vectorizer = joblib.load(filename)
    return vectorizer

def text_to_indices(text: str, vectorizer: CountVectorizer) -> list:
    """
    Converts a text string into a list of indices based on the trained vectorizer's vocabulary.

    Args:
    - text (str): The input text to be converted into indices.
    - vectorizer (CountVectorizer): The trained CountVectorizer instance used for vocabulary.

    Returns:
    - list: A list of indices corresponding to the words in the input text, based on the vectorizer's vocabulary.
    """
    tokens = tokenize(text)
    vocab = vectorizer.vocabulary_ 
    return [vocab[word] for word in tokens if word in vocab]  



def data_split(dataset: Dataset, split_ratio: float) -> tuple:
    """
    Splits a dataset into training and testing subsets based on the provided split ratio.

    Args:
    - dataset (Dataset): The dataset to be split.
    - split_ratio (float): The ratio of the dataset to be used for training (e.g., 0.8 for an 80%/20% split).

    Returns:
    - tuple: A tuple containing two elements:
        - train_data (Dataset): The training subset of the dataset.
        - test_data (Dataset): The testing subset of the dataset.
    """
    # Ensure the dataset is not too small to split
    if len(dataset) < 2:
        raise ValueError("Dataset is too small to split into training and testing subsets.")

    # Calculate the split index
    split_index = int(split_ratio * len(dataset))

    # Ensure the split index is between 1 and len(dataset) - 1
    split_index = max(1, min(split_index, len(dataset) - 1))

    # Perform the split using random_split
    train_data, test_data = random_split(dataset, [split_index, len(dataset) - split_index])
    
    return train_data, test_data


def accuracy_fn(y_true, y_pred):
    """
    Calculates accuracy between truth labels and predictions.

    Args:
        y_true (torch.Tensor): Truth labels for predictions.
        y_pred (torch.Tensor): Predictions to be compared to predictions.

    Returns:
        [torch.float]: Accuracy value between y_true and y_pred, e.g. 78.45
    """
    correct = torch.eq(y_true, y_pred).sum().item()
    acc = (correct / len(y_pred)) * 100
    return acc

def create_causal_mask(seq_len):
    mask = torch.tril(torch.ones(seq_len, seq_len))  
    mask = mask.unsqueeze(0)    
    return mask

def preprocessing_for_bert(data, tokenizer, max_seq_len):

    # Create empty lists to store outputs
    input_ids = []
    attention_masks = []

    # For every sentence...
    for sent in tqdm(data):
        # `encode_plus` will:
        #    (1) Tokenize the sentence
        #    (2) Add the `[CLS]` and `[SEP]` token to the start and end
        #    (3) Truncate/Pad sentence to max length
        #    (4) Map tokens to their IDs
        #    (5) Create attention mask
        #    (6) Return a dictionary of outputs
        

        encoded_sent = tokenizer.encode_plus(
            text=sent,  
            add_special_tokens=True,        # Add `[CLS]` and `[SEP]`
            max_length=max_seq_len,             # Max length to truncate/pad
            pad_to_max_length=True,         # Pad or Truncate sentences to max length
            return_attention_mask=True      # Return attention mask
            )
        
        # Add the outputs to the lists
        input_ids.append(encoded_sent.get('input_ids'))
        attention_masks.append(encoded_sent.get('attention_mask'))

    # Convert lists to tensors
    input_ids = torch.tensor(input_ids)
    attention_masks = torch.tensor(attention_masks)

    return input_ids, attention_masks