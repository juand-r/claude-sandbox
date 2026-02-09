#!/usr/bin/env python3
"""Post-process .tex files to fix remaining formatting issues."""
import re
import os

def fix_tex_file(text):
    """Fix all remaining formatting issues in a .tex file."""
    lines = text.split('\n')
    result = []
    i = 0
    in_display_math = False

    while i < len(lines):
        line = lines[i]

        # Fix 1: Convert raw --- horizontal rules to \bigskip
        if line.strip() == '---':
            result.append('')
            result.append('\\bigskip')
            result.append('')
            i += 1
            continue

        # Fix 2: Convert raw $$ display math blocks
        if line.strip() == '$$':
            # Opening $$, find closing $$
            math_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != '$$':
                math_lines.append(lines[i])
                i += 1
            math = '\n'.join(math_lines)
            tag_m = re.search(r'\\tag\{([^}]+)\}', math)
            if tag_m:
                label_raw = tag_m.group(1)
                label = re.sub(r'[\$\\]', '', label_raw)
                math = re.sub(r'\s*\\tag\{[^}]+\}', '', math)
                result.append(f'\\begin{{equation}}\\label{{eq:pp-{label}}}\\tag{{{label_raw}}}')
                result.append(math)
                result.append('\\end{equation}')
            else:
                result.append('\\[')
                result.append(math)
                result.append('\\]')
            i += 1  # skip closing $$
            continue

        # Also handle single-line $$...$$ that wasn't converted
        stripped = line.strip()
        if stripped.startswith('$$') and stripped.endswith('$$') and len(stripped) > 4 and '\\[' not in stripped:
            math = stripped[2:-2].strip()
            tag_m = re.search(r'\\tag\{([^}]+)\}', math)
            if tag_m:
                label_raw = tag_m.group(1)
                label = re.sub(r'[\$\\]', '', label_raw)
                math = re.sub(r'\s*\\tag\{[^}]+\}', '', math)
                result.append(f'\\begin{{equation}}\\label{{eq:pp-{label}}}\\tag{{{label_raw}}}')
                result.append(math)
                result.append('\\end{equation}')
            else:
                result.append('\\[')
                result.append(math)
                result.append('\\]')
            i += 1
            continue

        # Fix 3: Convert raw **text** to \textbf{text}
        # Skip lines inside display math environments and lines with ** in \label/\tag
        if not in_display_math and '**' in line and not re.search(r'\\(?:label|tag)\{[^}]*\*\*', line):
            line = re.sub(r'\*\*((?:[^*]|\*(?!\*))+?)\*\*', r'\\textbf{\1}', line)

        # Track display math state for next iteration
        if line.strip() in ('\\[', '\\begin{equation}', '\\begin{align}', '\\begin{align*}',
                           '\\begin{gather}', '\\begin{gather*}', '\\begin{multline}',
                           '\\begin{multline*}'):
            in_display_math = True
        elif line.strip() in ('\\]', '\\end{equation}', '\\end{align}', '\\end{align*}',
                              '\\end{gather}', '\\end{gather*}', '\\end{multline}',
                              '\\end{multline*}'):
            in_display_math = False

        result.append(line)
        i += 1

    return '\n'.join(result)


def main():
    latex_dir = '/home/user/claude-sandbox/reservoir-textbook/latex'
    for ch in range(1, 18):
        fname = f'chapter{ch:02d}.tex'
        path = os.path.join(latex_dir, fname)
        with open(path, 'r') as f:
            text = f.read()

        fixed = fix_tex_file(text)

        if fixed != text:
            with open(path, 'w') as f:
                f.write(fixed)

            # Count fixes
            dashes_before = text.count('\n---\n')
            dashes_after = fixed.count('\n---\n')
            dd_before = text.count('$$')
            dd_after = fixed.count('$$')
            bold_before = len(re.findall(r'\*\*[^*]+\*\*', text))
            bold_after = len(re.findall(r'\*\*[^*]+\*\*', fixed))

            changes = []
            if dashes_before != dashes_after:
                changes.append(f'--- {dashes_before}->{dashes_after}')
            if dd_before != dd_after:
                changes.append(f'$$ {dd_before}->{dd_after}')
            if bold_before != bold_after:
                changes.append(f'** {bold_before}->{bold_after}')

            if changes:
                print(f'{fname}: {", ".join(changes)}')
            else:
                print(f'{fname}: minor fixes')
        else:
            print(f'{fname}: no changes')


if __name__ == '__main__':
    main()
