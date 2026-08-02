#!/usr/bin/env bash
# Fetch the CLICS4 database into vendor/clics4 and unzip the tables we use.
#
# CLICS4 is ~390 MB unzipped and is not committed to this repository.
# Run this once per fresh checkout before running anything in src/.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENDOR="$HERE/../vendor"
REPO="$VENDOR/clics4"

mkdir -p "$VENDOR"

if [ -d "$REPO/.git" ]; then
    echo "clics4 already present at $REPO"
else
    echo "Cloning clics4..."
    git clone --depth 1 https://github.com/clics/clics4.git "$REPO"
fi

# forms.csv gives us one row per (language, concept, word form).
# colexifications.csv gives us the aggregated concept-pair graph.
cd "$REPO/cldf"
for f in forms colexifications; do
    if [ -f "$f.csv" ]; then
        echo "$f.csv already unzipped"
    else
        echo "Unzipping $f.csv.zip..."
        unzip -q "$f.csv.zip"
    fi
done

echo "Done. CLICS4 tables are in $REPO/cldf/"
