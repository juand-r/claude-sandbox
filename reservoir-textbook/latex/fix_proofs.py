#!/usr/bin/env python3
"""Post-process .tex files to fix proof environment balance."""
import re
import os

def fix_proofs(tex_text):
    """Ensure every \\begin{proof} has a matching \\end{proof}."""
    lines = tex_text.split('\n')
    result = []
    proof_depth = 0

    for i, line in enumerate(lines):
        # Check if this line starts a new environment that should close any open proof
        if proof_depth > 0:
            # Close proof before new theorem-like envs, sections, chapters
            if re.match(r'\\(begin\{(theorem|definition|proposition|lemma|corollary|example|exercise|remark)\}|section|subsection|chapter|part\b|end\{document\})', line.strip()):
                while proof_depth > 0:
                    result.append('\\end{proof}')
                    result.append('')
                    proof_depth -= 1

        if '\\begin{proof}' in line:
            proof_depth += 1
        if '\\end{proof}' in line:
            proof_depth = max(0, proof_depth - 1)

        result.append(line)

    # Close any remaining open proofs at end of file
    while proof_depth > 0:
        result.append('\\end{proof}')
        proof_depth -= 1

    return '\n'.join(result)


def main():
    latex_dir = '/home/user/claude-sandbox/reservoir-textbook/latex'
    for ch in range(1, 18):
        fname = f'chapter{ch:02d}.tex'
        path = os.path.join(latex_dir, fname)
        with open(path, 'r') as f:
            text = f.read()

        begins = len(re.findall(r'\\begin\{proof\}', text))
        ends = len(re.findall(r'\\end\{proof\}', text))

        if begins != ends:
            fixed = fix_proofs(text)
            new_begins = len(re.findall(r'\\begin\{proof\}', fixed))
            new_ends = len(re.findall(r'\\end\{proof\}', fixed))
            with open(path, 'w') as f:
                f.write(fixed)
            print(f'{fname}: {begins}b/{ends}e -> {new_begins}b/{new_ends}e')
        else:
            print(f'{fname}: OK ({begins})')


if __name__ == '__main__':
    main()
