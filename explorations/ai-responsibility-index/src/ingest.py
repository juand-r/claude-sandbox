"""
Document Ingestion Module

Parses PDF and XML documents into a list of text chunks with metadata.
Each chunk carries its source information (file, page/section) for citation.

Supported formats:
- PDF: via PyMuPDF (fitz)
- XML: via lxml (handles generic XML and common ESG reporting formats like XBRL)
"""

import re
from dataclasses import dataclass
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from lxml import etree
except ImportError:
    etree = None


@dataclass
class Chunk:
    """A piece of text extracted from a document, with provenance metadata."""
    text: str
    source_file: str
    page: int | None = None        # PDF page number (1-indexed)
    section: str | None = None     # section heading if detected
    chunk_index: int = 0           # position within the document
    metadata: dict = None          # additional metadata

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


def chunk_text(text: str, max_chars: int = 1500, overlap: int = 200) -> list[str]:
    """
    Split text into overlapping chunks, preferring to break at paragraph boundaries.

    Args:
        text: The text to split.
        max_chars: Target maximum characters per chunk.
        overlap: Number of characters to overlap between chunks.

    Returns:
        List of text strings.
    """
    if len(text) <= max_chars:
        return [text] if text.strip() else []

    # Split on double newlines (paragraph boundaries) first
    paragraphs = re.split(r'\n\s*\n', text)

    chunks = []
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # If adding this paragraph exceeds the limit, finalize current chunk
        if current and len(current) + len(para) + 2 > max_chars:
            chunks.append(current.strip())
            # Keep overlap from end of current chunk
            if overlap > 0 and len(current) > overlap:
                current = current[-overlap:] + "\n\n" + para
            else:
                current = para
        else:
            current = current + "\n\n" + para if current else para

    if current.strip():
        chunks.append(current.strip())

    # Handle case where a single paragraph is longer than max_chars
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > max_chars * 1.5:
            # Force-split long chunks at sentence boundaries
            sentences = re.split(r'(?<=[.!?])\s+', chunk)
            sub = ""
            for sent in sentences:
                if sub and len(sub) + len(sent) + 1 > max_chars:
                    final_chunks.append(sub.strip())
                    sub = sent
                else:
                    sub = sub + " " + sent if sub else sent
            if sub.strip():
                final_chunks.append(sub.strip())
        else:
            final_chunks.append(chunk)

    return final_chunks


def ingest_pdf(filepath: str | Path, max_chars: int = 1500, overlap: int = 200) -> list[Chunk]:
    """
    Parse a PDF file into text chunks with page metadata.

    Uses PyMuPDF to extract text page by page, then chunks each page.
    Attempts to detect section headings from font size changes.

    Args:
        filepath: Path to the PDF file.
        max_chars: Target max characters per chunk.
        overlap: Overlap between chunks.

    Returns:
        List of Chunk objects.
    """
    if fitz is None:
        raise ImportError("PyMuPDF (fitz) is required for PDF ingestion. Install with: pip install pymupdf")

    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"PDF file not found: {filepath}")

    doc = fitz.open(str(filepath))
    all_chunks = []
    chunk_idx = 0
    current_section = None

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Try to detect section headings via text blocks with larger fonts
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        page_text_parts = []

        for block in blocks:
            if block.get("type") != 0:  # skip non-text blocks (images, etc.)
                continue
            for line in block.get("lines", []):
                line_text = ""
                max_font_size = 0
                for span in line.get("spans", []):
                    line_text += span.get("text", "")
                    max_font_size = max(max_font_size, span.get("size", 0))

                line_text = line_text.strip()
                if not line_text:
                    continue

                # Heuristic: lines with larger font size and short length are likely headings
                if max_font_size > 13 and len(line_text) < 120 and not line_text.endswith('.'):
                    current_section = line_text

                page_text_parts.append(line_text)

        page_text = "\n".join(page_text_parts)
        if not page_text.strip():
            continue

        text_chunks = chunk_text(page_text, max_chars=max_chars, overlap=overlap)
        for text in text_chunks:
            all_chunks.append(Chunk(
                text=text,
                source_file=str(filepath),
                page=page_num + 1,  # 1-indexed
                section=current_section,
                chunk_index=chunk_idx,
            ))
            chunk_idx += 1

    doc.close()
    return all_chunks


