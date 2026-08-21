#!/usr/bin/env python3
"""Download the images listed in sources.tsv into this directory.

Why a script instead of plain curl: an image URL that fails often still returns
HTTP 200-looking content (an HTML error page, a placeholder), and writing that
to `cover.jpg` produces a file that only looks fine until you open it. So every
download here is checked twice -- the Content-Type header must be image/*, and
the first bytes must match a known image signature -- and anything else is a
hard error, not a warning.

Usage:
    python3 fetch.py            # fetch anything missing
    python3 fetch.py --force    # re-fetch everything, overwriting

Output: the image files themselves, plus manifest.json recording where each one
came from (url, sha256, size, pixel dimensions) so provenance is not lost.
"""

import argparse
import hashlib
import json
import struct
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = HERE / "sources.tsv"
MANIFEST = HERE / "manifest.json"

# Some hosts reject the default urllib agent outright.
USER_AGENT = "claude-sandbox-image-fetcher/1.0 (+https://github.com/juand-r/claude-sandbox)"
TIMEOUT_SECONDS = 60

# First bytes -> format name. Used to confirm the payload really is an image.
MAGIC = {
    b"\xff\xd8\xff": "jpeg",
    b"\x89PNG\r\n\x1a\n": "png",
    b"GIF87a": "gif",
    b"GIF89a": "gif",
    b"RIFF": "webp",  # bytes 8:12 are checked separately below
}


def read_sources(path):
    """Parse sources.tsv -> list of (filename, url, description).

    Format: three tab-separated columns. Blank lines and lines starting with #
    are ignored.
    """
    entries = []
    for lineno, raw in enumerate(path.read_text().splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            raise ValueError(
                f"{path.name}:{lineno}: expected 3 tab-separated columns, got {len(parts)}: {raw!r}"
            )
        entries.append(tuple(p.strip() for p in parts))
    return entries


def sniff_format(data):
    """Return the image format implied by the leading bytes, or None."""
    for magic, name in MAGIC.items():
        if data.startswith(magic):
            if name == "webp" and data[8:12] != b"WEBP":
                continue
            return name
    return None


def image_size(data, fmt):
    """Return (width, height) for a PNG or JPEG, or None for other formats.

    Only the two formats we actually download are parsed; anything else returns
    None rather than guessing.
    """
    if fmt == "png":
        # IHDR is always the first chunk: width and height are big-endian uint32.
        return struct.unpack(">II", data[16:24])
    if fmt == "jpeg":
        # Walk the marker segments until a start-of-frame (SOFn) carries the size.
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                return None
            marker = data[i + 1]
            length = struct.unpack(">H", data[i + 2:i + 4])[0]
            # SOFn markers, excluding DHT/JPGA/DAC which share the 0xC0 range.
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                height, width = struct.unpack(">HH", data[i + 5:i + 9])
                return width, height
            i += 2 + length
        return None
    return None


def download(url):
    """Fetch url and return (bytes, format). Raises on anything that is not an image."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        content_type = (response.headers.get("Content-Type") or "").split(";")[0].strip()
        data = response.read()

    if not content_type.startswith("image/"):
        raise ValueError(
            f"expected an image, server sent Content-Type {content_type!r} "
            f"({len(data)} bytes). First bytes: {data[:80]!r}"
        )
    fmt = sniff_format(data)
    if fmt is None:
        raise ValueError(
            f"Content-Type said {content_type!r} but the bytes are not a known "
            f"image format. First bytes: {data[:80]!r}"
        )
    return data, fmt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="re-download files that already exist")
    args = parser.parse_args()

    entries = read_sources(SOURCES)
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    failures = []

    for filename, url, description in entries:
        target = HERE / filename
        if target.exists() and not args.force:
            print(f"skip     {filename} (already present)")
            continue
        try:
            data, fmt = download(url)
        except Exception as exc:  # report every failure, keep going, exit nonzero
            print(f"FAILED   {filename}: {exc}", file=sys.stderr)
            failures.append(filename)
            continue

        target.write_bytes(data)
        size = image_size(data, fmt)
        manifest[filename] = {
            "url": url,
            "description": description,
            "format": fmt,
            "bytes": len(data),
            "width": size[0] if size else None,
            "height": size[1] if size else None,
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        dims = f"{size[0]}x{size[1]}" if size else "?"
        print(f"fetched  {filename}  {fmt} {dims} {len(data)} bytes")

    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    if failures:
        print(f"\n{len(failures)} download(s) failed: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
