"""Debug script to understand GPT-2 behavior in the 2D grid."""

import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer

print("Loading GPT-2...")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

VOCAB = [
    "the", "a", "an", "this", "that", "my", "your", "his", "her",
    "i", "you", "he", "she", "it", "we", "they",
    "man", "woman", "child", "time", "day", "night", "life", "world",
    "way", "place", "house", "hand", "eye", "head", "heart", "mind",
    "is", "are", "was", "were", "be", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "can",
    "see", "know", "think", "make", "take", "come", "go", "want",
    "say", "said", "get", "give", "find", "tell", "feel", "become",
    "good", "new", "old", "great", "little", "own", "other", "long",
    "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "and", "but", "or", "if", "when", "so", "as", "than",
    "not", "all", "some", "no", "more", "just", "now", "then",
    "very", "also", "well", "only", "even", "still", "back", "there",
]

# Build word -> token_id mapping
word_to_token = {}
for word in VOCAB:
    tokens = tokenizer.encode(" " + word, add_special_tokens=False)
    if len(tokens) == 1:
        word_to_token[word] = tokens[0]

def get_top_k(context_str, k=20):
    """Get top-k vocab words after context."""
    if context_str:
        input_ids = tokenizer.encode(context_str, return_tensors="pt")
    else:
        input_ids = torch.tensor([[tokenizer.bos_token_id or 50256]])

    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits[0, -1, :]
        log_probs = F.log_softmax(logits, dim=-1)

    scores = []
    for word in VOCAB:
        if word in word_to_token:
            score = log_probs[word_to_token[word]].item()
            scores.append((word, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:k]

def show_top_k(context, k=10):
    print(f"\nContext: '{context}'")
    print(f"Top {k} words:")
    for word, score in get_top_k(context, k):
        print(f"  {word:12} {score:.3f}")

# Test various contexts
print("\n" + "="*60)
print("DEBUGGING GPT-2 PREDICTIONS")
print("="*60)

# What does GPT-2 think comes after "has"?
show_top_k("has")

# What does GPT-2 think comes after "to"?
show_top_k("to")

# What does GPT-2 think comes after "to and"?  (this is the problematic one)
show_top_k("to and")

# What does GPT-2 think comes after "to and in"?
show_top_k("to and in")

# Compare with n-gram style result
show_top_k("but")
show_top_k("but it")
show_top_k("but it is")

# Check the full problematic sequence scoring
print("\n" + "="*60)
print("FULL SEQUENCE PERPLEXITY CHECK")
print("="*60)

def score_sequence(text):
    """Score a sequence using GPT-2."""
    input_ids = tokenizer.encode(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        loss = outputs.loss.item()
    return -loss  # Higher is better

sequences = [
    "has to be a",       # First row
    "to and in the",     # Second row (problematic!)
    "be in my head",     # Third row
    "but it is not",     # n-gram result
    "it was the only",   # n-gram result
    "the man is good",   # sensible
    "to and fro",        # valid use of "to and"
]

for seq in sequences:
    score = score_sequence(seq)
    print(f"  '{seq}':  {score:.3f}")