def ingest_xml(filepath: str | Path, max_chars: int = 1500, overlap: int = 200) -> list[Chunk]:
    """
    Parse an XML file into text chunks with section metadata.

    Handles:
    - Generic XML: extracts text content from all elements
    - XBRL: extracts text from narrative/textual elements (common in ESG filings)

    Args:
        filepath: Path to the XML file.
        max_chars: Target max characters per chunk.
        overlap: Overlap between chunks.

    Returns:
        List of Chunk objects.
    """
    if etree is None:
        raise ImportError("lxml is required for XML ingestion. Install with: pip install lxml")

    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"XML file not found: {filepath}")

    tree = etree.parse(str(filepath))
    root = tree.getroot()

    # Detect if this is XBRL/iXBRL by checking namespaces
    # Collect all namespaces including from child elements (iXBRL has ns on root)
    all_ns = set(root.nsmap.values())
    for elem in root.iter():
        all_ns.update(elem.nsmap.values())
    ns_str = " ".join(str(ns) for ns in all_ns if ns)
    is_xbrl = ('xbrl' in ns_str.lower() or 'efrag.org' in ns_str.lower()
               or 'fasb.org' in ns_str.lower() or 'ifrs.org' in ns_str.lower())

    sections = _extract_xml_sections(root, is_xbrl)

    all_chunks = []
    chunk_idx = 0

    for section_name, text in sections:
        if not text.strip():
            continue
        text_chunks = chunk_text(text, max_chars=max_chars, overlap=overlap)
        for chunk_text_str in text_chunks:
            all_chunks.append(Chunk(
                text=chunk_text_str,
                source_file=str(filepath),
                page=None,
                section=section_name,
                chunk_index=chunk_idx,
                metadata={"format": "xbrl" if is_xbrl else "xml"},
            ))
            chunk_idx += 1

    return all_chunks


def _get_all_text(elem) -> str:
    """
    Recursively extract all text from an element and its children.
    Handles cases where HTML markup is embedded as child elements in XBRL.
    """
    parts = []
    if elem.text and elem.text.strip():
        parts.append(elem.text.strip())
    for child in elem:
        parts.append(_get_all_text(child))
        if child.tail and child.tail.strip():
            parts.append(child.tail.strip())
    return " ".join(p for p in parts if p)


# Tag local names that typically contain narrative disclosures in XBRL/iXBRL
_NARRATIVE_PATTERNS = {
    'explanation', 'textblock', 'description', 'disclosure',
    'policy', 'narrative', 'discussion', 'overview',
}

# Tag names that are structural containers, not content elements
_CONTAINER_TAGS = {
    'xbrl', 'html', 'head', 'body', 'div', 'span', 'section', 'article',
    'header', 'footer', 'nav', 'main', 'table', 'tr', 'td', 'th', 'thead',
    'tbody', 'ul', 'ol', 'li', 'p', 'a', 'b', 'i', 'em', 'strong',
    'resources', 'context', 'entity', 'period', 'identifier', 'hidden',
    'startdate', 'enddate', 'title', 'style', 'script', 'link', 'meta',
}


def _is_narrative_tag(tag: str) -> bool:
    """Check if an element's local name suggests narrative content."""
    tag_lower = tag.lower()
    return any(p in tag_lower for p in _NARRATIVE_PATTERNS)


def _is_container_tag(tag: str) -> bool:
    """Check if a tag is a structural container rather than a content element."""
    return tag.lower() in _CONTAINER_TAGS


