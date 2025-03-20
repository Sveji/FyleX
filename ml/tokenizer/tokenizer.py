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

    def fit(self, corpus, vocab_size: int):
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
        tokens = list(text.encode("utf-8"))
        while len(tokens) >= 2:
            stats = self.get_stats(tokens)
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break 
            idx = self.merges[pair]
            tokens = self.merge(tokens, pair, idx)
        print(tokens)
        return tokens
        
    def decode(self, ids):
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in self.merges.items():
            vocab[idx] = vocab[p0] + vocab[p1]
        tokens = b"".join(vocab[idx] for idx in ids)
        text = tokens.decode("utf-8", errors="replace")
        return text

corpus = """
The deadliest virus in modern history, perhaps of all time, was the 1918 Spanish Flu. It killed about 20 to 50 million people worldwide, perhaps more. The total death toll is unknown because medical records were not kept in many areas.
The pandemic hit during World War I and devastated military troops. In the United States, for instance, more servicemen were killed from the flu than from the war itself. The Spanish flu was fatal to a higher proportion of young adults than most flu viruses.
The pandemic started mildly, in the spring of 1918, but was followed by a much more severe wave in the fall of 1918. The war likely contributed to the devastating mortality numbers, as large outbreaks occurred in military forces living in close quarters. Poor nutrition and the unsanitary conditions of war camps had an effect.
A third wave occurred in the winter and spring of 1919, and a fourth, smaller wave occurred in a few areas in spring 1920. Initial symptoms of the flu were typical: sore throat, headache, and fever. The flu often progressed rapidly to cause severe pneumonia and sometimes hemorrhage in the lungs and mucus membranes. A characteristic feature of severe cases of the Spanish Flu was heliotrope cyanosis, where the patient’s face turned blue from lack of oxygen in the cells. Death usually followed within hours or days.
Modern medicine such as vaccines, antivirals, and antibiotics for secondary infections were not available at that time, so medical personnel couldn’t do much more than try to relieve symptoms.
The flu ended when it had infected enough people that those who were susceptible had either died or developed immunity.
"""
tokenizer = GPT4Tokenizer()
tokenizer.fit(corpus, 270)
print(tokenizer.decode(tokenizer.encode("A freshly created tokenizer can already serialize MIDI or abc files into token sequences that can be used to train your model. But if you want to get the best performances (results quality) and efficiency (training and inference speed), you will need to train the tokenizer first!")))