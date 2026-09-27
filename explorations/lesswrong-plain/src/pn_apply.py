"""Insert plain paragraph notes into annotated/posts/<slug>.tex.

Usage: python pn_apply.py <posts_dir> <notes_dir> <slug> [--dry]
Notes file <notes_dir>/<slug>.json: {"<block id>": "note text in LaTeX", ...}
Every id must be a current target (see pn_extract.py); every target must have a note.
Fails loudly on any check; writes nothing unless all notes pass.
"""
import json, os, re, sys
from pn_extract import targets

BANNED = ['load-bearing', 'it is worth noting', "here's the thing", 'smoking gun', 'real gap',
          'notably', 'importantly', 'crucially', 'delve', 'underscores', 'doing a lot of work']


def check(note, item):
    errs = []
    w = len(note.split())
    if w >= item['words']: errs.append(f'note {w}w not shorter than paragraph {item["words"]}w')
    if w > 40: errs.append(f'note {w}w over 40')
    if '—' in note or '---' in note: errs.append('em dash')
    if re.search(r'\\(emph|textit|it)\b', note): errs.append('italics')
    if '"' in note: errs.append('straight double quote; use ``...\'\'')
    if re.search(r'(?<!\\)[%&#_$]', note): errs.append('unescaped special char')
    if note.count('{') != note.count('}'): errs.append('unbalanced braces')
    low = note.lower()
    errs += [f'banned: {b}' for b in BANNED if b in low]
    return errs


def insert_at(block, note):
    """Prepend to prose; inside a quote, after \\begin{quote}; inside a list, after the first \\item."""
    lead = len(block) - len(block.lstrip())
    rest = block[lead:]
    tok = next((t for t in ('\\begin{quote}', '\\begin{quotation}') if rest.startswith(t)), None)
    if tok is None and re.match(r'\\begin\{(itemize|enumerate)\}', rest):
        tok = '\\item'
    if tok is None:
        return block[:lead] + '\\cpara{' + note + '}' + rest
    p = lead + block[lead:].index(tok) + len(tok)
    return block[:p] + ' \\cpara{' + note + '}' + block[p:].lstrip(' ')


if __name__ == '__main__':
    posts, notes_dir, slug = sys.argv[1:4]
    dry = '--dry' in sys.argv
    path = os.path.join(posts, slug + '.tex')
    head, body = open(path).read().split('\n', 1)
    items = {str(t['id']): t for t in targets(body)}
    notes = json.load(open(os.path.join(notes_dir, slug + '.json')))
    missing, extra = set(items) - set(notes), set(notes) - set(items)
    if missing or extra: raise SystemExit(f'{slug}: missing {sorted(missing)} extra {sorted(extra)}')
    bad = {i: e for i, n in notes.items() if (e := check(n, items[i]))}
    if bad:
        for i, e in bad.items(): print(slug, i, e)
        raise SystemExit(1)
    blocks = body.split('\\flushnotes')
    for i, n in notes.items(): blocks[int(i)] = insert_at(blocks[int(i)], n)
    if not dry: open(path, 'w').write(head + '\n' + '\\flushnotes'.join(blocks))
    print(slug, 'ok', len(notes), '(dry)' if dry else '')
