# Garden of Forking Paths

Nonlinear text navigation and adaptive reading order. The core idea: linear text
forces authors to serialize what is inherently a graph of interconnected ideas.
Hyperlinks are a poor solution -- they rupture flow. We want *seamless* navigation
through a text along different paths.

## The Problem

A static DAG over "idea nodes" is insufficient. Two readers at the same node can
have different epistemic states depending on their path. The graph structure alone
doesn't capture this.

## The Formalism

Following Doignon & Falmagne's *knowledge spaces*:

- Each text chunk (node) **teaches** a set of concepts and **requires** a set of
  prerequisite concepts.
- The reader's state is their accumulated knowledge set.
- Available transitions are computed dynamically: a node is available iff all its
  prerequisites are in the reader's current knowledge set.
- Different readers traverse different induced graphs from the same underlying material.

This connects to Binmore's small/large world distinction: linear text is a small
world (author pre-committed to an order). This system puts the reader in a structured
large world -- you cross bridges when you come to them, and the order shapes what
things mean to you.

## Key Design Problems

1. **Annotation**: tagging each text chunk with what it teaches and what it requires
2. **Convergence**: when paths rejoin, readers arrive with different preparation --
   may need bridging summaries
3. **Interface**: spatial visualization (DAG rendered as cards/tiles) + adaptive
   sequencing (online topological sort personalized to reader choices)
4. **Extraction**: can we recover this structure from existing linear text? (LLM-assisted)

## How to Run

TBD -- project is in early design phase.
