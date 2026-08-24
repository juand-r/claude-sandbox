# images

A folder for images downloaded from the internet, with their provenance kept
alongside them.

## What is here

| File | What it is |
| --- | --- |
| `pdp-vol1-foundations.jpg` | *Parallel Distributed Processing*, Volume 1: Foundations (Rumelhart, McClelland & the PDP Research Group, MIT Press, 1986). The blue one. |
| `pdp-vol2-psychological-and-biological-models.jpg` | *Parallel Distributed Processing*, Volume 2: Psychological and Biological Models (McClelland, Rumelhart & the PDP Research Group, MIT Press, 1986). The red one. |
| `pdp-vol3-handbook.jpg` | *Explorations in Parallel Distributed Processing: A Handbook of Models, Programs, and Exercises* (McClelland & Rumelhart, MIT Press, 1988) — the third volume of the set. The teal one. |
| `perceptrons-1969.jpg` | *Perceptrons: An Introduction to Computational Geometry* (Minsky & Papert, MIT Press, 1969), original edition. Red cover, two purple spirals. |
| `perceptrons-1988-expanded.jpg` | *Perceptrons*, Expanded Edition (1988). Green cover, nested red squares. |
| `perceptrons-2017-reissue.jpg` | *Perceptrons*, 2017 reissue of the expanded edition, with a foreword by Léon Bottou. Orange cover, spirals redrawn. |

### `pluribus/` — Pluribus (Apple TV+, 2025)

| File | What it is |
| --- | --- |
| `key-art-poster-2x3.png` | Official key art, 2000x3000 — the yellow poster with Carol mid-scream. |
| `key-art-16x9.png` | The same key art in 16:9, 3840x2160. |
| `key-art-header-4x1.jpg` | Key art cropped to the 4:1 banner Apple uses on the press page, 2364x688. |
| `still-carol-yellow-jacket-closeup.jpg` | Screen still, 3840x2160: Carol Sturka (Rhea Seehorn) in close-up. |
| `still-carol-yellow-jacket-dark.jpg` | Screen still, 3840x2160: Carol lit against black, looking up. |
| `bts-gilligan-on-set.jpg` | Behind the scenes, 3840x2160: Vince Gilligan on a night shoot. |
| `bts-gilligan-seehorn-interview.jpg` | Behind the scenes, 3840x2160: Gilligan and Seehorn, featurette interview. |
| `logo.svg` | The Pluribus logotype, vector. |
| `rhea-seehorn-qa.jpg` | Rhea Seehorn at a Pluribus Q&A, 1600x2000. |

Only two of these are committed to the repository: `logo.svg` (public domain)
and `rhea-seehorn-qa.jpg` (CC BY 4.0, photo by Kevin Paul). The rest are in
`.gitignore` and are fetched on demand — see the rights note at the end.

The two `still-` files are the cover frames of the *Happiness* and *Join Us*
trailers, and the two `bts-` files come from the *From Every Angle* and *What
on Earth Is Pluribus?* featurettes. Apple's press site publishes no episodic
stills for this show; these frames, pulled at 3840x2160 from the Apple TV
storefront's artwork CDN, are the highest-resolution imagery available without
screen-grabbing the episodes yourself.

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

Pluribus key art comes from [Apple's press site](https://www.apple.com/tv-pr/originals/pluribus/),
which distributes it as a zip; `fetch.py` supports a `url#member` syntax for
pulling one file out of an archive. The 4K frames come from the Apple TV
storefront's artwork CDN, whose URLs carry a `{w}x{h}` size template that
`sources.tsv` fills in with the maximum available dimensions. The logotype and
the Seehorn photograph come from Wikimedia Commons.

Book covers are the property of their publishers and are kept here for
reference and study, not for redistribution.

The Apple material is more constrained: the press kit ships a legal notice
limiting use to "personal or editorial and non-commercial" and forbidding
modification. Because this repository is public and MIT-licensed, committing
those files would amount to redistributing them under a licence Apple has not
granted, so they are listed in `.gitignore` and pulled down by `fetch.py`
instead. This is a judgement call rather than legal advice; if you would rather
have the files in git, delete those three lines from `.gitignore` and commit
them.
