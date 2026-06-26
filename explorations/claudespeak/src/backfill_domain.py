"""Backfill domain/task_type into generated records from their prompt manifest.

The generation scripts saved Claude cells without copying domain/task_type from
the manifest (only the reused cells carried them), leaving a blank ("?") bucket
in the per-domain volume stats. This joins on prompt_id and fills the missing
fields in place. Idempotent: only writes fields that are currently null and only
when the manifest supplies a non-null value. No API calls.
"""
from __future__ import annotations

import json
import os

from schema import REPO, CORPUS_DIR

# (manifest, generated-corpus) pairs to backfill.
PAIRS = [
    ("data/sources/norobots_manifest.jsonl", "norobots_generated.jsonl"),
    # WildChat manifest has no source domain (real user logs are unlabeled),
    # so there is nothing to backfill there.
]


def manifest_map(path):
    m = {}
    with open(os.path.join(REPO, path), encoding="utf-8") as f:
        for line in f:
            if line.strip():
                d = json.loads(line)
                m[d["prompt_id"]] = (d.get("domain"), d.get("task_type"))
    return m


def backfill(manifest_path, corpus_name):
    m = manifest_map(manifest_path)
    corpus = os.path.join(CORPUS_DIR, corpus_name)
    out, n_fixed = [], 0
    with open(corpus, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            dom, tt = m.get(r["prompt_id"], (None, None))
            changed = False
            if r.get("domain") is None and dom is not None:
                r["domain"] = dom; changed = True
            if r.get("task_type") is None and tt is not None:
                r["task_type"] = tt; changed = True
            n_fixed += changed
            out.append(json.dumps(r, ensure_ascii=False))
    with open(corpus, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"{corpus_name}: filled domain/task_type on {n_fixed} records")


if __name__ == "__main__":
    for mani, corp in PAIRS:
        backfill(mani, corp)
