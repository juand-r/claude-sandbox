"""Tokenizer and token files for TinyStories.

Trains a byte-level BPE tokenizer with VOCAB tokens (one of them the
end-of-story token) on the training shard, then writes every story, followed
by the end-of-story token, as uint16 token ids:

  data/tokenizer.json
  data/train.bin, data/valid.bin   (numpy uint16)

Usage: python prepare.py
"""
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers

DATA = Path(__file__).parent / "data"
VOCAB = 4096
EOS = "<|eos|>"
N_TOKENIZER_STORIES = 200_000      # stories used to train the tokenizer


def stories(name):
    return pq.read_table(DATA / name).column("text").to_pylist()


def train_tokenizer(texts):
    tok = Tokenizer(models.BPE())
    tok.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tok.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(vocab_size=VOCAB, special_tokens=[EOS],
                                  initial_alphabet=pre_tokenizers.ByteLevel.alphabet())
    tok.train_from_iterator(texts, trainer)
    if tok.get_vocab_size() != VOCAB:
        raise RuntimeError(f"tokenizer has {tok.get_vocab_size()} tokens, expected {VOCAB}")
    return tok


def encode(tok, texts, chunk=10_000):
    """Token ids of all stories, each followed by EOS. In chunks: encoding all
    530k stories at once needed 14 GB and was killed (NOTES.md)."""
    eos = tok.token_to_id(EOS)
    parts = []
    for s in range(0, len(texts), chunk):
        ids = []
        for enc in tok.encode_batch(texts[s:s + chunk]):
            ids.extend(enc.ids)
            ids.append(eos)
        parts.append(np.array(ids, dtype=np.uint16))
    return np.concatenate(parts)


def main():
    train_texts = stories("train0.parquet")
    valid_texts = stories("valid.parquet")
    path = DATA / "tokenizer.json"
    if path.exists():
        tok = Tokenizer.from_file(str(path))
        print("reusing", path)
    else:
        tok = train_tokenizer(train_texts[:N_TOKENIZER_STORIES])
        tok.save(str(path))
    for name, texts in (("train", train_texts), ("valid", valid_texts)):
        ids = encode(tok, texts)
        ids.tofile(DATA / f"{name}.bin")
        print(f"{name}: {len(texts):,} stories, {len(ids):,} tokens, {len(ids) / len(texts):.0f} per story")
    print("eos id:", tok.token_to_id(EOS))


if __name__ == "__main__":
    main()
