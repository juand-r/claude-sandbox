# LaTeX Formatting Issues Catalogue

## Issue Categories

### 1. Unconverted `---` horizontal rules
Many chapters still have raw `---` lines that should be `\bigskip` or removed.
Files affected: ch01, ch03, ch05, ch06, ch07, ch08, ch11, ch12, ch13, ch14, ch15, ch16, ch17

### 2. Raw `$$` display math in chapter02.tex
chapter02 has 16 instances of raw `$$` lines (standalone `$$` open/close) that weren't
converted to `\[...\]`.

### 3. Raw markdown bold (`**text**`) not converted to `\textbf{}`
Multiple chapters have `**text**` patterns in non-math text that the converter missed.
These are typically bold labels like `**At $x_0^* = 0$:**` or `**Case 1: ...**`.
The issue: these lines start with `**` but are not theorem/definition/proof markers,
so the converter passes them through process_line() which handles `**` ONLY within
non-math segments. However, these `**text $math$ text**` patterns confuse the bold
regex because the `*` crosses math boundaries.
Files affected: ch02, ch03, ch05, ch06, ch09

### 4. Unbalanced proof environment in chapter15.tex
begin{proof}=4, end{proof}=5 → one extra \end{proof}
Line 399 has \end{proof} without a matching \begin{proof}.
This is because lines ~262-398 are a proof sketch section that should have
\begin{proof} before it but the converter missed the "Proof sketch" start.
The source has `### 15.3.2 Proof Sketch` as a subsection title (correctly converted
to \subsection), and then later there's inline proof content ending with a
$\square$ marker that generated \end{proof} without a corresponding begin.

### 5. Broken list environments
Some multi-line list items create separate \begin{itemize}/\end{itemize} pairs
for each item (opening and closing the list for every bullet point, instead of
keeping one list open). This happens when continuation lines of a list item are
not indented, causing the list closer to fire prematurely.
Most visible in chapter15.tex around line 280-289.
