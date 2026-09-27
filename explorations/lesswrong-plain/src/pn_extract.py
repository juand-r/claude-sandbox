"""List paragraphs in annotated/posts/<slug>.tex that lack a \\cpara note.

Usage: python pn_extract.py <posts_dir> <out_dir>
Writes <out_dir>/<slug>.json: [{"id": block_index, "kind", "words", "text"}, ...]
Block index = position in body.split('\\flushnotes'); pn_apply.py uses the same split.
"""
import json, os, re, sys

NOTE_CMDS = ('clogic', 'cstyle', 'cfact', 'ccut', 'cauthor', 'cpara')
MIN_PROSE, MIN_BLOCK = 15, 30


def strip_notes(s):
    """Remove \\c<kind>{...} note commands (brace-matched)."""
    out, i = [], 0
    while i < len(s):
        m = re.match(r'\\(%s)\{' % '|'.join(NOTE_CMDS), s[i:])
        if not m:
            out.append(s[i]); i += 1; continue
        depth, j = 1, i + m.end()
        while depth:
            depth += {'{': 1, '}': -1}.get(s[j], 0); j += 1
        i = j
    return ''.join(out)


def plain(s):
    s = strip_notes(s)
    s = re.sub(r'\\href\{[^}]*\}', '', s)
    s = re.sub(r'\\(begin|end)\{[a-z]+\}|\\item\b', ' ', s)
    s = re.sub(r'\\[a-zA-Z]+\*?', '', s)
    s = s.replace('{', '').replace('}', '').replace('``', '"').replace("''", '"')
    return re.sub(r'\s+', ' ', s).strip()


def kind(b):
    if re.match(r'\\(sub)*section|\\textbf\{[^}]*\}\s*$|\{\\bf', b): return 'heading'
    if b.startswith('\\figph') or b.startswith('\\img'): return 'image'
    if b.startswith('\\begin{quote') : return 'quote'
    if re.match(r'\\begin\{(itemize|enumerate)\}|\\item', b): return 'list'
    if b.startswith('\\['): return 'math'
    return 'prose'


def targets(body):
    for i, b in enumerate(body.split('\\flushnotes')):
        b = b.strip()
        if not b or '\\cpara' in b: continue
        k = kind(b); t = plain(b); w = len(t.split())
        if (k == 'prose' and w >= MIN_PROSE) or (k in ('quote', 'list') and w >= MIN_BLOCK):
            yield {'id': i, 'kind': k, 'words': w, 'text': t}


if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    total = 0
    for f in sorted(os.listdir(src)):
        if not f.endswith('.tex'): continue
        body = open(os.path.join(src, f)).read().split('\n', 1)[1]
        items = list(targets(body)); total += len(items)
        json.dump(items, open(os.path.join(out, f[:-4] + '.json'), 'w'), indent=1, ensure_ascii=False)
    print('targets', total)
