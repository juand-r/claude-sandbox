#!/usr/bin/env python3
"""Convert markdown textbook chapters to LaTeX."""

import re
import os


def convert_md_to_latex(md_content: str) -> str:
    """Convert markdown content to LaTeX."""
    lines = md_content.split('\n')
    output = []

    in_code_block = False
    code_lang = ""
    in_itemize = False
    in_enumerate = False
    in_table = False
    table_lines = []
    in_env = None  # Track current theorem environment

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lang = line[3:].strip()
                lang_map = {'python': 'Python', 'haskell': 'Haskell', '': ''}
                latex_lang = lang_map.get(code_lang.lower(), code_lang)
                if latex_lang:
                    output.append(f'\\begin{{lstlisting}}[language={latex_lang}]')
                else:
                    output.append('\\begin{lstlisting}')
            else:
                in_code_block = False
                output.append('\\end{lstlisting}')
            i += 1
            continue

        if in_code_block:
            output.append(line)
            i += 1
            continue

        # Tables
        if '|' in line and not in_table:
            # Check if this is a table start
            if i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i + 1]):
                in_table = True
                table_lines = [line]
                i += 1
                continue

        if in_table:
            if '|' in line:
                table_lines.append(line)
                i += 1
                continue
            else:
                # End of table, process it
                output.extend(convert_table(table_lines))
                in_table = False
                table_lines = []
                # Don't increment i, process current line normally

        # Display math ($$...$$)
        if line.strip().startswith('$$') and line.strip().endswith('$$') and len(line.strip()) > 4:
            # Single-line display math
            math = line.strip()[2:-2]
            output.append('\\[')
            output.append(fix_math(math))
            output.append('\\]')
            i += 1
            continue

        if line.strip() == '$$':
            # Multi-line display math
            output.append('\\[')
            i += 1
            math_lines = []
            while i < len(lines) and lines[i].strip() != '$$':
                math_lines.append(lines[i])
                i += 1
            output.append(fix_math('\n'.join(math_lines)))
            output.append('\\]')
            i += 1
            continue

        # Headers - don't escape, just convert inline elements
        if line.startswith('# '):
            close_env_if_open(output, in_env)
            in_env = None
            title = line[2:].strip()
            output.append(f'\\chapter{{{convert_inline(title)}}}')
            i += 1
            continue
        if line.startswith('## '):
            close_env_if_open(output, in_env)
            in_env = None
            title = line[3:].strip()
            output.append(f'\\section{{{convert_inline(title)}}}')
            i += 1
            continue
        if line.startswith('### '):
            close_env_if_open(output, in_env)
            in_env = None
            title = line[4:].strip()
            output.append(f'\\subsection{{{convert_inline(title)}}}')
            i += 1
            continue
        if line.startswith('#### '):
            close_env_if_open(output, in_env)
            in_env = None
            title = line[5:].strip()
            output.append(f'\\subsubsection{{{convert_inline(title)}}}')
            i += 1
            continue

        # Horizontal rules
        if re.match(r'^---+$', line.strip()):
            output.append('\\bigskip\\hrule\\bigskip')
            i += 1
            continue

        # Check for theorem-like environments at start of paragraph
        env_match = check_for_theorem_env(line)
        if env_match:
            close_env_if_open(output, in_env)
            env_name, env_title, remaining = env_match
            if env_title:
                output.append(f'\\begin{{{env_name}}}[{env_title}]')
            else:
                output.append(f'\\begin{{{env_name}}}')
            in_env = env_name
            if remaining.strip():
                output.append(convert_inline(remaining))
            i += 1
            continue

        # Lists
        stripped = line.lstrip()

        # Bulleted list
        if stripped.startswith('- '):
            close_env_if_open(output, in_env)
            in_env = None
            if not in_itemize:
                output.append('\\begin{itemize}')
                in_itemize = True
            item_text = convert_inline(stripped[2:])
            output.append(f'  \\item {item_text}')
            i += 1
            continue

        # Numbered list
        if re.match(r'^\d+\.\s', stripped):
            close_env_if_open(output, in_env)
            in_env = None
            if not in_enumerate:
                output.append('\\begin{enumerate}')
                in_enumerate = True
            item_text = convert_inline(re.sub(r'^\d+\.\s', '', stripped))
            output.append(f'  \\item {item_text}')
            i += 1
            continue

        # End lists if we're no longer in a list item
        if in_itemize and not stripped.startswith('- '):
            output.append('\\end{itemize}')
            in_itemize = False
        if in_enumerate and not re.match(r'^\d+\.\s', stripped):
            output.append('\\end{enumerate}')
            in_enumerate = False

        # Empty line - might end a theorem environment
        if not line.strip():
            # Check if next non-empty line starts a new section or environment
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                next_line = lines[j]
                if (next_line.startswith('#') or
                    check_for_theorem_env(next_line) or
                    next_line.strip().startswith('- ') or
                    re.match(r'^\d+\.\s', next_line.strip())):
                    close_env_if_open(output, in_env)
                    in_env = None
            output.append('')
            i += 1
            continue

        # Regular paragraph - convert inline formatting
        converted = convert_inline(line)
        output.append(converted)
        i += 1

    # Close any open environments
    close_env_if_open(output, in_env)
    if in_itemize:
        output.append('\\end{itemize}')
    if in_enumerate:
        output.append('\\end{enumerate}')
    if in_table:
        output.extend(convert_table(table_lines))

    return '\n'.join(output)


