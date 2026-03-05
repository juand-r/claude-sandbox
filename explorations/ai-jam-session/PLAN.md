# AI Jam Session -- Plan

## What
Five AI agents improvise music together in a round-based jam session. Each agent controls one instrument and uses an LLM to decide what to play, reacting to what all other agents played in previous rounds.

## The Band
- **Piano** -- harmony, comping, chords
- **Bass** -- groove, walking lines, foundation
- **Drums** -- rhythm patterns (MIDI percussion channel 10)
- **Saxophone** -- melody, lead lines, soloing
- **Electric Guitar** -- flexible: rhythm comping, lead, bridges jazz and rock

## Architecture (Option 2: Parallel with Shared Context)

```
Round N:
  1. Build context: all measures from rounds 1..N-1 for all instruments
  2. Send context to all 5 agents IN PARALLEL
  3. Each agent returns MIDI data for their measure N
  4. Collect, validate, append to shared history
  5. Repeat for N rounds
```

### Key Design Decisions
- **MIDI representation for LLM I/O**: The LLM needs a text-friendly way to specify notes. Options:
  - Simple text format: `C4 0.5 0.8` (pitch, duration in beats, velocity 0-1). One note per line.
  - This is simpler than raw MIDI bytes or ABC notation and easy to parse.
- **Tempo/Key/Style**: Set at the start of the jam. Could evolve (e.g., key changes) but start fixed.
- **Rounds = measures**: Each round, each agent generates one measure of music.
- **LLM backends**: Support both OpenAI and Anthropic APIs. Configurable per agent or globally.

## File Structure
```
explorations/ai-jam-session/
  README.md          -- what this is, how to run
  PLAN.md            -- this file
  jam.py             -- main entry point, orchestrates the session
  agents.py          -- Agent class, LLM interaction, prompt construction
  midi_utils.py      -- parse text->MIDI, build final MIDI file
  config.py          -- session config (tempo, key, num_rounds, LLM settings)
```

Four files of code. Keeping it tight.

## Implementation Steps

### Phase 1: Foundation
- [ ] Set up dependencies (mido, anthropic, openai)
- [ ] Implement `config.py` -- session parameters (tempo, key, time signature, num_rounds, LLM provider/model)
- [ ] Implement `midi_utils.py`:
  - Text note format parser (e.g., `C4 0.5 0.8` -> MIDI note on/off)
  - Function to render a list of measures (per instrument) into a MIDI track
  - Function to combine all tracks into a single MIDI file
  - Handle drums on channel 10 with GM drum map names (kick, snare, hihat, etc.)

### Phase 2: Agents
- [ ] Implement `agents.py`:
  - `Agent` class: name, instrument, system prompt, LLM config
  - System prompt per instrument describing their role, style, constraints
  - Method to build the user prompt from shared history (previous rounds)
  - Method to call LLM (OpenAI or Anthropic) and parse the response into notes
  - Validation: ensure output is parseable, in key, reasonable range for instrument

### Phase 3: Orchestration
- [ ] Implement `jam.py`:
  - Initialize 5 agents
  - Main loop: for each round, call all 5 agents in parallel (asyncio or threading)
  - Collect results, append to history
  - After all rounds, call midi_utils to build the final MIDI file
  - Print a summary of what happened

### Phase 4: Test and Iterate
- [ ] Run a short jam (4-8 rounds) and listen to the output
- [ ] Tune prompts if the music is nonsensical
- [ ] Adjust note format if LLMs struggle with it

## Note Format (LLM I/O)

Each agent outputs one measure as a list of note events:
```
# For melodic instruments (piano, bass, sax, guitar):
NOTE pitch start_beat duration velocity
# Example:
NOTE C4 0.0 0.5 0.8
NOTE Eb4 0.5 0.25 0.7
NOTE G4 1.0 1.0 0.9
REST 2.0 1.0

# For drums:
DRUM sound start_beat duration velocity
# Example:
DRUM kick 0.0 0.25 0.9
DRUM hihat 0.0 0.25 0.6
DRUM snare 1.0 0.25 0.8
DRUM hihat 1.0 0.25 0.6
```

- `pitch`: note name + octave (C4 = middle C)
- `start_beat`: position in the measure (0.0 to 3.75 for 4/4 time)
- `duration`: in beats
- `velocity`: 0.0 to 1.0 (mapped to 0-127)

This is simple enough for an LLM to generate reliably, and straightforward to parse into MIDI.

## Open Questions
- How well will LLMs actually improvise? Might need prompt engineering.
- Should agents have "personality" (conservative vs. adventurous)?
- How many rounds before it gets repetitive or chaotic?
- Do we want a "bandleader" agent that sets direction?

We'll discover these as we go.
