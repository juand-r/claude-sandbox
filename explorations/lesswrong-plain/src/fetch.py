"""Fetch post lists and post texts from the public LessWrong GraphQL API.

Usage:
    python src/fetch.py manifests          # write data/manifests/*.json (metadata only)
    python src/fetch.py posts highlights   # fetch every post in a manifest to data/originals/
    python src/fetch.py post <post_id>     # fetch one post

Originals are saved as Markdown with a small header. They are not committed to git
(see .gitignore): they are the authors' copyrighted text and can be re-fetched any time.
"""

import json
import sys
import time
from pathlib import Path

import requests
from markdownify import markdownify

API_URL = "https://www.lesswrong.com/graphql"
SITE_URL = "https://www.lesswrong.com"
HIGHLIGHTS_COLLECTION_ID = "62bf5f5dc581cd211cc67d49"  # "Highlights from the Sequences"
RAZ_COLLECTION_ID = "oneQyj4pw77ynzwAF"  # "Rationality: A-Z" (slug "rationality")
REQUEST_TIMEOUT_S = 120
PAUSE_BETWEEN_POSTS_S = 1.0  # be polite to the server

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = ROOT / "data" / "manifests"
ORIGINALS_DIR = ROOT / "data" / "originals"

POST_FIELDS = "_id title slug baseScore wordCount postedAt user { displayName }"


def graphql(query: str) -> dict:
    """Run a GraphQL query. Raises on HTTP errors and on GraphQL errors."""
    resp = requests.post(API_URL, json={"query": query}, timeout=REQUEST_TIMEOUT_S)
    resp.raise_for_status()
    body = resp.json()
    if "errors" in body:
        raise RuntimeError(f"GraphQL error: {body['errors'][0]['message']}")
    return body["data"]


def post_record(p: dict, **extra) -> dict:
    """Flatten an API post object into a manifest entry."""
    return {
        "id": p["_id"],
        "title": p["title"],
        "slug": p["slug"],
        "author": p["user"]["displayName"] if p["user"] else None,
        "posted_at": p["postedAt"],
        "karma": p["baseScore"],
        "word_count": p["wordCount"],
        "url": f"{SITE_URL}/posts/{p['_id']}/{p['slug']}",
        **extra,
    }


def highlights_manifest() -> list[dict]:
    """The 50 posts of 'Highlights from the Sequences', in reading order."""
    q = f"""{{ collection(input:{{selector:{{_id:"{HIGHLIGHTS_COLLECTION_ID}"}}}}) {{
        result {{ books {{ title sequences {{ title chapters {{ posts {{ {POST_FIELDS} }} }} }} }} }} }} }}"""
    books = graphql(q)["collection"]["result"]["books"]
    main_book = books[0]  # books[1] is "Further Reading", not part of the 50 highlights
    entries = []
    for seq in main_book["sequences"]:
        for chapter in seq["chapters"]:
            for p in chapter["posts"]:
                entries.append(post_record(p, section=seq["title"], order=len(entries) + 1))
    return entries


def rationality_az_manifest() -> list[dict]:
    """All posts of "Rationality: A-Z", in reading order, with book and sequence titles."""
    q = f"""{{ collection(input:{{selector:{{_id:"{RAZ_COLLECTION_ID}"}}}}) {{
        result {{ books {{ title sequences {{ title chapters {{ posts {{ {POST_FIELDS} }} }} }} }} }} }} }}"""
    entries = []
    for book in graphql(q)["collection"]["result"]["books"]:
        for seq in book["sequences"]:
            for chapter in seq["chapters"]:
                for p in chapter["posts"]:
                    entries.append(post_record(p, book=book["title"], section=seq["title"],
                                               order=len(entries) + 1))
    return entries


def review_winners_manifest() -> list[dict]:
    """All Annual Review winners, sorted by year then by rank (rank 0 = top)."""
    q = f"""{{ GetAllReviewWinners {{ {POST_FIELDS}
        reviewWinner {{ reviewYear reviewRanking category }} }} }}"""
    posts = graphql(q)["GetAllReviewWinners"]
    entries = [
        post_record(
            p,
            review_year=p["reviewWinner"]["reviewYear"],
            review_rank=p["reviewWinner"]["reviewRanking"],
            category=p["reviewWinner"]["category"],
        )
        for p in posts
    ]
    return sorted(entries, key=lambda e: (e["review_year"], e["review_rank"]))


def write_manifests() -> None:
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    for name, build in [("highlights", highlights_manifest), ("review_winners", review_winners_manifest),
                        ("rationality_az", rationality_az_manifest)]:
        entries = build()
        path = MANIFEST_DIR / f"{name}.json"
        path.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
        words = sum(e["word_count"] or 0 for e in entries)
        print(f"{path.relative_to(ROOT)}: {len(entries)} posts, {words} words")


def fetch_post(post_id: str) -> Path:
    """Fetch one post's HTML, convert to Markdown, save with a header. Returns the path."""
    q = f"""{{ post(input:{{selector:{{_id:"{post_id}"}}}}) {{
        result {{ {POST_FIELDS} contents {{ html }} }} }} }}"""
    p = graphql(q)["post"]["result"]
    if p is None or p["contents"] is None:
        raise RuntimeError(f"No content returned for post {post_id}")
    rec = post_record(p)
    body = markdownify(p["contents"]["html"], heading_style="ATX")
    header = (
        f"# {rec['title']}\n\n"
        f"Author: {rec['author']}  \nPosted: {rec['posted_at'][:10]}  \n"
        f"Source: {rec['url']}\n\n---\n\n"
    )
    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
    path = ORIGINALS_DIR / f"{rec['slug']}.md"
    path.write_text(header + body)
    return path


def fetch_manifest_posts(manifest_name: str) -> None:
    entries = json.loads((MANIFEST_DIR / f"{manifest_name}.json").read_text())
    for e in entries:
        path = fetch_post(e["id"])
        print(f"saved {path.relative_to(ROOT)}")
        time.sleep(PAUSE_BETWEEN_POSTS_S)


def main(argv: list[str]) -> None:
    if argv[:1] == ["manifests"]:
        write_manifests()
    elif argv[:1] == ["posts"] and len(argv) == 2:
        fetch_manifest_posts(argv[1])
    elif argv[:1] == ["post"] and len(argv) == 2:
        print(fetch_post(argv[1]).relative_to(ROOT))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