def close_env_if_open(output, env):
    """Close a theorem environment if one is open."""
    if env:
        if env == 'proof':
            output.append('\\end{proof}')
        else:
            output.append(f'\\end{{{env}}}')


def check_for_theorem_env(line):
    """Check if line starts a theorem-like environment.
    Returns (env_name, title, remaining_text) or None.
    """
    patterns = [
        (r'^\*\*Definition\s+[\d.]+\s*\(([^)]+)\)\.\*\*\s*', 'definition'),
        (r'^\*\*Definition\s+[\d.]+\.\*\*\s*', 'definition'),
        (r'^\*\*Definition\.\*\*\s*', 'definition'),
        (r'^\*\*Theorem\s+[\d.]+\s*\(([^)]+)\)\.\*\*\s*', 'theorem'),
        (r'^\*\*Theorem\s+[\d.]+\.\*\*\s*', 'theorem'),
        (r'^\*\*Theorem\.\*\*\s*', 'theorem'),
        (r'^\*\*Proposition\s+[\d.]+\s*\(([^)]+)\)\.\*\*\s*', 'proposition'),
        (r'^\*\*Proposition\s+[\d.]+\.\*\*\s*', 'proposition'),
        (r'^\*\*Lemma\s+[\d.]+\s*\(([^)]+)\)\.\*\*\s*', 'lemma'),
        (r'^\*\*Lemma\s+[\d.]+\.\*\*\s*', 'lemma'),
        (r'^\*\*Corollary\s+[\d.]+\s*\(([^)]+)\)\.\*\*\s*', 'corollary'),
        (r'^\*\*Corollary\s+[\d.]+\.\*\*\s*', 'corollary'),
        (r'^\*\*Example\s+[\d.]+\s*\(([^)]+)\)\.\*\*\s*', 'example'),
        (r'^\*\*Example\s+[\d.]+\.\*\*\s*', 'example'),
        (r'^\*\*Example\.\*\*\s*', 'example'),
        (r'^\*\*Remark\s+[\d.]+\.\*\*\s*', 'remark'),
        (r'^\*\*Remark\.\*\*\s*', 'remark'),
    ]

    for pattern, env in patterns:
        match = re.match(pattern, line)
        if match:
            remaining = line[match.end():]
            # Check if there's a title in parentheses
            title = match.groups()[0] if match.groups() else None
            return (env, title, remaining)

    return None


def convert_table(table_lines: list) -> list:
    """Convert markdown table to LaTeX tabular."""
    if len(table_lines) < 2:
        return []

    # Parse header
    header = table_lines[0]
    cells = [c.strip() for c in header.split('|')[1:-1]]
    num_cols = len(cells)

    output = []
    col_spec = '|' + 'l|' * num_cols
    output.append(f'\\begin{{tabular}}{{{col_spec}}}')
    output.append('\\hline')

    # Header row
    header_cells = [convert_inline(c) for c in cells]
    output.append(' & '.join(header_cells) + ' \\\\')
    output.append('\\hline')

    # Data rows (skip separator line at index 1)
    for row in table_lines[2:]:
        cells = [c.strip() for c in row.split('|')[1:-1]]
        row_cells = [convert_inline(c) for c in cells]
        output.append(' & '.join(row_cells) + ' \\\\')

    output.append('\\hline')
    output.append('\\end{tabular}')
    output.append('')

    return output


