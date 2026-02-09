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

    # Detect if this is XBRL by checking namespace
    nsmap = root.nsmap
    is_xbrl = any('xbrl' in str(ns).lower() for ns in nsmap.values())

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


def _extract_xml_sections(root, is_xbrl: bool) -> list[tuple[str, str]]:
    """
    Walk an XML tree and extract (section_name, text) pairs.

    For XBRL, focuses on textual/narrative elements (which contain the actual
    disclosures). For generic XML, extracts all text content grouped by
    top-level elements.
    """
    sections = []

    if is_xbrl:
        # XBRL: look for elements with substantial text content
        # These are typically narrative disclosures
        for elem in root.iter():
            text = elem.text
            if text and len(text.strip()) > 100:
                # Use the element's local name as section identifier
                tag = etree.QName(elem.tag).localname if '}' in elem.tag else elem.tag
                # Clean HTML that may be embedded in XBRL text blocks
                clean = _strip_html(text.strip())
                if clean:
                    sections.append((tag, clean))
    else:
        # Generic XML: group by top-level children
        for child in root:
            tag = etree.QName(child.tag).localname if '}' in child.tag else child.tag
            # Collect all text recursively under this element
            texts = []
            for elem in child.iter():
                if elem.text and elem.text.strip():
                    texts.append(elem.text.strip())
                if elem.tail and elem.tail.strip():
                    texts.append(elem.tail.strip())
            if texts:
                sections.append((tag, "\n\n".join(texts)))

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
