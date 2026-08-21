# images

A folder for images downloaded from the internet, with their provenance kept
alongside them.

## What is here

| File | What it is |
| --- | --- |
| `pdp-vol1-foundations.jpg` | *Parallel Distributed Processing*, Volume 1: Foundations (Rumelhart, McClelland & the PDP Research Group, MIT Press, 1986). The blue one. |
| `pdp-vol2-psychological-and-biological-models.jpg` | *Parallel Distributed Processing*, Volume 2: Psychological and Biological Models (McClelland, Rumelhart & the PDP Research Group, MIT Press, 1986). The red one. |
| `pdp-vol3-handbook.jpg` | *Explorations in Parallel Distributed Processing: A Handbook of Models, Programs, and Exercises* (McClelland & Rumelhart, MIT Press, 1988) — the third volume of the set. The teal one. |

## How to add more

1. Add a line to `sources.tsv`: `filename<TAB>url<TAB>description`.
2. Run `python3 fetch.py`. Existing files are left alone; use `--force` to
   re-download everything.

`fetch.py` needs nothing but the Python standard library. It writes
`manifest.json`, which records the source URL, sha256, byte size and pixel
dimensions of each file, so an image in this folder can always be traced back
to where it came from.

## Why the fetcher validates instead of just saving the bytes

The first download attempt for this folder wrote a 2 KB "PNG" that was actually
a Wikimedia HTML error page: their thumbnailer only serves a fixed set of widths
and rejected the one requested. A plain `curl -o cover.png` records that
failure as a file which looks correct in a directory listing and only reveals
itself when something tries to decode it.

So `fetch.py` checks twice — the `Content-Type` header must be `image/*`, and
the leading bytes must match a known image signature (JPEG/PNG/GIF/WebP) — and
raises on anything else rather than writing the file. There is no fallback and
no retry-with-a-guess: a failed download is reported and the script exits
nonzero.

## Sources and rights

Cover images come from the [Open Library cover API](https://openlibrary.org/dev/docs/api/covers),
keyed by ISBN. Note the `?default=false` query parameter in `sources.tsv`:
without it, a missing cover returns a blank placeholder image with a success
status instead of a 404, which is exactly the silent-failure mode the validation
above exists to prevent.

Book covers are the property of their publishers and are kept here for
reference and study, not for redistribution.
