# Sentence-to-Recipe Translator

## Goal
Translate any sentence into a culinary recipe based on its meaning.

## Requirements
- [x] Accept any sentence as input
- [x] Understand abstract concepts (love, anger) and specific instructions ("cook for 1 hour")
- [x] Output step-by-step format: ingredients → steps → assembly
- [x] Include culinary keywords (lavender, spices, etc.)
- [x] Allow for "unintended results" based on input and user state

## Approach
Use LLM to interpret sentence meaning and generate a thematic recipe. The LLM handles:
1. Semantic analysis of the input
2. Mapping concepts to culinary elements (emotions → flavors, actions → techniques)
3. Generating coherent recipe structure

## Design
- CLI tool with simple interface
- Reuse LLM backends from prompt-generator exploration
- Single Python file for simplicity

## Status
- [x] Create directory structure
- [x] Implement core translator
- [x] Test with various inputs
- [x] Write README
- [x] Commit and push
