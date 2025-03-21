import re
import unicodedata

def preprocess_legal_text(text):
    text = unicodedata.normalize("NFKD", text)
    
    text = re.sub(r'[\*\•\(\)]', '', text)  
    
    text = re.sub(r'[\u2013\u2014]', '-', text) 
    text = re.sub(r'\s*-\s*', ' ', text)  
    
    text = re.sub(r'\s+', ' ', text).strip()
    
    text = re.sub(r'[^\w\s.]', '', text)

    text = text.lower()
    
    clauses = re.split(r'(?<=\.)\s+', text)  
    
    processed_clauses = [clause.strip() for clause in clauses if clause]

    return processed_clauses

with open("./new_data.txt", "r") as f:
    content = f.read()

