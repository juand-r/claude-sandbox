#!/usr/bin/env python3
"""Fix unmatched proof environments."""

import re
import sys


def fix_proofs(content):
    """Remove stray \end{proof} tags and ensure matching."""
    lines = content.split('\n')
    output = []
    proof_depth = 0

    for i, line in enumerate(lines):
        # Count proof opens
        if '\\begin{proof}' in line:
            proof_depth += 1
            output.append(line)
        elif '\\end{proof}' in line:
            if proof_depth > 0:
                proof_depth -= 1
                output.append(line)
            else:
                # Stray \end{proof}, skip it
                print(f"  Removed stray \\end{{proof}} at line {i+1}")
        else:
            output.append(line)

    return '\n'.join(output)


def main():
    for filepath in sys.argv[1:]:
        print(f"Processing {filepath}")
        with open(filepath, 'r') as f:
            content = f.read()

        content = fix_proofs(content)

        with open(filepath, 'w') as f:
            f.write(content)


if __name__ == '__main__':
    main()
