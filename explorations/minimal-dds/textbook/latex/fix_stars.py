#!/usr/bin/env python3
"""Fix incorrectly converted asterisks in math mode."""

import re
import sys


def fix_stars(content):
    """Fix patterns like $\Sigma^\textit{$ to $\Sigma^*$."""

    # Pattern 1: $...\textit{$ is the }something*
    # These are split math/text caused by * being treated as markdown italic
    # Find and fix patterns like: $...\textit{$ ... }something*
    content = re.sub(
        r'\$([^$]*)\^\textit\{\$\s+is the\s+\}([^*]+)\*',
        r'$\1^*$ is the \\textit{\2}',
        content
    )

    # Pattern 2: $...\textit{...}$ for incorrectly italicized math
    # Fix $w \vdash_T^\textit{ w'$ for...}orbit* pattern
    content = re.sub(
        r'\$([^$]*)\^\textit\{\s+([^$]+)\$\s+for the reflexive-transitive closure\.\s+The\s+\}orbit\*',
        r'$\1^* \2$ for the reflexive-transitive closure. The \\textit{orbit}',
        content
    )

    # Pattern 3: Generic fix for ^textit{ followed by $ and closing }...*
    # Try a more aggressive pattern matching
    lines = content.split('\n')
    fixed_lines = []

    for line in lines:
        # Fix the specific broken pattern in tag_systems
        if '\\textit{$' in line and '}' in line and '*' in line:
            # Try to reconstruct: $X^\textit{$ text }word* -> $X^*$ text \textit{word}
            match = re.search(r'\$([^$]+)\^\textit\{\$([^}]+)\}(\w+)\*', line)
            if match:
                line = line.replace(
                    match.group(0),
                    f'${match.group(1)}^*${match.group(2)}\\textit{{{match.group(3)}}}'
                )
        fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def main():
    for filepath in sys.argv[1:]:
        print(f"Processing {filepath}")
        with open(filepath, 'r') as f:
            content = f.read()

        content = fix_stars(content)

        with open(filepath, 'w') as f:
            f.write(content)


if __name__ == '__main__':
    main()
