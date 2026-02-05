"""
PlausibleQA dataset analysis.

PlausibleQA (SIGIR 2025): 10,000 questions with 10 candidate answers each.
Each question has one correct answer and 9 plausible-but-incorrect alternatives.
Answers have plausibility scores (0-100).

Source datasets: TriviaQA, Natural Questions, WebQuestions.
HuggingFace: JamshidJDMY/PlausibleQA
"""

from datasets import load_dataset
import pandas as pd
from collections import Counter
import json


def load_plausibleqa():
    """Load PlausibleQA from HuggingFace."""
    ds = load_dataset("JamshidJDMY/PlausibleQA")
    return ds


def explore_structure(ds):
    """Print raw structure of first example to understand the format."""
    print("\n" + "="*80)
    print("RAW STRUCTURE (first example)")
    print("="*80)
    split_name = list(ds.keys())[0]
    example = ds[split_name][0]
    print(f"Split: {split_name}")
    print(f"Keys: {list(example.keys())}")
    for key, val in example.items():
        if isinstance(val, str) and len(val) > 200:
            print(f"  {key}: {val[:200]}...")
        elif isinstance(val, list) and len(val) > 3:
            print(f"  {key}: list of {len(val)} items, first: {val[0]}")
        else:
            print(f"  {key}: {val}")


def build_question_df(ds):
    """
    Build a per-question DataFrame with answer counts.
    Returns (question_df, per_answer_df).
    """
    split_name = list(ds.keys())[0]  # might only have one split
    data = ds[split_name]

    question_records = []
    answer_records = []

    for i, row in enumerate(data):
        # Extract what we can -- field names may vary
        q_id = row.get("question_id", row.get("id", i))
        question_text = row.get("question", "")
        correct_answer = row.get("correct_answer", row.get("answer", ""))
        source = row.get("source_dataset", row.get("source", "unknown"))

        # Find candidate answers -- could be under various keys
        candidates = row.get("candidate_answers", row.get("candidates", []))

        # Count correct and incorrect among candidates
        n_correct = 0
        n_incorrect = 0
        for cand in candidates:
            if isinstance(cand, dict):
                answer_text = cand.get("CandidateAnswer", cand.get("answer", cand.get("text", "")))
                score = cand.get("PlausibilityScore", cand.get("plausibility_score", cand.get("score", None)))
                is_correct = (answer_text.strip().lower() == str(correct_answer).strip().lower())
            else:
                answer_text = str(cand)
                score = None
                is_correct = (answer_text.strip().lower() == str(correct_answer).strip().lower())

            if is_correct:
                n_correct += 1
            else:
                n_incorrect += 1

            answer_records.append({
                "question_id": q_id,
                "answer": answer_text,
                "plausibility_score": score,
                "is_correct": is_correct,
            })

        # If no candidates found, try alternative structures
        if len(candidates) == 0:
            # Maybe answers are in columns directly
            n_correct = 1  # at least the correct answer
            n_incorrect = 0

        question_records.append({
            "question_id": q_id,
            "question": question_text,
            "correct_answer": correct_answer,
            "source": source,
            "n_candidates": len(candidates),
            "n_correct": n_correct,
            "n_incorrect": n_incorrect,
            "total_answers": len(candidates) if len(candidates) > 0 else 1,
        })

    return pd.DataFrame(question_records), pd.DataFrame(answer_records), split_name


def print_examples(qdf, adf, n=3):
    """Print n example questions with their answers."""
    for i in range(min(n, len(qdf))):
        row = qdf.iloc[i]
        print(f"\n{'='*80}")
        print(f"Example {i+1} (id={row['question_id']})")
        print(f"{'='*80}")
        print(f"Source: {row['source']}")
        print(f"Question: {row['question']}")
        print(f"Correct answer: {row['correct_answer']}")

        answers = adf[adf["question_id"] == row["question_id"]]
        if len(answers) > 0:
            print(f"\nCandidate answers ({len(answers)}):")
            for _, a in answers.iterrows():
                marker = "CORRECT" if a["is_correct"] else "WRONG"
                score_str = f" (plausibility={a['plausibility_score']})" if pd.notna(a["plausibility_score"]) else ""
                print(f"  [{marker}]{score_str} {a['answer']}")


