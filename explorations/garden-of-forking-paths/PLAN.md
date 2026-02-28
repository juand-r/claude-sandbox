# Plan

## Phase 1: Core Data Model [DONE]

- [x] Define the knowledge space data structures:
  - `Concept`: atomic unit of knowledge
  - `TextNode`: chunk of text with `teaches: Set[Concept]`, `requires: Set[Concept]`, and content
  - `ReaderState`: accumulated `Set[Concept]`, reading history
- [x] Implement the dynamic graph traversal logic:
  - Given a `ReaderState`, compute available next nodes
  - Update state after reading a node
  - Detect when convergence points need bridging summaries
- [x] Bayesian reasoning toy example (two paths, convergence)

## Phase 2: A Concrete Example [DONE]

- [x] Eigenvalues/eigenvectors text with 10 nodes, 16 concepts
  - Multiple entry points, convergence at PCA (requires spectral theorem path)
  - Applications branch: quantum mechanics, PCA, stability (reader chooses)
- [x] Manual annotation in `texts/eigenvalues_ks.json`
- [x] Verified: both formal-first and geometric-first paths work correctly
- [ ] Try more texts (math/physics chapters) -- pick from real textbooks

## Phase 3: Extraction Pipeline (LLM-assisted)

- [x] Built `extractor.py`: segmentation + concept annotation via Claude API
- [x] Save/load knowledge spaces to/from JSON
- [ ] Test with API key (need ANTHROPIC_API_KEY in environment)
- [ ] Compare LLM-extracted structure to manual annotation
- [ ] Iterate on prompts/approach

## Phase 4: Interface / UI [MVP DONE]

- [x] Flask web app with split-panel layout (graph + reader)
- [x] SVG graph visualization with layered layout
- [x] Node states: locked, available, visited, current
- [x] Interactive navigation: click nodes or use choice buttons
- [x] Concept tracking display
- [ ] Polish: better graph layout, zoom/pan, animations
- [ ] Bridging summaries at convergence points
- [ ] Mobile support

## Phase 5: Educational Curriculum Application [DEFERRED]

Tabled until Phases 2-4 prove the formalism works on real material.
Ideas for later:
- Apply to a full course (e.g., linear algebra, probability)
- Track student knowledge across sessions
- Assessment: detect gaps, suggest review
- Spaced repetition integration

## Open Questions

- What granularity for text chunks? Paragraph? Section? Sentence?
- How to handle concepts that are partially taught (introduced but not fully developed)?
- Is the knowledge space always a clean antimatroid, or do real texts violate the axioms?
- How to represent "depth" -- reading the same node twice with more background yields
  deeper understanding?
- What about circular dependencies / mutually illuminating ideas?
