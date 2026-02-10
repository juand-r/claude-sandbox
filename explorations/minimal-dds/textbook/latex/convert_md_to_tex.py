#!/usr/bin/env python3
"""
Convert markdown chapter files to LaTeX.
This handles the specific formatting used in the minimal-dds textbook.
"""

import re
import sys
from pathlib import Path


def convert_inline_math(text):
    """Convert $...$ to LaTeX inline math (already compatible)."""
    return text


def convert_display_math(text):
    """Convert $$...$$ to \[...\]"""
    # Handle multi-line display math
    text = re.sub(r'\$\$(.*?)\$\$', r'\\[\1\\]', text, flags=re.DOTALL)
    return text


def convert_bold_italic(text):
    """Convert markdown bold/italic to LaTeX."""
    # Bold: **text** -> \textbf{text}
    text = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', text)
    # Italic: *text* -> \textit{text}
    text = re.sub(r'\*([^*]+)\*', r'\\textit{\1}', text)
    return text


def escape_latex(text):
    """Escape special LaTeX characters (except math)."""
    # Don't escape inside math mode - this is tricky
    # For now, handle common cases
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('#', '\\#')
    # But restore & in tables
    return text


def convert_table(lines, start_idx):
    """Convert markdown table to LaTeX tabular."""
    table_lines = []
    i = start_idx

    # Collect table lines
    while i < len(lines) and '|' in lines[i]:
        table_lines.append(lines[i])
        i += 1

    if len(table_lines) < 2:
        return None, start_idx

    # Parse header
    header = table_lines[0]
    cells = [c.strip() for c in header.split('|')[1:-1]]
    num_cols = len(cells)

    # Create LaTeX table
    col_spec = 'c' * num_cols
    latex = ['\\begin{center}', f'\\begin{{tabular}}{{{col_spec}}}', '\\toprule']

    # Header row
    header_cells = [c.strip() for c in table_lines[0].split('|')[1:-1]]
    latex.append(' & '.join(header_cells) + ' \\\\')
    latex.append('\\midrule')

    # Data rows (skip separator line)
    for line in table_lines[2:]:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        latex.append(' & '.join(cells) + ' \\\\')

    latex.append('\\bottomrule')
    latex.append('\\end{tabular}')
    latex.append('\\end{center}')

    return '\n'.join(latex), i


def convert_list(lines, start_idx):
    """Convert markdown list to LaTeX itemize."""
    list_lines = []
    i = start_idx

    while i < len(lines):
        line = lines[i]
        if line.startswith('- ') or line.startswith('* '):
            list_lines.append(line[2:])
            i += 1
        elif line.startswith('  ') and list_lines:  # Continuation
            list_lines[-1] += ' ' + line.strip()
            i += 1
        elif re.match(r'^\d+\. ', line):
            list_lines.append(('enum', line[line.index('.')+2:]))
            i += 1
        else:
            break

    if not list_lines:
        return None, start_idx

    # Check if enumerated
    is_enum = isinstance(list_lines[0], tuple)

    if is_enum:
        latex = ['\\begin{enumerate}']
        for item in list_lines:
            if isinstance(item, tuple):
                latex.append(f'\\item {item[1]}')
            else:
                latex.append(f'\\item {item}')
        latex.append('\\end{enumerate}')
    else:
        latex = ['\\begin{itemize}']
        for item in list_lines:
            latex.append(f'\\item {item}')
        latex.append('\\end{itemize}')

    return '\n'.join(latex), i


def convert_theorem_env(line, env_type, name=None):
    """Convert theorem-like environment."""
    if name:
        return f'\\begin{{{env_type}}}[{name}]'
    else:
        return f'\\begin{{{env_type}}}'


