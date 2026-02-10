#!/usr/bin/env python3
"""Post-process converted LaTeX files to fix common issues."""

import re
import sys
from pathlib import Path


def fix_italics_in_text(text):
    """Fix remaining *text* to \textit{text}."""
    # Only convert *text* that's not already inside math mode
    # Simple approach: convert remaining single asterisk pairs
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'\\textit{\1}', text)
    return text


def fix_proof_endings(text):
    """Ensure proofs end properly."""
    # Remove $\square$ that wasn't converted
    text = text.replace('$\\square$', '')
    return text


def fix_nested_environments(text):
    """Fix environments that got nested incorrectly."""
    lines = text.split('\n')
    output = []
    env_stack = []

    for line in lines:
        # Track environment starts
        begin_match = re.search(r'\\begin\{(\w+)\}', line)
        if begin_match:
            env_stack.append(begin_match.group(1))

        # Track environment ends
        end_match = re.search(r'\\end\{(\w+)\}', line)
        if end_match:
            if env_stack and env_stack[-1] == end_match.group(1):
                env_stack.pop()

        output.append(line)

    return '\n'.join(output)


def fix_double_backslash_braces(text):
    """Ensure \{ and \} are correct."""
    # Replace \lbrace and \rbrace if still present
    text = text.replace('\\lbrace', '\\{')
    text = text.replace('\\rbrace', '\\}')
    return text


def fix_bold_steps(text):
    """Convert **Step N:** to \textbf{Step N:}"""
    text = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', text)
    return text


def add_missing_end_envs(text):
    """Add missing \end{} tags."""
    lines = text.split('\n')
    output = []
    open_envs = []

    theorem_envs = ['definition', 'theorem', 'proposition', 'lemma', 'corollary',
                    'example', 'remark', 'observation', 'conjecture', 'question',
                    'algorithm_env', 'proof']

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for begin
        begin_match = re.search(r'\\begin\{(\w+)\}', line)
        if begin_match:
            env = begin_match.group(1)
            if env in theorem_envs:
                # Close any previous theorem env of same type or different
                if open_envs and open_envs[-1] in theorem_envs and open_envs[-1] != 'proof':
                    # Check if this line starts a new env - need to close previous
                    if env != 'proof':  # Don't close for proof start
                        output.append(f'\\end{{{open_envs[-1]}}}')
                        output.append('')
                        open_envs.pop()
                open_envs.append(env)

        # Check for end
        end_match = re.search(r'\\end\{(\w+)\}', line)
        if end_match:
            env = end_match.group(1)
            if env in open_envs:
                # Pop until we find this env
                while open_envs and open_envs[-1] != env:
                    output.append(f'\\end{{{open_envs.pop()}}}')
                if open_envs:
                    open_envs.pop()

        # Check for section start - close any open theorem envs
        if line.startswith('\\section{') or line.startswith('\\subsection'):
            while open_envs and open_envs[-1] in theorem_envs:
                output.append(f'\\end{{{open_envs.pop()}}}')
                output.append('')

        output.append(line)
        i += 1

    # Close any remaining envs
    while open_envs:
        output.append(f'\\end{{{open_envs.pop()}}}')

    return '\n'.join(output)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = fix_italics_in_text(content)
    content = fix_proof_endings(content)
    content = fix_double_backslash_braces(content)
    content = fix_bold_steps(content)
    content = add_missing_end_envs(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed {filepath}")


def main():
    if len(sys.argv) < 2:
        print("Usage: fix_tex.py file1.tex [file2.tex ...]")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        process_file(filepath)


if __name__ == '__main__':
    main()
