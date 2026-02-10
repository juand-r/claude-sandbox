#!/usr/bin/env python3
"""Escape ampersands in text but not in tables."""

import re
import sys


def escape_ampersands(content):
    """Escape & characters that are outside of tabular environments."""
    lines = content.split('\n')
    output = []
    in_tabular = False

    for line in lines:
        if '\\begin{tabular}' in line or '\\begin{center}' in line:
            in_tabular = True
        if '\\end{tabular}' in line or '\\end{center}' in line:
            in_tabular = False
            output.append(line)
            continue

        if not in_tabular:
            # Escape & that are in text (not already escaped)
            # Look for patterns like "Foo & Bar" but not "\&" or "& " in tables
            line = re.sub(r'(?<!\\)(\s)&(\s)', r'\1\\&\2', line)

        output.append(line)

    return '\n'.join(output)


def main():
    for filepath in sys.argv[1:]:
        with open(filepath, 'r') as f:
            content = f.read()

        content = escape_ampersands(content)

        with open(filepath, 'w') as f:
            f.write(content)

        print(f"Escaped ampersands in {filepath}")


if __name__ == '__main__':
    main()