def process_chapter(md_content, chapter_num):
    """Convert a full markdown chapter to LaTeX."""
    lines = md_content.split('\n')
    output = []
    i = 0
    in_env = None  # Track current theorem environment
    in_code_block = False
    code_language = None

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                lang = line[3:].strip() or 'python'
                output.append(f'\\begin{{lstlisting}}[language={lang}]')
            else:
                in_code_block = False
                output.append('\\end{lstlisting}')
            i += 1
            continue

        if in_code_block:
            output.append(line)
            i += 1
            continue

        # Chapter title
        if line.startswith('# Chapter'):
            match = re.match(r'# Chapter \d+: (.+)', line)
            if match:
                title = match.group(1)
                output.append(f'\\chapter{{{title}}}')
            i += 1
            continue

        # Section headers
        if line.startswith('## '):
            # Extract section number and title
            match = re.match(r'## (\d+\.\d+) (.+)', line)
            if match:
                title = match.group(2)
                output.append(f'\\section{{{title}}}')
            else:
                title = line[3:]
                output.append(f'\\section{{{title}}}')
            i += 1
            continue

        if line.startswith('### '):
            match = re.match(r'### (Example \d+\.\d+): (.+)', line)
            if match:
                name = match.group(2)
                output.append(f'\\subsection*{{Example: {name}}}')
            else:
                title = line[4:]
                output.append(f'\\subsection{{{title}}}')
            i += 1
            continue

        # Horizontal rule (section break)
        if line.strip() == '---':
            output.append('')
            i += 1
            continue

        # Tables
        if '|' in line and i + 1 < len(lines) and '|' in lines[i + 1]:
            table_latex, new_i = convert_table(lines, i)
            if table_latex:
                output.append(table_latex)
                i = new_i
                continue

        # Lists
        if line.startswith('- ') or line.startswith('* ') or re.match(r'^\d+\. ', line):
            # Check if this is a definition list item (inside theorem env)
            if in_env:
                # Keep as-is for now, process item
                pass
            else:
                list_latex, new_i = convert_list(lines, i)
                if list_latex:
                    output.append(list_latex)
                    i = new_i
                    continue

        # Theorem-like environments
        # Definition
        def_match = re.match(r'\*\*Definition (\d+\.\d+)(?: \(([^)]+)\))?\.\*\*\s*(.*)', line)
        if def_match:
            name = def_match.group(2)
            rest = def_match.group(3)
            if name:
                output.append(f'\\begin{{definition}}[{name}]')
            else:
                output.append('\\begin{definition}')
            if rest:
                output.append(rest)
            in_env = 'definition'
            i += 1
            continue

        # Theorem
        thm_match = re.match(r'\*\*Theorem (\d+\.\d+)(?: \(([^)]+)\))?\.\*\*\s*(.*)', line)
        if thm_match:
            name = thm_match.group(2)
            rest = thm_match.group(3)
            if name:
                output.append(f'\\begin{{theorem}}[{name}]')
            else:
                output.append('\\begin{theorem}')
            if rest:
                output.append(rest)
            in_env = 'theorem'
            i += 1
            continue

        # Proposition
        prop_match = re.match(r'\*\*Proposition (\d+\.\d+)(?: \(([^)]+)\))?\.\*\*\s*(.*)', line)
        if prop_match:
            name = prop_match.group(2)
            rest = prop_match.group(3)
            if name:
                output.append(f'\\begin{{proposition}}[{name}]')
            else:
                output.append('\\begin{proposition}')
            if rest:
                output.append(rest)
            in_env = 'proposition'
            i += 1
            continue

        # Lemma
        lem_match = re.match(r'\*\*Lemma (\d+\.\d+)(?: \(([^)]+)\))?\.\*\*\s*(.*)', line)
        if lem_match:
            name = lem_match.group(2)
            rest = lem_match.group(3)
            if name:
                output.append(f'\\begin{{lemma}}[{name}]')
            else:
                output.append('\\begin{lemma}')
            if rest:
                output.append(rest)
            in_env = 'lemma'
            i += 1
            continue

        # Corollary
        cor_match = re.match(r'\*\*Corollary (\d+\.\d+)(?: \(([^)]+)\))?\.\*\*\s*(.*)', line)
        if cor_match:
            name = cor_match.group(2)
            rest = cor_match.group(3)
            if name:
                output.append(f'\\begin{{corollary}}[{name}]')
            else:
                output.append('\\begin{corollary}')
            if rest:
                output.append(rest)
            in_env = 'corollary'
            i += 1
            continue

        # Example
        ex_match = re.match(r'\*\*Example (\d+\.\d+)(?: \(([^)]+)\))?\.\*\*\s*(.*)', line)
        if ex_match:
            name = ex_match.group(2)
            rest = ex_match.group(3)
            if name:
                output.append(f'\\begin{{example}}[{name}]')
            else:
                output.append('\\begin{example}')
            if rest:
                output.append(rest)
            in_env = 'example'
            i += 1
            continue

        # Remark
        rem_match = re.match(r'\*\*Remark(\.\*\*|\s*\d+\.\d+\.?\*\*)\s*(.*)', line)
        if rem_match:
            rest = rem_match.group(2)
            output.append('\\begin{remark}')
            if rest:
                output.append(rest)
            in_env = 'remark'
            i += 1
            continue

        # Observation
        obs_match = re.match(r'\*\*Observation (\d+\.\d+)(?: \(([^)]+)\))?\.\*\*\s*(.*)', line)
        if obs_match:
            name = obs_match.group(2)
            rest = obs_match.group(3)
            if name:
                output.append(f'\\begin{{observation}}[{name}]')
            else:
                output.append('\\begin{observation}')
            if rest:
                output.append(rest)
            in_env = 'observation'
            i += 1
            continue

        # Conjecture
        conj_match = re.match(r'\*\*Conjecture (\d+\.\d+)(?: \(([^)]+)\))?\.\*\*\s*(.*)', line)
        if conj_match:
            name = conj_match.group(2)
            rest = conj_match.group(3)
            if name:
                output.append(f'\\begin{{conjecture}}[{name}]')
            else:
                output.append('\\begin{conjecture}')
            if rest:
                output.append(rest)
            in_env = 'conjecture'
            i += 1
            continue

        # Question
        quest_match = re.match(r'\*\*Question (\d+\.\d+)(?: \(([^)]+)\))?\.\*\*\s*(.*)', line)
        if quest_match:
            name = quest_match.group(2)
            rest = quest_match.group(3)
            if name:
                output.append(f'\\begin{{question}}[{name}]')
            else:
                output.append('\\begin{question}')
            if rest:
                output.append(rest)
            in_env = 'question'
            i += 1
            continue

        # Algorithm
        alg_match = re.match(r'\*\*Algorithm (\d+\.\d+)(?: \(([^)]+)\))?\.\*\*\s*(.*)', line)
        if alg_match:
            name = alg_match.group(2)
            rest = alg_match.group(3)
            if name:
                output.append(f'\\begin{{algorithm_env}}[{name}]')
            else:
                output.append('\\begin{algorithm_env}')
            if rest:
                output.append(rest)
            in_env = 'algorithm_env'
            i += 1
            continue

        # Proof start
        if line.strip().startswith('*Proof.*') or line.strip().startswith('*Proof:*'):
            rest = line.replace('*Proof.*', '').replace('*Proof:*', '').strip()
            output.append('\\begin{proof}')
            if rest:
                output.append(rest)
            in_env = 'proof'
            i += 1
            continue

        # End of proof (square)
        if '$\\square$' in line or line.strip() == '$\\square$':
            line = line.replace('$\\square$', '')
            if line.strip():
                output.append(line)
            output.append('\\end{proof}')
            in_env = None
            i += 1
            continue

        # Empty line might end an environment
        if line.strip() == '' and in_env and in_env != 'proof':
            # Look ahead - if next non-empty line is a new env or section, close current
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines):
                next_line = lines[j]
                # Check if next line starts new env or section
                if (next_line.startswith('**Definition') or
                    next_line.startswith('**Theorem') or
                    next_line.startswith('**Proposition') or
                    next_line.startswith('**Lemma') or
                    next_line.startswith('**Example') or
                    next_line.startswith('**Remark') or
                    next_line.startswith('**Observation') or
                    next_line.startswith('**Conjecture') or
                    next_line.startswith('**Question') or
                    next_line.startswith('**Algorithm') or
                    next_line.startswith('## ') or
                    next_line.startswith('### ') or
                    next_line.startswith('---')):
                    output.append(f'\\end{{{in_env}}}')
                    in_env = None

        # Regular line processing
        processed_line = line
        processed_line = convert_display_math(processed_line)
        processed_line = convert_bold_italic(processed_line)

        # Handle \lbrace and \rbrace -> \{ and \}
        processed_line = processed_line.replace('\\lbrace', '\\{')
        processed_line = processed_line.replace('\\rbrace', '\\}')

        output.append(processed_line)
        i += 1

    # Close any remaining environment
    if in_env:
        output.append(f'\\end{{{in_env}}}')

    return '\n'.join(output)


def main():
    if len(sys.argv) < 3:
        print("Usage: convert_md_to_tex.py input.md output.tex")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    # Extract chapter number from filename
    match = re.match(r'(\d+)_', input_path.name)
    chapter_num = int(match.group(1)) if match else 1

    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    tex_content = process_chapter(md_content, chapter_num)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(tex_content)

    print(f"Converted {input_path} -> {output_path}")


if __name__ == '__main__':
    main()
