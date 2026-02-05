"""
MultiRC dataset analysis.

MultiRC (Multi-Sentence Reading Comprehension) from SuperGLUE.
Each row is a (passage, question, answer_option, label) tuple.
label=1 means the answer is correct, label=0 means incorrect.
Multiple answer options per question; multiple correct answers possible.

We group by (paragraph_idx, question_idx) to get per-question stats.
"""

from datasets import load_dataset
import pandas as pd
from collections import Counter


def load_multirc():
    """Load MultiRC from super_glue. Returns dict of splits."""
    ds = load_dataset("super_glue", "multirc")
    return ds


def dataset_to_df(split):
    """Convert a HF dataset split to a DataFrame with flattened idx."""
    records = []
    for row in split:
        records.append({
            "paragraph_idx": row["idx"]["paragraph"],
            "question_idx": row["idx"]["question"],
            "answer_idx": row["idx"]["answer"],
            "paragraph": row["paragraph"],
            "question": row["question"],
            "answer": row["answer"],
            "label": row["label"],
        })
    return pd.DataFrame(records)


def print_examples(df, n=3):
    """Print n example questions with all their answer options."""
    # Get n unique (paragraph_idx, question_idx) pairs
    question_keys = df.groupby(["paragraph_idx", "question_idx"]).size().index[:n]

    for i, (p_idx, q_idx) in enumerate(question_keys):
        group = df[(df["paragraph_idx"] == p_idx) & (df["question_idx"] == q_idx)]
        row = group.iloc[0]
        print(f"\n{'='*80}")
        print(f"Example {i+1} (paragraph={p_idx}, question={q_idx})")
        print(f"{'='*80}")
        print(f"Passage (first 300 chars): {row['paragraph'][:300]}...")
        print(f"\nQuestion: {row['question']}")
        print(f"\nAnswers ({len(group)} total):")
        for _, a in group.iterrows():
            label_str = "CORRECT" if a["label"] == 1 else "WRONG"
            print(f"  [{label_str}] {a['answer']}")


def compute_question_stats(df):
    """
    Group by question, compute per-question counts.
    Returns a DataFrame with one row per question.
    """
    grouped = df.groupby(["paragraph_idx", "question_idx"])
    stats = grouped.agg(
        total_answers=("label", "count"),
        correct_answers=("label", "sum"),
    ).reset_index()
    stats["incorrect_answers"] = stats["total_answers"] - stats["correct_answers"]
    return stats


def print_basic_stats(qstats, split_name):
    """Print basic statistics about the questions."""
    print(f"\n{'='*80}")
    print(f"Basic Stats: {split_name}")
    print(f"{'='*80}")
    print(f"Number of questions: {len(qstats)}")
    print(f"Number of unique passages: {qstats['paragraph_idx'].nunique()}")
    print()

    for col, label in [
        ("total_answers", "Total answers per question"),
        ("correct_answers", "Correct answers per question"),
        ("incorrect_answers", "Incorrect answers per question"),
    ]:
        print(f"{label}:")
        print(f"  min={qstats[col].min()}, max={qstats[col].max()}, "
              f"mean={qstats[col].mean():.2f}, median={qstats[col].median():.1f}")
        print(f"  Distribution: {dict(Counter(qstats[col]).most_common(10))}")
        print()


def make_threshold_table(qstats, column, thresholds, split_name):
    """
    For each threshold N, compute how many questions have >= N in `column`.
    Prints a formatted table.
    """
    total = len(qstats)
    rows = []
    for n in thresholds:
        count = (qstats[column] >= n).sum()
        frac = count / total if total > 0 else 0
        rows.append({"N": n, "count": count, "fraction": f"{frac:.4f}", "pct": f"{frac*100:.1f}%"})

    table_df = pd.DataFrame(rows)
    print(f"\nQuestions with >= N {column} ({split_name}):")
    print(table_df.to_string(index=False))
    return table_df


def get_adaptive_thresholds(max_val):
    """
    Generate threshold values: use {4, 5, 10, 15, 20} but cap at actual max.
    """
    candidates = [4, 5, 10, 15, 20]
    thresholds = [n for n in candidates if n <= max_val]
    # Always include the max if it's not already there
    if max_val not in thresholds and max_val > 0:
        thresholds.append(max_val)
    return sorted(thresholds)


def analyze_split(df, split_name):
    """Full analysis for one split."""
    print(f"\n{'#'*80}")
    print(f"# {split_name.upper()}")
    print(f"{'#'*80}")
    print(f"Total rows (answer options): {len(df)}")

    print_examples(df, n=3)

    qstats = compute_question_stats(df)
    print_basic_stats(qstats, split_name)

    # Determine adaptive thresholds
    max_total = qstats["total_answers"].max()
    max_incorrect = qstats["incorrect_answers"].max()

    total_thresholds = get_adaptive_thresholds(max_total)
    incorrect_thresholds = get_adaptive_thresholds(max_incorrect)

    make_threshold_table(qstats, "total_answers", total_thresholds, split_name)
    make_threshold_table(qstats, "incorrect_answers", incorrect_thresholds, split_name)
    make_threshold_table(qstats, "correct_answers", get_adaptive_thresholds(qstats["correct_answers"].max()), split_name)

    return qstats


def main():
    print("Loading MultiRC dataset...")
    ds = load_multirc()

    results = {}
    for split_name in ["train", "validation"]:
        if split_name in ds:
            df = dataset_to_df(ds[split_name])
            qstats = analyze_split(df, split_name)
            results[split_name] = qstats

    # test split usually has label=-1 (hidden), check if usable
    if "test" in ds:
        df_test = dataset_to_df(ds["test"])
        if (df_test["label"] >= 0).all():
            analyze_split(df_test, "test")
        else:
            print(f"\nTest split has hidden labels (label=-1), skipping analysis.")
            print(f"Test split rows: {len(df_test)}")

    print("\n\nDone.")


if __name__ == "__main__":
    main()
