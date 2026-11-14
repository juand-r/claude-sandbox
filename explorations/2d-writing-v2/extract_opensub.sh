#!/bin/bash
# Extract short complete sentences from the OpenSubtitles 2018 English file
# (https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/mono/en.txt.gz).
#
# A line is kept if it starts with a capital letter, consists only of letters,
# apostrophes, spaces and commas, ends in one of . ? !, and has 2 to 7 words.
# Output lines: "<count> <lowercase words>\t<final punctuation>", one per
# distinct (sentence, punctuation) pair, written to data/opensub_short_counts.txt.
set -euo pipefail
cd "$(dirname "$0")"
export LC_ALL=C
zcat data/opensub_en.txt.gz \
  | grep -E "^[A-Z][A-Za-z' ,]*[.?!]$" \
  | awk 'NF >= 2 && NF <= 7' \
  | tr -d ',' | tr 'A-Z' 'a-z' \
  | sed -E 's/ +/ /g; s/(.)$/\t\1/' \
  | sort -S 5G --parallel=3 -T data \
  | uniq -c > data/opensub_short_counts.txt
wc -l data/opensub_short_counts.txt
