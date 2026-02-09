#!/usr/bin/env python3
"""Convert markdown chapters to LaTeX .tex files for the textbook."""

import re
import sys
import os

def convert_md_to_latex(md_text):
    """Convert a markdown chapter to LaTeX."""
    lines = md_text.split('\n')
    out = []
    i = 0
    in_list = None  # 'itemize' or 'enumerate'
    list_stack = []  # stack of list types for nesting
    in_code_block = False
    in_exercise_section = False
    in_rec_reading = False
    in_references = False

    def split_math(s):
        """Split a string into math and non-math segments.
        Returns list of (is_math, text) tuples."""
        # Match display math $$...$$ first, then inline $...$
        # Use a simple state machine to handle nested/escaped $
        segments = []
        i = 0
        n = len(s)
        current = []
        in_math = False
        math_delim = None  # '$' or '$$'

        while i < n:
            if not in_math:
                if s[i:i+2] == '$$':
                    if current:
                        segments.append((False, ''.join(current)))
                        current = []
                    current.append('$$')
                    in_math = True
                    math_delim = '$$'
                    i += 2
                elif s[i] == '$' and (i + 1 < n and s[i+1] != '$'):
                    if current:
                        segments.append((False, ''.join(current)))
                        current = []
                    current.append('$')
                    in_math = True
                    math_delim = '$'
                    i += 1
                else:
                    current.append(s[i])
                    i += 1
            else:
                if math_delim == '$$' and s[i:i+2] == '$$':
                    current.append('$$')
                    segments.append((True, ''.join(current)))
                    current = []
                    in_math = False
                    math_delim = None
                    i += 2
                elif math_delim == '$' and s[i] == '$' and (i + 1 >= n or s[i+1] != '$'):
                    current.append('$')
                    segments.append((True, ''.join(current)))
                    current = []
                    in_math = False
                    math_delim = None
                    i += 1
                else:
                    current.append(s[i])
                    i += 1

        if current:
            segments.append((in_math, ''.join(current)))

        return segments

    def escape_text(s):
        """Escape LaTeX special chars in text (not math)."""
        segments = split_math(s)
        result = []
        for is_math, part in segments:
            if is_math:
                result.append(part)
            else:
                part = part.replace('&', r'\&')
                part = part.replace('%', r'\%')
                part = part.replace('#', r'\#')
                part = re.sub(r'(?<!\\)_', r'\_', part)
                # Replace Unicode arrows and special chars
                part = part.replace('↔', r'$\leftrightarrow$')
                part = part.replace('→', r'$\to$')
                part = part.replace('←', r'$\leftarrow$')
                part = part.replace('⟹', r'$\Longrightarrow$')
                part = part.replace('≥', r'$\geq$')
                part = part.replace('≤', r'$\leq$')
                part = part.replace('…', r'\ldots{}')
                part = part.replace('—', '---')
                part = part.replace('–', '--')
                result.append(part)
        return ''.join(result)

    def convert_inline_formatting(s):
        """Convert **bold** and *italic* to LaTeX, only in non-math segments."""
        segments = split_math(s)
        result = []
        for is_math, part in segments:
            if is_math:
                result.append(part)
            else:
                # Bold: **text** → \textbf{text}
                part = re.sub(r'\*\*([^*]+?)\*\*', r'\\textbf{\1}', part)
                # Italic: *text* → \textit{text}
                part = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'\\textit{\1}', part)
                result.append(part)
        return ''.join(result)

    def convert_display_math_line(s):
        """Convert $$...$$ on a single line to equation or displaymath."""
        stripped = s.strip()
        if stripped.startswith('$$') and stripped.endswith('$$') and len(stripped) > 4:
            math = stripped[2:-2].strip()
            tag_m = re.search(r'\\tag\{([^}]+)\}', math)
            if tag_m:
                label_raw = tag_m.group(1)
                # Clean label: remove $, \, etc.
                label = re.sub(r'[\$\\]', '', label_raw)
                math = re.sub(r'\s*\\tag\{[^}]+\}', '', math)
                return f'\\begin{{equation}}\\label{{eq:{label}}}\\tag{{{label_raw}}}\n{math}\n\\end{{equation}}'
            else:
                return f'\\[\n{math}\n\\]'
        return s

    def close_all_lists():
        nonlocal list_stack
        result = []
        while list_stack:
            lt = list_stack.pop()
            result.append(f'\\end{{{lt}}}')
        return result

    def process_line(line):
        """Process a single line, applying escaping and formatting."""
        # Handle display math on single lines first (before escaping)
        stripped = line.strip()
        if stripped.startswith('$$') and stripped.endswith('$$') and len(stripped) > 4:
            return convert_display_math_line(line)
        line = escape_text(line)
        line = convert_inline_formatting(line)
        return line

    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                out.append('\\end{lstlisting}')
                in_code_block = False
                i += 1
                continue
            else:
                in_code_block = True
                out.append('\\begin{lstlisting}')
                i += 1
                continue

        if in_code_block:
            out.append(line)
            i += 1
            continue

        # Horizontal rules
        if line.strip() == '---':
            out.append('')
            out.append('\\bigskip')
            out.append('')
            i += 1
            continue

        # Chapter heading: # Chapter N: Title
        m = re.match(r'^#\s+Chapter\s+(\d+):\s*(.*)', line)
        if m:
            out.extend(close_all_lists())
            chnum = m.group(1)
            title = m.group(2).strip()
            out.append(f'\\chapter{{{title}}}\\label{{ch:{chnum}}}')
            i += 1
            continue

        # Section: ## N.M Title  or ## Title
        m = re.match(r'^##\s+(\d+\.\d+)\s+(.*)', line)
        if m:
            out.extend(close_all_lists())
            secnum = m.group(1)
            title = m.group(2).strip()
            # Check for unnumbered sections
            if any(kw in title.lower() for kw in ['recommended reading', 'exercises', 'references', 'further reading']):
                out.append(f'\\section*{{{title}}}')
                in_rec_reading = 'reading' in title.lower()
                in_exercise_section = 'exercise' in title.lower()
                in_references = 'reference' in title.lower()
            else:
                out.append(f'\\section{{{title}}}\\label{{sec:{secnum}}}')
                in_rec_reading = False
                in_exercise_section = False
                in_references = False
            i += 1
            continue

        # Also handle ## without number
        m = re.match(r'^##\s+(.*)', line)
        if m and not line.startswith('###'):
            out.extend(close_all_lists())
            title = m.group(1).strip()
            if any(kw in title.lower() for kw in ['recommended reading', 'exercises', 'references', 'further reading']):
                out.append(f'\\section*{{{title}}}')
            else:
                out.append(f'\\section{{{title}}}')
            i += 1
            continue

        # Subsection: ### N.M.K Title
        m = re.match(r'^###\s+(\d+\.\d+\.\d+)\s+(.*)', line)
        if m:
            out.extend(close_all_lists())
            secnum = m.group(1)
            title = m.group(2).strip()
            out.append(f'\\subsection{{{title}}}\\label{{sec:{secnum}}}')
            i += 1
            continue

        # Also handle ### without number
        m = re.match(r'^###\s+(.*)', line)
        if m:
            out.extend(close_all_lists())
            title = m.group(1).strip()
            out.append(f'\\subsection{{{title}}}')
            i += 1
            continue

        # Display math blocks: $$ ... $$
        if line.strip().startswith('$$'):
            out.extend(close_all_lists())
            if line.strip().endswith('$$') and len(line.strip()) > 4:
                # Single-line display math
                math = line.strip()[2:-2].strip()
                tag_m = re.search(r'\\tag\{([^}]+)\}', math)
                if tag_m:
                    label_raw = tag_m.group(1)
                    label = re.sub(r'[\$\\]', '', label_raw)
                    math = re.sub(r'\s*\\tag\{[^}]+\}', '', math)
                    out.append(f'\\begin{{equation}}\\label{{eq:{label}}}\\tag{{{label_raw}}}')
                    out.append(math)
                    out.append('\\end{equation}')
                else:
                    out.append('\\[')
                    out.append(math)
                    out.append('\\]')
            else:
                # Multi-line display math
                # Opening line might have content after $$, e.g. $$\begin{aligned}
                opening_content = line.strip()[2:].strip()
                math_lines = []
                if opening_content:
                    math_lines.append(opening_content)
                i += 1
                while i < len(lines):
                    cl = lines[i].strip()
                    # Check for closing: line is just "$$" or ends with "$$"
                    if cl == '$$':
                        break
                    if cl.endswith('$$') and not cl.startswith('$$'):
                        # e.g. \end{aligned}$$
                        math_lines.append(cl[:-2].strip())
                        break
                    if cl.startswith('$$'):
                        break
                    math_lines.append(lines[i])
                    i += 1
                math = '\n'.join(math_lines)
                tag_m = re.search(r'\\tag\{([^}]+)\}', math)
                if tag_m:
                    label_raw = tag_m.group(1)
                    label = re.sub(r'[\$\\]', '', label_raw)
                    math = re.sub(r'\s*\\tag\{[^}]+\}', '', math)
                    out.append(f'\\begin{{equation}}\\label{{eq:{label}}}\\tag{{{label_raw}}}')
                    out.append(math)
                    out.append('\\end{equation}')
                else:
                    out.append('\\[')
                    out.append(math)
                    out.append('\\]')
            i += 1
            continue

        # Blockquotes
        if line.strip().startswith('> '):
            out.extend(close_all_lists())
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            out.append('\\begin{quote}')
            for ql in quote_lines:
                out.append(process_line(ql))
            out.append('\\end{quote}')
            continue

        # Definition: **Definition N.M** (Name).
        m = re.match(r'^\*\*Definition\s+([\d.]+)\*\*\s*\(([^)]+)\)\.\s*(.*)', line)
        if m:
            out.extend(close_all_lists())
            defnum = m.group(1)
            name = m.group(2)
            rest = m.group(3).strip()
            # Remove italic markers from definition body
            rest = re.sub(r'^\*(.+)\*$', r'\1', rest)
            out.append(f'\\begin{{definition}}[{name}]\\label{{def:{defnum}}}')
            if rest:
                out.append(process_line(rest))
            # Read continuation lines until next definition/theorem/section or blank line followed by non-continuation
            i += 1
            while i < len(lines):
                nl = lines[i]
                # Check if this is a new environment or section
                if re.match(r'^#{1,3}\s', nl) or re.match(r'^\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b', nl):
                    break
                if nl.strip() == '' and i + 1 < len(lines) and re.match(r'^(#{1,3}\s|\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b)', lines[i+1]):
                    break
                out.append(process_line(nl))
                i += 1
            # Remove trailing empty lines inside the environment
            while out and out[-1].strip() == '':
                out.pop()
            out.append('\\end{definition}')
            out.append('')
            continue

        # Definition without name
        m = re.match(r'^\*\*Definition\s+([\d.]+)\*\*\.?\s*(.*)', line)
        if m:
            out.extend(close_all_lists())
            defnum = m.group(1)
            rest = m.group(2).strip()
            rest = re.sub(r'^\*(.+)\*$', r'\1', rest)
            out.append(f'\\begin{{definition}}\\label{{def:{defnum}}}')
            if rest:
                out.append(process_line(rest))
            i += 1
            while i < len(lines):
                nl = lines[i]
                if re.match(r'^#{1,3}\s', nl) or re.match(r'^\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b', nl):
                    break
                if nl.strip() == '' and i + 1 < len(lines) and re.match(r'^(#{1,3}\s|\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b)', lines[i+1]):
                    break
                out.append(process_line(nl))
                i += 1
            while out and out[-1].strip() == '':
                out.pop()
            out.append('\\end{definition}')
            out.append('')
            continue

        # Theorem
        m = re.match(r'^\*\*Theorem\s+([\d.]+)\*\*\s*(?:\(([^)]+)\))?\.\s*(.*)', line)
        if m:
            out.extend(close_all_lists())
            thmnum = m.group(1)
            name = m.group(2)
            rest = m.group(3).strip()
            if name:
                out.append(f'\\begin{{theorem}}[{name}]\\label{{thm:{thmnum}}}')
            else:
                out.append(f'\\begin{{theorem}}\\label{{thm:{thmnum}}}')
            if rest:
                out.append(process_line(rest))
            i += 1
            while i < len(lines):
                nl = lines[i]
                if nl.strip().startswith('*Proof') or nl.strip().startswith('\\begin{proof'):
                    break
                if re.match(r'^#{1,3}\s', nl) or re.match(r'^\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b', nl):
                    break
                if nl.strip() == '' and i + 1 < len(lines) and (re.match(r'^(#{1,3}\s|\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b|\*Proof)', lines[i+1])):
                    break
                out.append(process_line(nl))
                i += 1
            while out and out[-1].strip() == '':
                out.pop()
            out.append('\\end{theorem}')
            out.append('')
            continue

        # Proposition
        m = re.match(r'^\*\*Proposition\s+([\d.]+)\*\*\.?\s*(.*)', line)
        if m:
            out.extend(close_all_lists())
            num = m.group(1)
            rest = m.group(2).strip()
            out.append(f'\\begin{{proposition}}\\label{{prop:{num}}}')
            if rest:
                out.append(process_line(rest))
            i += 1
            while i < len(lines):
                nl = lines[i]
                if nl.strip().startswith('*Proof') or re.match(r'^#{1,3}\s', nl) or re.match(r'^\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b', nl):
                    break
                if nl.strip() == '' and i + 1 < len(lines) and re.match(r'^(#{1,3}\s|\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b|\*Proof)', lines[i+1]):
                    break
                out.append(process_line(nl))
                i += 1
            while out and out[-1].strip() == '':
                out.pop()
            out.append('\\end{proposition}')
            out.append('')
            continue

        # Lemma
        m = re.match(r'^\*\*Lemma\s+([\d.]+)\*\*\s*(?:\(([^)]+)\))?\.\s*(.*)', line)
        if m:
            out.extend(close_all_lists())
            num = m.group(1)
            name = m.group(2)
            rest = m.group(3).strip()
            if name:
                out.append(f'\\begin{{lemma}}[{name}]\\label{{lem:{num}}}')
            else:
                out.append(f'\\begin{{lemma}}\\label{{lem:{num}}}')
            if rest:
                out.append(process_line(rest))
            i += 1
            while i < len(lines):
                nl = lines[i]
                if nl.strip().startswith('*Proof') or re.match(r'^#{1,3}\s', nl) or re.match(r'^\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b', nl):
                    break
                if nl.strip() == '' and i + 1 < len(lines) and re.match(r'^(#{1,3}\s|\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b|\*Proof)', lines[i+1]):
                    break
                out.append(process_line(nl))
                i += 1
            while out and out[-1].strip() == '':
                out.pop()
            out.append('\\end{lemma}')
            out.append('')
            continue

        # Corollary
        m = re.match(r'^\*\*Corollary\s+([\d.]+)\*\*\s*(?:\(([^)]+)\))?\.\s*(.*)', line)
        if m:
            out.extend(close_all_lists())
            num = m.group(1)
            name = m.group(2)
            rest = m.group(3).strip()
            if name:
                out.append(f'\\begin{{corollary}}[{name}]\\label{{cor:{num}}}')
            else:
                out.append(f'\\begin{{corollary}}\\label{{cor:{num}}}')
            if rest:
                out.append(process_line(rest))
            i += 1
            while i < len(lines):
                nl = lines[i]
                if nl.strip().startswith('*Proof') or re.match(r'^#{1,3}\s', nl) or re.match(r'^\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b', nl):
                    break
                if nl.strip() == '' and i + 1 < len(lines) and re.match(r'^(#{1,3}\s|\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b|\*Proof)', lines[i+1]):
                    break
                out.append(process_line(nl))
                i += 1
            while out and out[-1].strip() == '':
                out.pop()
            out.append('\\end{corollary}')
            out.append('')
            continue

        # Proof start - matches *Proof.*, *Proof of (1).*, **Proof.**, **Proof sketch.**, etc.
        proof_start_m = re.match(r'^\*{1,2}Proof(?:\s+[^*]+?)?\*{0,2}\.?\s*(.*)', line.strip())
        if proof_start_m and ('Proof' in line.strip()[:20]):
            # Extract optional proof title
            title_m = re.match(r'^\*{1,2}Proof\s*(.*?)\*{0,2}\.?\s*$', line.strip().split('.')[0] + '.')
            proof_title = ''
            if title_m:
                t = title_m.group(1).strip().rstrip('.*')
                if t:
                    proof_title = t
            if proof_title:
                out.append(f'\\begin{{proof}}[Proof {proof_title}]')
            else:
                out.append('\\begin{proof}')
            # Get the rest of the line after the proof marker
            rest = re.sub(r'^\*{1,2}Proof(?:\s+[^*]*?)?\*{0,2}\.?\s*', '', line.strip())
            if rest:
                out.append(process_line(rest))
            i += 1
            continue

        # Proof end (square) - handle $\square$, $\blacksquare$, $\quad\square$, etc.
        square_re = re.compile(r'\$\s*(?:\\quad\s*)?\\(?:square|blacksquare)\s*\$')
        if square_re.search(line):
            line_without_square = square_re.sub('', line).strip()
            if line_without_square:
                out.append(process_line(line_without_square))
            out.append('\\end{proof}')
            out.append('')
            i += 1
            continue

        # Remark
        m = re.match(r'^\*\*Remark(?:\s+[\d.]+)?\.\*\*\s*(.*)', line)
        if not m:
            m = re.match(r'^\*\*Remark(?:\s+[\d.]+)?\*\*\.?\s*(.*)', line)
        if m:
            out.extend(close_all_lists())
            rest = m.group(1).strip()
            out.append('\\begin{remark}')
            if rest:
                out.append(process_line(rest))
            i += 1
            while i < len(lines):
                nl = lines[i]
                if re.match(r'^#{1,3}\s', nl) or re.match(r'^\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b', nl):
                    break
                if nl.strip() == '' and i + 1 < len(lines) and re.match(r'^(#{1,3}\s|\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b)', lines[i+1]):
                    break
                out.append(process_line(nl))
                i += 1
            while out and out[-1].strip() == '':
                out.pop()
            out.append('\\end{remark}')
            out.append('')
            continue

        # Example
        m = re.match(r'^\*\*Example(?:\s+[\d.]+)?\.\*\*\s*(.*)', line)
        if not m:
            m = re.match(r'^\*\*Example(?:\s+[\d.]+)?\*\*\.?\s*(.*)', line)
        if m:
            out.extend(close_all_lists())
            rest = m.group(1).strip()
            out.append('\\begin{example}')
            if rest:
                out.append(process_line(rest))
            i += 1
            while i < len(lines):
                nl = lines[i]
                if re.match(r'^#{1,3}\s', nl) or re.match(r'^\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b', nl):
                    break
                if nl.strip() == '' and i + 1 < len(lines) and re.match(r'^(#{1,3}\s|\*\*(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Exercise)\b)', lines[i+1]):
                    break
                # But allow display math inside examples
                out.append(process_line(nl))
                i += 1
            while out and out[-1].strip() == '':
                out.pop()
            out.append('\\end{example}')
            out.append('')
            continue

        # Exercise
        m = re.match(r'^\*\*Exercise\s+([\d.]+)[\.\*].*?\*\*\.?\s*(.*)', line)
        if m:
            out.extend(close_all_lists())
            rest = m.group(2).strip()
            out.append('\\begin{exercise}')
            if rest:
                out.append(process_line(rest))
            i += 1
            while i < len(lines):
                nl = lines[i]
                if re.match(r'^\*\*Exercise\s+', nl) or re.match(r'^#{1,3}\s', nl):
                    break
                if nl.strip() == '' and i + 1 < len(lines) and (re.match(r'^\*\*Exercise\s+', lines[i+1]) or re.match(r'^#{1,3}\s', lines[i+1])):
                    break
                out.append(process_line(nl))
                i += 1
            while out and out[-1].strip() == '':
                out.pop()
            out.append('\\end{exercise}')
            out.append('')
            continue

        # Lists: unordered
        if re.match(r'^(\s*)- ', line):
            indent = len(re.match(r'^(\s*)', line).group(1))
            if not list_stack or indent > 0:
                # Determine nesting level
                pass
            if not list_stack:
                out.append('\\begin{itemize}[nosep]')
                list_stack.append('itemize')
            item_text = re.sub(r'^\s*- ', '', line)
            out.append(f'  \\item {process_line(item_text)}')
            i += 1
            continue

        # Lists: ordered
        m = re.match(r'^(\s*)\d+\.\s+(.*)', line)
        if m:
            if not list_stack:
                out.append('\\begin{enumerate}[nosep]')
                list_stack.append('enumerate')
            item_text = m.group(2)
            out.append(f'  \\item {process_line(item_text)}')
            i += 1
            continue

        # If we're in a list but hit a non-list line, close the list
        if list_stack and line.strip() != '' and not re.match(r'^\s*[-\d]', line):
            out.extend(close_all_lists())

        # Empty lines - close lists
        if line.strip() == '' and list_stack:
            # Check if next line continues the list
            if i + 1 < len(lines) and re.match(r'^\s*[-\d]', lines[i+1]):
                out.append('')
                i += 1
                continue
            else:
                out.extend(close_all_lists())

        # Regular text
        out.append(process_line(line))
        i += 1

    # Close any remaining open lists
    out.extend(close_all_lists())

    return '\n'.join(out)


def main():
    src_dir = '/home/user/claude-sandbox/reservoir-textbook'
    dst_dir = '/home/user/claude-sandbox/reservoir-textbook/latex'
    os.makedirs(dst_dir, exist_ok=True)

    for ch in range(1, 18):
        fname = f'chapter{ch:02d}'
        src = os.path.join(src_dir, f'{fname}.md')
        dst = os.path.join(dst_dir, f'{fname}.tex')

        if not os.path.exists(src):
            print(f'WARNING: {src} not found, skipping')
            continue

        with open(src, 'r') as f:
            md = f.read()

        tex = convert_md_to_latex(md)

        with open(dst, 'w') as f:
            f.write(tex)

        print(f'Converted {fname}.md -> {fname}.tex')


if __name__ == '__main__':
    main()
