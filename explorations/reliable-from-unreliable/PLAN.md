# Plan

## Phase 1: Survey of relevant fields and ideas
- [x] Von Neumann's 1956 paper summary
- [x] Comprehensive survey of fields that address "reliable from unreliable"
- [x] Map each field's ideas to the LLM-as-building-block setting
- [x] Identify which ideas transfer cleanly and which don't (and why)

## Phase 2: Circuit-level construction (Merrill -> Boolean -> redundancy -> NN)
- [x] Boolean circuit framework (gates, wires, evaluation, batch fault injection)
- [x] Fixed-point arithmetic subcircuits (adder, constant multiplier)
- [x] Compile perceptron to Boolean circuit
- [x] Von Neumann redundancy transformation
- [x] Fault tolerance experiment: original vs. redundant at various fault rates
- [ ] Extend to small MLP (2-layer, XOR or similar)
- [ ] Extend to tiny 1-head attention mechanism
- [ ] Map redundant circuit back to neural network and characterize its structure
- [ ] Add permanent knockout mode (vs. transient faults)

## Phase 3: Formalization
- [ ] Define what "unreliable component" means for LLMs (error model)
- [ ] Define what "reliable system" means (what guarantees, for what tasks)
- [ ] Identify which theoretical frameworks are most promising

## Phase 4: Simulation of higher-level patterns
- [ ] Demonstrate with LLM-like failure modes (not just random bit flips)
- [ ] Voting / ensemble simulation
- [ ] Generate-and-verify simulation

## Phase 5: Practical patterns
- [ ] Concrete patterns for building reliable LLM-based systems
- [ ] When each pattern works and when it breaks down
