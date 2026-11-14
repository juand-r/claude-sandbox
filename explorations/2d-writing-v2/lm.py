"""Score text with a small causal language model (SmolLM2-360M, CPU)."""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "HuggingFaceTB/SmolLM2-360M"
BATCH_SIZE = 64


class Scorer:
    def __init__(self, model_name=MODEL_NAME):
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.tok.pad_token = self.tok.eos_token
        self.tok.padding_side = "right"
        self.model = AutoModelForCausalLM.from_pretrained(model_name, dtype=torch.float32).eval()
        self.bos = self.tok.bos_token_id

    @torch.no_grad()
    def logprobs(self, texts):
        """Total log-probability (nats) of each text, conditioned on BOS.

        Returns a list of (logprob, n_tokens)."""
        results = []
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]
            enc = self.tok(batch, return_tensors="pt", padding=True, add_special_tokens=False)
            bos = torch.full((len(batch), 1), self.bos)
            ids = torch.cat([bos, enc.input_ids], dim=1)
            mask = torch.cat([torch.ones_like(bos), enc.attention_mask], dim=1)
            logits = self.model(input_ids=ids, attention_mask=mask).logits
            lp = torch.log_softmax(logits[:, :-1], dim=-1)
            tok_lp = lp.gather(2, ids[:, 1:].unsqueeze(-1)).squeeze(-1) * enc.attention_mask
            n = enc.attention_mask.sum(1)
            results += list(zip(tok_lp.sum(1).tolist(), n.tolist()))
        return results
