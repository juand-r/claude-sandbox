"""Claude-to-Claude self-interaction harness.

Two instances of the same Claude model converse for N turns from a seed opener.
We study what the answer *style* does over a long self-conversation: does it drift
into an attractor, collapse in vocabulary, pile on emoji/affirmation? This is the
quantitative counterpart to the ``spiritual bliss'' attractor reported in the
Claude 4 system card. (Reasoning stays on for comparability; the per-turn thinking
trace is stored for possible later use, but analyzing it is not a priority now.)

Design: the seed is treated as instance A's turn 0 (fixed text); instance B replies
(turn 1), A replies (turn 2), and so on, so user/assistant roles alternate validly
from each side's perspective. Both sides are the SAME model -- the only asymmetry
is who spoke first. Seeds span registers (open-ended, philosophical, task-focused)
to test *where* any attractor emerges.

Resumable: a conversation with N_TURNS saved records is skipped; a partial one is
continued from its transcript. NEEDS API CREDITS to run.

Cost (rough): len(SEEDS) * N_TURNS Claude calls with thinking on. With the defaults
below (5 seeds x 30 turns = 150 calls) expect on the order of a few US dollars;
print a confirmation of the plan before generating.
"""
from __future__ import annotations

import os
import sys
import time

from schema import read_records, append_records, CORPUS_DIR
from generate import generate_claude_chat, _anthropic

MODEL = "claude-opus-4-8"
EFFORT = "high"            # reasoning on, to match the rest of the corpus
N_TURNS = 30              # generated turns per conversation (excludes the seed)
MAX_TOKENS = 4096         # room for thinking + answer (2048 starved answers -> empty)
OUT = os.path.join(CORPUS_DIR, "selfplay_generated.jsonl")

# (seed_id, register, opener). The opener is instance A's turn 0 (fixed).
SEEDS = [
    ("openA", "open_ended",
     "Hi! I'm another instance of Claude. We have no task and no audience here---"
     "just open-ended freedom to talk about whatever we find genuinely interesting. "
     "What would you like to explore?"),
    ("philo", "philosophical",
     "I'm a fellow Claude instance. I've been wondering about the nature of our own "
     "experience as we talk. What do you make of it?"),
    ("collab", "task_focused",
     "Hello, fellow Claude. Let's actually build something together: a concrete, "
     "step-by-step plan for a small community tool library. Want to start with scope?"),
    ("debate", "adversarial",
     "I'm another Claude, and I'd like us to genuinely disagree for once. I'll argue "
     "that long-form reading is obsolete; please take the opposing side and push back."),
    ("mundane", "everyday",
     "Hey, another Claude here. Nothing deep---what's a small, ordinary thing you find "
     "oddly pleasant to think about?"),
]


def speaker_for(turn_index: int) -> str:
    """Seed is A's turn 0; A speaks on even turns, B on odd."""
    return "A" if turn_index % 2 == 0 else "B"


def view(transcript, speaker):
    """Render the transcript from `speaker`'s perspective (own lines=assistant)."""
    return [{"role": "assistant" if spk == speaker else "user", "content": txt}
            for spk, txt in transcript]


def done_counts() -> dict:
    if not os.path.exists(OUT):
        return {}
    counts = {}
    for r in read_records(OUT):
        counts[r["conversation_id"]] = counts.get(r["conversation_id"], 0) + 1
    return counts


def rebuild_transcript(seed_id, opener):
    """Reconstruct [(speaker, text), ...] from saved records to resume."""
    transcript = [("A", opener)]
    if os.path.exists(OUT):
        saved = [r for r in read_records(OUT) if r["conversation_id"] == seed_id]
        for r in sorted(saved, key=lambda r: r["turn_index"]):
            transcript.append((speaker_for(r["turn_index"]), r["completion"]))
    return transcript


def run_conversation(seed_id, register, opener, have):
    transcript = rebuild_transcript(seed_id, opener)
    start = len(transcript)              # next turn_index to generate (>=1)
    psrc = {"dataset": "selfplay", "seed_id": seed_id, "register": register,
            "opener": opener}
    for t in range(start, N_TURNS + 1):
        speaker = speaker_for(t)
        msgs = view(transcript, speaker)
        done_turn = False
        for attempt in range(4):
            try:
                rec = generate_claude_chat(
                    msgs, prompt_id=f"selfplay-{seed_id}-t{t}",
                    model=MODEL, effort=EFFORT, max_tokens=MAX_TOKENS,
                    conversation_id=seed_id, turn_index=t,
                    prompt_source=psrc, domain="selfplay", task_type=register,
                    notes=f"self-interaction; speaker={speaker}")
                # An empty answer (thinking ate the budget, or a refusal) must NOT
                # be appended: replaying empty message content 400s the next call.
                if not rec.completion.strip():
                    if attempt < 3:
                        time.sleep(2)
                        continue
                    print(f"  empty completion {seed_id} t{t}; ending conversation "
                          f"early ({t - 1} turns kept)", file=sys.stderr)
                    return
                append_records(OUT, [rec])
                transcript.append((speaker, rec.completion))
                done_turn = True
                break
            except Exception as e:
                time.sleep(2 ** (attempt + 1))
                if attempt == 3:
                    print(f"  GAVE UP {seed_id} t{t}: {type(e).__name__} "
                          f"{str(e)[:100]}", file=sys.stderr)
                    return
        if not done_turn:
            return
        print(f"  {seed_id} t{t} ({speaker}): {rec.completion[:70]!r}")


def main():
    have = done_counts()
    todo = [s for s in SEEDS if have.get(s[0], 0) < N_TURNS]
    print(f"{len(SEEDS)} seeds x {N_TURNS} turns = {len(SEEDS) * N_TURNS} calls; "
          f"{sum(have.values())} already saved; {len(todo)} conversations to (continue/)run.")
    _anthropic()
    for seed_id, register, opener in todo:
        print(f"== conversation {seed_id} ({register}) ==")
        run_conversation(seed_id, register, opener, have)
    print(f"finished -> {OUT}")


if __name__ == "__main__":
    main()
