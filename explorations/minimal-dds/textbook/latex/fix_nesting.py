#!/usr/bin/env python3
"""
Fix LaTeX environment nesting issues.
Proofs should come AFTER theorem environments, not inside them.
"""

import re
import sys
from pathlib import Path


def fix_proof_nesting(content):
    """Move proofs outside of theorem environments."""

    theorem_envs = ['proposition', 'theorem', 'lemma', 'corollary', 'definition']

    lines = content.split('\n')
    output = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if we're starting a theorem-like environment
        begin_match = re.match(r'\\begin\{(' + '|'.join(theorem_envs) + r')\}', line)

        if begin_match:
            env_name = begin_match.group(1)
            env_lines = [line]
            proof_lines = []
            in_proof = False
            nesting = 1
            i += 1

            # Collect the environment content
            while i < len(lines) and nesting > 0:
                curr_line = lines[i]

                # Check for nested begins/ends
                if re.search(r'\\begin\{(' + '|'.join(theorem_envs) + r')\}', curr_line):
                    nesting += 1
                if re.search(r'\\end\{(' + '|'.join(theorem_envs) + r')\}', curr_line):
                    nesting -= 1
                    if nesting == 0:
                        # This is the end of our main environment
                        # Output the theorem content (without proof) and end
                        output.extend(env_lines)
                        output.append(curr_line)  # \end{theorem}

                        # Now output any collected proof
                        if proof_lines:
                            output.append('')
                            output.extend(proof_lines)
                        i += 1
                        break

                # Check for proof start
                if curr_line.strip().startswith('\\begin{proof}'):
                    in_proof = True
                    proof_lines.append(curr_line)
                    i += 1
                    continue

                # Check for proof end
                if curr_line.strip().startswith('\\end{proof}'):
                    in_proof = False
                    proof_lines.append(curr_line)
                    i += 1
                    continue

                # Add to appropriate list
                if in_proof:
                    proof_lines.append(curr_line)
                else:
                    env_lines.append(curr_line)

                i += 1
        else:
            output.append(line)
            i += 1

    return '\n'.join(output)


def fix_list_items(content):
    """Convert - items to proper itemize when inside definitions."""
    lines = content.split('\n')
    output = []
    i = 0
    in_definition = False
    list_started = False

    while i < len(lines):
        line = lines[i]

        if '\\begin{definition}' in line:
            in_definition = True
        if '\\end{definition}' in line:
            if list_started:
                output.append('\\end{itemize}')
                list_started = False
            in_definition = False

        if in_definition and line.startswith('- '):
            if not list_started:
                output.append('\\begin{itemize}')
                list_started = True
            output.append('\\item ' + line[2:])
        else:
            if list_started and not line.startswith('- ') and line.strip() != '':
                output.append('\\end{itemize}')
                list_started = False
            output.append(line)

        i += 1

    return '\n'.join(output)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = fix_proof_nesting(content)
    content = fix_list_items(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed nesting in {filepath}")


def main():
    if len(sys.argv) < 2:
        print("Usage: fix_nesting.py file1.tex [file2.tex ...]")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        process_file(filepath)


if __name__ == '__main__':
    main()