def _extract_xml_sections(root, is_xbrl: bool) -> list[tuple[str, str]]:
    """
    Walk an XML tree and extract (section_name, text) pairs.

    For XBRL/iXBRL, focuses on textual/narrative elements (which contain the
    actual disclosures). Extracts all text recursively from each element to
    handle embedded HTML markup.

    For generic XML, extracts all text content grouped by top-level elements.
    """
    sections = []

    if is_xbrl:
        # Pass 1: Collect ix:nonNumeric elements (iXBRL)
        # Pass 2: Collect elements matching narrative tag patterns
        # No fallback on container elements -- avoids duplicating content
        seen_texts = set()

        for elem in root.iter():
            tag = etree.QName(elem.tag).localname if '}' in elem.tag else elem.tag

            # iXBRL: extract ix:nonNumeric elements with narrative content
            if tag == 'nonNumeric':
                full_text = _get_all_text(elem)
                clean = _strip_html(full_text)
                if clean and len(clean) > 100 and clean not in seen_texts:
                    # Use the 'name' attribute (e.g., esrs:DisclosureOf...)
                    name = elem.get('name', tag)
                    if ':' in name:
                        name = name.split(':', 1)[1]
                    sections.append((name, clean))
                    seen_texts.add(clean)
                continue

            # Skip known container/structural tags
            if _is_container_tag(tag):
                continue

            # Traditional XBRL: extract narrative-tagged elements
            if _is_narrative_tag(tag):
                full_text = _get_all_text(elem)
                clean = _strip_html(full_text)
                if clean and len(clean) > 100 and clean not in seen_texts:
                    sections.append((tag, clean))
                    seen_texts.add(clean)
                continue

            # Fallback: only for leaf-ish elements (few or no children)
            # This catches elements with unexpected tag names but real content,
            # while avoiding container elements that aggregate child text.
            n_children = len(list(elem))
            if n_children <= 3:
                full_text = _get_all_text(elem)
                clean = _strip_html(full_text) if full_text else ""
                if clean and len(clean) > 100 and clean not in seen_texts:
                    sections.append((tag, clean))
                    seen_texts.add(clean)

        # If XBRL extraction found nothing (e.g., unusual structure),
        # fall back to collecting text from non-container elements with
        # substantial direct text content
        if not sections:
            for elem in root.iter():
                tag = etree.QName(elem.tag).localname if '}' in elem.tag else elem.tag
                if _is_container_tag(tag):
                    continue
                text = elem.text
                if text and len(text.strip()) > 100:
                    clean = _strip_html(text.strip())
                    if clean and clean not in seen_texts:
                        sections.append((tag, clean))
                        seen_texts.add(clean)
    else:
        # Generic XML: group by top-level children
        for child in root:
            tag = etree.QName(child.tag).localname if '}' in child.tag else child.tag
            # Collect all text recursively under this element
            full_text = _get_all_text(child)
            if full_text and len(full_text.strip()) > 50:
                sections.append((tag, full_text))

    return sections


def _strip_html(text: str) -> str:
    """Remove HTML tags from text (XBRL often embeds HTML in text blocks)."""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()


def ingest(filepath: str | Path, max_chars: int = 1500, overlap: int = 200) -> list[Chunk]:
    """
    Auto-detect file type and ingest accordingly.

    Args:
        filepath: Path to PDF or XML file.
        max_chars: Target max characters per chunk.
        overlap: Overlap between chunks.

    Returns:
        List of Chunk objects.
    """
    filepath = Path(filepath)
    suffix = filepath.suffix.lower()

    if suffix == '.pdf':
        return ingest_pdf(filepath, max_chars, overlap)
    elif suffix in ('.xml', '.xbrl', '.html', '.xhtml'):
        return ingest_xml(filepath, max_chars, overlap)
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Supported: .pdf, .xml, .xbrl")
