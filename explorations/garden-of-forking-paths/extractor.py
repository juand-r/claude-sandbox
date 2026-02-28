"""
LLM-assisted extraction of knowledge space structure from linear text.

Given a linear text, uses Claude to:
1. Segment into meaningful chunks
2. Identify concepts each chunk teaches and requires
3. Produce a KnowledgeSpace object

Requires ANTHROPIC_API_KEY in environment.
"""

import json
import os
import sys
from typing import Any

import anthropic

from knowledge_space import Concept, TextNode, KnowledgeSpace


MODEL = "claude-sonnet-4-20250514"

SEGMENTATION_PROMPT = """\
You are analyzing a text to break it into self-contained "idea chunks" for a
nonlinear reading system. Each chunk should:

- Contain ONE main idea, argument, definition, or example
- Be understandable on its own (given its prerequisites)
- Be roughly paragraph-to-subsection sized (not single sentences, not entire sections)

Given the following text, segment it into chunks. For each chunk, provide:
- id: a short snake_case identifier
- title: a brief descriptive title
- content: the exact text of the chunk (preserve original wording)

Return valid JSON with this structure:
{
  "chunks": [
    {"id": "...", "title": "...", "content": "..."},
    ...
  ]
}

TEXT:
"""

ANNOTATION_PROMPT = """\
You are annotating text chunks for a knowledge space system. Each chunk TEACHES
certain concepts (ideas the reader learns by reading it) and REQUIRES certain
concepts (ideas the reader must already know to understand it).

Concepts should be:
- Atomic: one clear idea per concept
- Named with short snake_case identifiers
- Described briefly

IMPORTANT RULES:
- A chunk's "requires" should ONLY list concepts that are taught by OTHER chunks.
  Do not require general world knowledge or things not covered in this text.
- Entry points (first things a reader encounters) should have empty requires.
- Be precise: if chunk B uses a term defined in chunk A, then B requires that concept
  and A teaches it.
- A concept taught by one chunk can be required by many chunks.
- A chunk can teach multiple concepts and require multiple concepts.

Here are the chunks:
{chunks_json}

Return valid JSON with this structure:
{{
  "concepts": [
    {{"id": "...", "label": "...", "description": "..."}},
    ...
  ],
  "annotations": [
    {{"chunk_id": "...", "teaches": ["concept_id", ...], "requires": ["concept_id", ...]}},
    ...
  ]
}}
"""


def _call_claude(prompt: str) -> str:
    """Call Claude and return the text response."""
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def _parse_json_response(text: str) -> dict[str, Any]:
    """Extract JSON from Claude's response, handling markdown code blocks."""
    # Strip markdown code fences if present
    text = text.strip()
    if text.startswith("```"):
        # Remove first line (```json or ```) and last line (```)
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])
    return json.loads(text)


def segment_text(text: str) -> list[dict[str, str]]:
    """Segment a linear text into idea chunks using Claude."""
    prompt = SEGMENTATION_PROMPT + text
    response = _call_claude(prompt)
    data = _parse_json_response(response)
    return data["chunks"]


def annotate_chunks(chunks: list[dict[str, str]]) -> dict[str, Any]:
    """Annotate chunks with teaches/requires concepts using Claude."""
    chunks_json = json.dumps(chunks, indent=2)
    prompt = ANNOTATION_PROMPT.format(chunks_json=chunks_json)
    response = _call_claude(prompt)
    return _parse_json_response(response)


def extract_knowledge_space(text: str) -> KnowledgeSpace:
    """Full pipeline: text -> segmented chunks -> annotated knowledge space."""
    print("Step 1: Segmenting text into chunks...")
    chunks = segment_text(text)
    print(f"  Found {len(chunks)} chunks:")
    for c in chunks:
        print(f"    - {c['id']}: {c['title']}")

    print("\nStep 2: Annotating chunks with concepts...")
    annotations = annotate_chunks(chunks)
    print(f"  Found {len(annotations['concepts'])} concepts:")
    for c in annotations["concepts"]:
        print(f"    - {c['id']}: {c['label']}")

    print("\nStep 3: Building knowledge space...")
    # Build concept lookup
    concepts = {}
    for c in annotations["concepts"]:
        concepts[c["id"]] = Concept(
            id=c["id"],
            label=c["label"],
            description=c.get("description", ""),
        )

    # Build chunk lookup
    chunk_lookup = {c["id"]: c for c in chunks}

    # Build knowledge space
    ks = KnowledgeSpace()
    for ann in annotations["annotations"]:
        chunk = chunk_lookup[ann["chunk_id"]]
        teaches = frozenset(
            concepts[cid] for cid in ann["teaches"] if cid in concepts
        )
        requires = frozenset(
            concepts[cid] for cid in ann["requires"] if cid in concepts
        )
        node = TextNode(
            id=chunk["id"],
            title=chunk["title"],
            content=chunk["content"],
            teaches=teaches,
            requires=requires,
        )
        ks.add_node(node)

    # Validate
    issues = ks.validate()
    if issues:
        print("\n  Validation issues:")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("  No validation issues.")

    print(f"\n  Entry points: {[n.id for n in ks.entry_points()]}")
    print(f"  Convergence points: {[n.id for n in ks.convergence_points()]}")

    return ks


def save_knowledge_space(ks: KnowledgeSpace, path: str):
    """Serialize a knowledge space to JSON for later use."""
    data = {
        "nodes": [
            {
                "id": node.id,
                "title": node.title,
                "content": node.content,
                "teaches": [{"id": c.id, "label": c.label, "description": c.description} for c in node.teaches],
                "requires": [{"id": c.id, "label": c.label, "description": c.description} for c in node.requires],
            }
            for node in ks.nodes.values()
        ]
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved knowledge space to {path}")


def load_knowledge_space(path: str) -> KnowledgeSpace:
    """Load a knowledge space from JSON."""
    with open(path) as f:
        data = json.load(f)

    # Collect all unique concepts
    concepts: dict[str, Concept] = {}
    for node_data in data["nodes"]:
        for c in node_data["teaches"] + node_data["requires"]:
            if c["id"] not in concepts:
                concepts[c["id"]] = Concept(
                    id=c["id"],
                    label=c["label"],
                    description=c.get("description", ""),
                )

    ks = KnowledgeSpace()
    for node_data in data["nodes"]:
        node = TextNode(
            id=node_data["id"],
            title=node_data["title"],
            content=node_data["content"],
            teaches=frozenset(concepts[c["id"]] for c in node_data["teaches"]),
            requires=frozenset(concepts[c["id"]] for c in node_data["requires"]),
        )
        ks.add_node(node)

    return ks


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <text_file> [output.json]")
        print("  Requires ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)

    text_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    with open(text_file) as f:
        text = f.read()

    ks = extract_knowledge_space(text)

    if output_file:
        save_knowledge_space(ks, output_file)
