# Plan

## Phase 1: Core Data Model

- [ ] Define the knowledge space data structures:
  - `Concept`: atomic unit of knowledge
  - `TextNode`: chunk of text with `teaches: Set[Concept]`, `requires: Set[Concept]`, and content
  - `ReaderState`: accumulated `Set[Concept]`, reading history
- [ ] Implement the dynamic graph traversal logic:
  - Given a `ReaderState`, compute available next nodes
  - Update state after reading a node
  - Detect when convergence points need bridging summaries

## Phase 2: A Concrete Example

- [ ] Take a real text (short essay, textbook chapter, or write one ourselves) and
      manually annotate it with the knowledge space structure
- [ ] Verify the formalism works: walk through several paths, check that the
      prerequisite logic produces sensible results
- [ ] Identify edge cases and refine the model

## Phase 3: Extraction Pipeline (LLM-assisted)

- [ ] Given a linear text, use an LLM to:
  - Segment into text chunks
  - Identify concepts taught and required by each chunk
  - Produce a knowledge space annotation
- [ ] Compare LLM-extracted structure to manual annotation
- [ ] Iterate on prompts/approach

## Phase 4: Interface / UI

- [ ] Spatial view: render the induced graph, show current position, available paths,
      explored/unexplored regions
- [ ] Reader view: present text adaptively, show branching choices, handle convergence
      with bridging summaries
- [ ] Technology choice TBD (web-based likely makes sense)

## Phase 5: Educational Curriculum Application

- [ ] Apply to a real curriculum or course material
- [ ] Explore how different learning paths through the same material lead to different
      understanding
- [ ] Think about assessment: does the system know what the reader knows well enough
      to suggest review or flag gaps?

## Open Questions

- What granularity for text chunks? Paragraph? Section? Sentence?
- How to handle concepts that are partially taught (introduced but not fully developed)?
- Is the knowledge space always a clean antimatroid, or do real texts violate the axioms?
- How to represent "depth" -- reading the same node twice with more background yields
  deeper understanding?
- What about circular dependencies / mutually illuminating ideas?
