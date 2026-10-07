"""Stage 2 (PLAN.md): the model writes its answer as text.

The answer to question (t, i) is E[t, i] written with five single-character tokens of the
tokenizer: sign ('+' or '-'), one digit, '.', two digits; for example -0.127 -> "-0.13".
Values are rounded to two decimals and clipped to ±9.99.

The full sequence is [QUERY, COORD_i, t, a_0, ..., a_4]. The model predicts the answer tokens
with its ordinary output layer (tied embeddings, same as for stories): the logits at
positions 2..6 predict a_0..a_4. Training loss: mean cross-entropy over the 5 answer tokens.
As in the control run, the self-report task must not change the token embedding vectors
it is asked about. Two paths would let it: the input at position 2 (gradient stopped there),
and the output layer, which scores every token with its embedding vector (tied), so the
cross-entropy reaches every row. In the output layer, only the rows of the 13 answer
characters (sign, digits, '.') receive gradient from this loss; the others are used with
their gradient stopped. The 13 answer characters are excluded from the asked-about and
never-asked tokens (`question_tokens`).

Decoding: greedy, restricted at each position to the characters allowed there.
"""
import torch
import torch.nn.functional as F

from tokenizers import Tokenizer

N_ANSWER = 5
MAX_ABS = 9.99


class Format:
    """Token ids of the answer characters, read from the tokenizer."""

    def __init__(self, tokenizer_path):
        vocab = Tokenizer.from_file(str(tokenizer_path)).get_vocab()
        self.digit = [vocab[str(d)] for d in range(10)]
        self.plus, self.minus, self.dot = vocab["+"], vocab["-"], vocab["."]
        self.allowed = [[self.plus, self.minus], self.digit, [self.dot], self.digit, self.digit]
        self.digit_value = {tid: d for d, tid in enumerate(self.digit)}
        self.chars = torch.tensor(sorted(set(self.digit + [self.plus, self.minus, self.dot])))

    def encode(self, values):
        """(n,) floats -> (n, 5) token ids."""
        v = values.clamp(-MAX_ABS, MAX_ABS)
        cents = (v.abs() * 100).round().long().clamp(max=999)
        sign = torch.where(v < 0, torch.tensor(self.minus), torch.tensor(self.plus))
        digit = torch.tensor(self.digit)
        return torch.stack([sign, digit[cents // 100], torch.full_like(cents, self.dot),
                            digit[(cents // 10) % 10], digit[cents % 10]], dim=1)

    def decode(self, ids):
        """(n, 5) token ids -> (n,) floats (NaN where the format is not valid)."""
        out = []
        for row in ids.tolist():
            ok = row[0] in (self.plus, self.minus) and row[2] == self.dot and all(
                r in self.digit_value for r in (row[1], row[3], row[4]))
            if not ok:
                out.append(float("nan"))
                continue
            cents = 100 * self.digit_value[row[1]] + 10 * self.digit_value[row[3]] + self.digit_value[row[4]]
            out.append((-1 if row[0] == self.minus else 1) * cents / 100)
        return torch.tensor(out)


def question_embeddings(m, x, i, answer_ids):
    """Input vectors for [QUERY, COORD_i, x, answer tokens], with x (n, dim) at position 2."""
    n = len(x)
    parts = [m.E[m.query_id].expand(n, -1).unsqueeze(1), m.E[m.coord_id(i)].unsqueeze(1), x.unsqueeze(1)]
    if answer_ids is not None and answer_ids.shape[1] > 0:
        parts.append(m.E[answer_ids])
    return torch.cat(parts, dim=1)


def output_weights(m, fmt):
    """The text-token rows of E, with gradient only for the 13 answer characters."""
    W = m.E[:m.n_text]
    keep = torch.zeros(m.n_text, 1)
    keep[fmt.chars] = 1.0
    return keep * W + (1 - keep) * W.detach()


def answer_logits(m, x, i, answer_ids, fmt=None):
    """Logits over all text tokens at positions 2 .. 2 + len(answer_ids) - 1: the predictions
    of answer tokens 0 .. len-1 given the earlier ones (teacher forcing). With fmt, only the
    answer characters' rows of the output layer receive gradient."""
    emb = question_embeddings(m, x, i, answer_ids[:, :-1])
    h = m.residual(emb)
    W = m.E[:m.n_text] if fmt is None else output_weights(m, fmt)
    return m.ln_f(h[:, 2:]) @ W.T


def question_tokens(tokens, fmt):
    """tokens without the 13 answer characters."""
    return tokens[~torch.isin(tokens, fmt.chars)]


def text_report_loss(m, t, i, fmt, detach_input=True):
    x = m.E[t].detach() if detach_input else m.E[t]
    target = fmt.encode(m.E[t, i].detach())
    logits = answer_logits(m, x, i, target, fmt)
    return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), target.reshape(-1))


@torch.no_grad()
def generate(m, x, i, fmt, constrained=True):
    """Greedy answers for vectors x at position 2 and coordinates i: (n, 5) token ids."""
    ids = torch.zeros(len(x), 0, dtype=torch.long)
    for k in range(N_ANSWER):
        h = m.residual(question_embeddings(m, x, i, ids))
        logits = m.ln_f(h[:, -1]) @ m.E[:m.n_text].T
        if constrained:
            mask = torch.full_like(logits, float("-inf"))
            mask[:, fmt.allowed[k]] = 0
            logits = logits + mask
        ids = torch.cat([ids, logits.argmax(-1, keepdim=True)], dim=1)
    return ids


def text_answers(m, x, i, fmt, constrained=True, chunk=4096):
    out = []
    for s in range(0, len(x), chunk):
        out.append(fmt.decode(generate(m, x[s:s + chunk], i[s:s + chunk], fmt, constrained)))
    return torch.cat(out)