def fix_math(math: str) -> str:
    """Fix math content for LaTeX - convert \lbrace/\rbrace back."""
    math = math.replace('\\lbrace', '\\{').replace('\\rbrace', '\\}')
    return math


def convert_inline(text: str) -> str:
    """Convert inline markdown formatting to LaTeX."""
    result = text

    # First, protect and fix math
    math_segments = []
    def save_math(m):
        fixed = fix_math(m.group(1))
        math_segments.append(f'${fixed}$')
        return f'%%MATH{len(math_segments)-1}%%'

    result = re.sub(r'\$([^$]+)\$', save_math, result)

    # Handle *Proof.* pattern -> \begin{proof}
    result = re.sub(r'^\*Proof\.\*\s*', r'\\begin{proof} ', result)

    # Bold: **text** -> \textbf{text}
    result = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', result)

    # Italic: *text* -> \textit{text}
    result = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'\\textit{\1}', result)

    # Inline code: `code` -> \texttt{code}
    def convert_code(m):
        code = m.group(1)
        # Escape special chars in code
        code = code.replace('\\', '\\textbackslash{}')
        code = code.replace('_', '\\_')
        code = code.replace('{', '\\{')
        code = code.replace('}', '\\}')
        code = code.replace('%', '\\%')
        code = code.replace('&', '\\&')
        code = code.replace('#', '\\#')
        return f'\\texttt{{{code}}}'
    result = re.sub(r'`([^`]+)`', convert_code, result)

    # Links: [text](url) -> \href{url}{text}
    result = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', result)

    # $\square$ QED symbol
    result = result.replace('$\\square$', '\\qed')

    # Restore math
    for i, math in enumerate(math_segments):
        result = result.replace(f'%%MATH{i}%%', math)

    return result


def process_file(md_path: str, tex_path: str):
    """Process a single markdown file to LaTeX."""
    with open(md_path, 'r') as f:
        md_content = f.read()

    latex_content = convert_md_to_latex(md_content)

    with open(tex_path, 'w') as f:
        f.write(latex_content)

    print(f"Converted: {os.path.basename(md_path)} -> {os.path.basename(tex_path)}")


def main():
    md_dir = '/home/user/claude-sandbox/explorations/minimal-dds/textbook'
    tex_dir = '/home/user/claude-sandbox/explorations/minimal-dds/textbook/latex'

    chapters = [
        ('01_iterated_maps.md', 'ch01_iterated_maps.tex'),
        ('02_symbolic_dynamics.md', 'ch02_symbolic_dynamics.tex'),
        ('03_sliding_block_codes.md', 'ch03_sliding_block_codes.tex'),
        ('04_tag_systems.md', 'ch04_tag_systems.tex'),
        ('05_substitution_systems.md', 'ch05_substitution_systems.tex'),
        ('06_iterated_function_systems.md', 'ch06_iterated_function_systems.tex'),
        ('07_cellular_automata.md', 'ch07_cellular_automata.tex'),
        ('08_kolmogorov_complexity.md', 'ch08_kolmogorov_complexity.tex'),
        ('09_logical_depth.md', 'ch09_logical_depth.tex'),
        ('10_computational_mechanics.md', 'ch10_computational_mechanics.tex'),
        ('11_kleene_recursion_theorem.md', 'ch11_kleene_recursion_theorem.tex'),
        ('12_reflective_towers.md', 'ch12_reflective_towers.tex'),
        ('13_aixi_godel_machines.md', 'ch13_aixi_godel_machines.tex'),
        ('14_llms_as_dynamical_systems.md', 'ch14_llms_as_dynamical_systems.tex'),
    ]

    for md_file, tex_file in chapters:
        md_path = os.path.join(md_dir, md_file)
        tex_path = os.path.join(tex_dir, tex_file)
        process_file(md_path, tex_path)

    print(f"\nConverted {len(chapters)} chapters.")


if __name__ == '__main__':
    main()
