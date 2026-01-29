"""Debug script to understand column predictions."""

import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer

print("Loading GPT-2...")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

def get_top_p(context_str, p=0.9, limit=20):
    """Show top-p words for a context."""
    if context_str:
        input_ids = tokenizer.encode(context_str, return_tensors="pt")
    else:
        input_ids = torch.tensor([[tokenizer.bos_token_id or 50256]])

    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits[0, -1, :]
        probs = F.softmax(logits, dim=-1)

    sorted_probs, sorted_indices = torch.sort(probs, descending=True)

    print(f"\nContext: '{context_str}'")
    print(f"Top-p={p} words:")
    cumulative = 0.0
    count = 0
    for prob, idx in zip(sorted_probs, sorted_indices):
        token = tokenizer.decode([idx.item()]).strip()
        if not token or not token[0].isalpha():
            continue
        print(f"  {token:15} {prob.item():.4f} (cum: {cumulative + prob.item():.4f})")
        cumulative += prob.item()
        count += 1
        if cumulative >= p or count >= limit:
            break
    print(f"  --- {count} words to reach p={p} ---")

# From the result:
# Grid:
# it is not
# in itself a
# crime punishable by

# Let's trace column 3 (words: "not", "a", "by")
print("="*60)
print("TRACING COLUMN 3: 'not' -> 'a' -> 'by'")
print("="*60)

# Row 0, Col 2: What comes after empty context? (first word of col 3)
get_top_p("", p=0.9)

# Row 1, Col 2: What comes after "not"? (column context)
get_top_p("not", p=0.9)

# Row 2, Col 2: What comes after "not a"? (column context)
get_top_p("not a", p=0.9)

# Now let's see the horizontal contexts that led to these choices
print("\n" + "="*60)
print("HORIZONTAL CONTEXTS")
print("="*60)

# Row 0: "it is" -> next word
get_top_p("it is", p=0.9)

# Row 1: "it is not in itself" -> next word should include "a"
get_top_p("it is not in itself", p=0.9)

# Row 2: "it is not in itself a crime punishable" -> next word should include "by"
get_top_p("it is not in itself a crime punishable", p=0.9)

print("\n" + "="*60)
print("THE PROBLEM")
print("="*60)
print("""
The issue: 'by' is in the intersection because:
- Horizontal: "crime punishable" -> "by" is very likely
- Column: "not a" -> "by" might be in top-p (check above)

But "not a by" as a standalone sentence is nonsense.
The intersection constraint doesn't guarantee column coherence.
""")
