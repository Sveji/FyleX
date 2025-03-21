import regex as re

class GPT4Tokenizer:
    def __init__(self):
        self.vocab_size = None
        self.merges = {}
        self.re = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""


    def load(self, merges: dict, vocab_size: int):
        self.merges = merges
        self.vocab_size = vocab_size

    def get_stats(self, ids):
        counts = {}
        for pair in zip(ids, ids[1:]): 
            counts[pair] = counts.get(pair, 0) + 1
        return counts

    def merge(self, ids, pair, idx):
        newids = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
                newids.append(idx)
                i += 2
            else:
                newids.append(ids[i])
                i += 1
        return newids
    
    def fit(self, corpus, vocab_size: int, special_token = True):
        preprocess_corpus = re.findall(self.re, corpus)
        tokenized = [list(x.encode("utf-8")) for x in preprocess_corpus]  
        
        self.vocab_size = vocab_size
        num_merges = vocab_size - 256

        for i in range(num_merges):
            global_stats = {}
            for bite in tokenized:
                stats = self.get_stats(bite)
                for pair, count in stats.items():
                    global_stats[pair] = global_stats.get(pair, 0) + count  
            
            if not global_stats:
                break

            pair = max(global_stats, key=global_stats.get)
            idx = 256 + i
            print(f"Merging {pair} into a new token {idx}")

            for j in range(len(tokenized)):
                tokenized[j] = self.merge(tokenized[j], pair, idx)
            
            self.merges[pair] = idx  

        


    def encode(self, text):
        tokens = list(str(text).encode("utf-8"))
        while len(tokens) >= 2:
            stats = self.get_stats(tokens)
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break 
            idx = self.merges[pair]
            tokens = self.merge(tokens, pair, idx)
        return tokens
        
    def decode(self, ids):
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in self.merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]
        tokens = b"".join(vocab[idx] for idx in ids)
        text = tokens.decode("utf-8", errors="replace")
        return text