def print_basic_stats(qdf, split_name):
    """Print basic statistics."""
    print(f"\n{'='*80}")
    print(f"Basic Stats: {split_name}")
    print(f"{'='*80}")
    print(f"Number of questions: {len(qdf)}")

    if "source" in qdf.columns:
        print(f"Source distribution:")
        for src, count in qdf["source"].value_counts().items():
            print(f"  {src}: {count}")

    print()
    for col, label in [
        ("total_answers", "Total answers per question"),
        ("n_correct", "Correct answers per question"),
        ("n_incorrect", "Incorrect answers per question"),
    ]:
        if col in qdf.columns:
            print(f"{label}:")
            print(f"  min={qdf[col].min()}, max={qdf[col].max()}, "
                  f"mean={qdf[col].mean():.2f}, median={qdf[col].median():.1f}")
            dist = dict(Counter(qdf[col]).most_common(10))
            print(f"  Distribution (top 10): {dist}")
            print()


def get_adaptive_thresholds(max_val):
    """Generate threshold values, capped at actual max."""
    candidates = [4, 5, 10, 15, 20]
    thresholds = [n for n in candidates if n <= max_val]
    if max_val not in thresholds and max_val > 0:
        thresholds.append(max_val)
    return sorted(thresholds)


def make_threshold_table(qdf, column, thresholds, split_name):
    """Print table of questions with >= N in column."""
    total = len(qdf)
    rows = []
    for n in thresholds:
        count = (qdf[column] >= n).sum()
        frac = count / total if total > 0 else 0
        rows.append({"N": n, "count": count, "fraction": f"{frac:.4f}", "pct": f"{frac*100:.1f}%"})

    table_df = pd.DataFrame(rows)
    print(f"\nQuestions with >= N {column} ({split_name}):")
    print(table_df.to_string(index=False))
    return table_df


def main():
    print("Loading PlausibleQA dataset...")
    ds = load_plausibleqa()

    print(f"Available splits: {list(ds.keys())}")
    explore_structure(ds)

    qdf, adf, split_name = build_question_df(ds)

    print_examples(qdf, adf, n=3)
    print_basic_stats(qdf, split_name)

    # Threshold tables
    max_total = qdf["total_answers"].max()
    max_incorrect = qdf["n_incorrect"].max()
    max_correct = qdf["n_correct"].max()

    make_threshold_table(qdf, "total_answers", get_adaptive_thresholds(max_total), split_name)
    make_threshold_table(qdf, "n_incorrect", get_adaptive_thresholds(max_incorrect), split_name)
    make_threshold_table(qdf, "n_correct", get_adaptive_thresholds(max_correct), split_name)

    # Plausibility score analysis
    if "plausibility_score" in adf.columns and adf["plausibility_score"].notna().any():
        print(f"\n{'='*80}")
        print("Plausibility Score Distribution")
        print(f"{'='*80}")
        scores = adf["plausibility_score"].dropna()
        print(f"Overall: min={scores.min()}, max={scores.max()}, mean={scores.mean():.1f}, median={scores.median():.1f}")

        correct_scores = adf[adf["is_correct"]]["plausibility_score"].dropna()
        wrong_scores = adf[~adf["is_correct"]]["plausibility_score"].dropna()
        if len(correct_scores) > 0:
            print(f"Correct answers: mean={correct_scores.mean():.1f}, median={correct_scores.median():.1f}")
        if len(wrong_scores) > 0:
            print(f"Wrong answers: mean={wrong_scores.mean():.1f}, median={wrong_scores.median():.1f}")

    print("\n\nDone.")


if __name__ == "__main__":
    main()
