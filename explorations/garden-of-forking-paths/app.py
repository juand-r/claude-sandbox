"""
Web UI for Garden of Forking Paths.

Serves a single-page app that visualizes a knowledge space as a graph
and lets the reader navigate it interactively.
"""

import json
import sys

from flask import Flask, jsonify, render_template, request

from extractor import load_knowledge_space
from knowledge_space import ReaderState, Concept

app = Flask(__name__)

# Global knowledge space -- loaded once at startup
KS = None


def _concept_to_dict(c: Concept) -> dict:
    return {"id": c.id, "label": c.label, "description": c.description}


def _build_graph_data() -> dict:
    """Build the full graph structure for visualization."""
    nodes = []
    edges = []

    for node in KS.nodes.values():
        nodes.append({
            "id": node.id,
            "title": node.title,
            "teaches": [_concept_to_dict(c) for c in node.teaches],
            "requires": [_concept_to_dict(c) for c in node.requires],
            "is_entry": len(node.requires) == 0,
        })

    # Edges: from any node that teaches a concept to any node that requires it
    for target in KS.nodes.values():
        for concept in target.requires:
            for source in KS.nodes.values():
                if concept in source.teaches:
                    edges.append({
                        "source": source.id,
                        "target": target.id,
                        "concept": concept.id,
                    })

    return {"nodes": nodes, "edges": edges}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/graph")
def graph():
    """Return the full graph structure."""
    return jsonify(_build_graph_data())


@app.route("/api/node/<node_id>")
def node_detail(node_id):
    """Return full content for a node."""
    node = KS.nodes.get(node_id)
    if not node:
        return jsonify({"error": "Node not found"}), 404
    return jsonify({
        "id": node.id,
        "title": node.title,
        "content": node.content,
        "teaches": [_concept_to_dict(c) for c in node.teaches],
        "requires": [_concept_to_dict(c) for c in node.requires],
    })


@app.route("/api/available", methods=["POST"])
def available():
    """Given a reader's history, return available next nodes."""
    data = request.json
    history = data.get("history", [])

    # Rebuild reader state from history
    state = ReaderState()
    for node_id in history:
        node = KS.nodes.get(node_id)
        if node:
            state = state.read(node)

    available_nodes = KS.available_from(state)
    return jsonify({
        "available": [n.id for n in available_nodes],
        "knowledge": [_concept_to_dict(c) for c in state.knowledge],
    })


if __name__ == "__main__":
    ks_path = sys.argv[1] if len(sys.argv) > 1 else "texts/eigenvalues_ks.json"
    KS = load_knowledge_space(ks_path)
    print(f"Loaded knowledge space: {len(KS.nodes)} nodes, "
          f"{len(KS.concepts_taught())} concepts")
    app.run(debug=True, port=5000)
