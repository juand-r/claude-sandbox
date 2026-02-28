"""
Knowledge space model for nonlinear text navigation.

Based on Doignon & Falmagne's knowledge space theory. Each text node
teaches concepts and requires concepts. The reader's state is their
accumulated concept set. Available transitions are computed dynamically.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Concept:
    """An atomic unit of knowledge."""
    id: str
    label: str
    description: str = ""

    def __repr__(self):
        return f"Concept({self.id!r})"


@dataclass
class TextNode:
    """A chunk of text with knowledge annotations."""
    id: str
    title: str
    content: str
    teaches: frozenset[Concept] = field(default_factory=frozenset)
    requires: frozenset[Concept] = field(default_factory=frozenset)

    def is_available(self, knowledge: frozenset[Concept]) -> bool:
        """Can the reader access this node given their current knowledge?"""
        return self.requires.issubset(knowledge)

    def __repr__(self):
        return f"TextNode({self.id!r}, teaches={len(self.teaches)}, requires={len(self.requires)})"


@dataclass
class ReaderState:
    """Tracks what the reader knows and where they've been."""
    knowledge: frozenset[Concept] = field(default_factory=frozenset)
    history: list[str] = field(default_factory=list)  # node ids in order visited

    def read(self, node: TextNode) -> "ReaderState":
        """Return new state after reading a node."""
        if not node.is_available(self.knowledge):
            missing = node.requires - self.knowledge
            raise ValueError(
                f"Cannot read {node.id!r}: missing concepts "
                f"{[c.id for c in missing]}"
            )
        return ReaderState(
            knowledge=self.knowledge | node.teaches,
            history=self.history + [node.id],
        )

    def available_nodes(self, nodes: list[TextNode]) -> list[TextNode]:
        """Which nodes can the reader access now (excluding already read)?"""
        visited = set(self.history)
        return [
            n for n in nodes
            if n.id not in visited and n.is_available(self.knowledge)
        ]


@dataclass
class KnowledgeSpace:
    """A collection of text nodes forming a navigable knowledge space."""
    nodes: dict[str, TextNode] = field(default_factory=dict)
    # Optional: entry points (nodes with no prerequisites)
    # These are computed, not stored.

    def add_node(self, node: TextNode):
        self.nodes[node.id] = node

    def entry_points(self) -> list[TextNode]:
        """Nodes with no prerequisites -- where a reader can start."""
        return [n for n in self.nodes.values() if not n.requires]

    def available_from(self, state: ReaderState) -> list[TextNode]:
        """What can this reader read next?"""
        return state.available_nodes(list(self.nodes.values()))

    def concepts_taught(self) -> frozenset[Concept]:
        """All concepts across all nodes."""
        result: set[Concept] = set()
        for node in self.nodes.values():
            result |= node.teaches
        return frozenset(result)

    def concepts_required(self) -> frozenset[Concept]:
        """All prerequisite concepts across all nodes."""
        result: set[Concept] = set()
        for node in self.nodes.values():
            result |= node.requires
        return frozenset(result)

    def unreachable_concepts(self) -> frozenset[Concept]:
        """Concepts required but never taught -- indicates a gap."""
        return self.concepts_required() - self.concepts_taught()

    def convergence_points(self) -> list[TextNode]:
        """Nodes reachable via multiple distinct prerequisite paths.

        These are the nodes where readers with different histories converge
        and may need bridging summaries.
        """
        result = []
        for node in self.nodes.values():
            if len(node.requires) == 0:
                continue
            # A node is a convergence point if its prerequisites are taught
            # by more than one distinct set of nodes (i.e., there are multiple
            # minimal sets of prior nodes that satisfy its requirements).
            # Simplified heuristic: if prerequisites come from 2+ different nodes.
            teaching_nodes = set()
            for concept in node.requires:
                for other in self.nodes.values():
                    if concept in other.teaches:
                        teaching_nodes.add(other.id)
            if len(teaching_nodes) > 1:
                result.append(node)
        return result

    def bridging_summary_needed(
        self, state: ReaderState, target: TextNode
    ) -> Optional[list[Concept]]:
        """Check if reader needs a bridging summary before reading target.

        Returns list of concepts the reader has but that were taught by nodes
        they skipped -- these concepts may need contextual grounding.
        Returns None if no bridging is needed.
        """
        if not target.is_available(state.knowledge):
            return None  # can't read it at all

        # Find concepts the target requires that the reader has,
        # but that they learned "indirectly" (from a different path than
        # the most direct one). This is a heuristic.
        # For now: concepts required by target that were taught by nodes
        # NOT in the reader's history.
        visited = set(state.history)
        bridging_concepts = []
        for concept in target.requires:
            # Which nodes teach this concept?
            teachers = [
                n for n in self.nodes.values()
                if concept in n.teaches
            ]
            # If none of the teachers are in the reader's history,
            # the reader got this concept from somewhere unexpected
            # (or it's a starting concept). Flag it.
            if teachers and not any(t.id in visited for t in teachers):
                bridging_concepts.append(concept)

        return bridging_concepts if bridging_concepts else None

    def validate(self) -> list[str]:
        """Check the knowledge space for structural issues."""
        issues = []

        unreachable = self.unreachable_concepts()
        if unreachable:
            issues.append(
                f"Concepts required but never taught: "
                f"{[c.id for c in unreachable]}"
            )

        if not self.entry_points():
            issues.append("No entry points (all nodes have prerequisites)")

        # Check for circular dependencies (shouldn't happen if it's a proper
        # knowledge space, but worth verifying)
        # Simple check: can we reach all nodes from entry points?
        reachable_ids: set[str] = set()
        state = ReaderState()
        frontier = self.entry_points()
        while frontier:
            node = frontier[0]
            frontier = frontier[1:]
            if node.id in reachable_ids:
                continue
            reachable_ids.add(node.id)
            state = state.read(node)
            frontier.extend(self.available_from(state))

        unreachable_nodes = set(self.nodes.keys()) - reachable_ids
        if unreachable_nodes:
            issues.append(
                f"Nodes unreachable from entry points: {unreachable_nodes}"
            )

        return issues
