# AI Jam Session

Five LLM-powered agents improvise music together in a round-based MIDI jam session.

## How it works

Each round, all 5 agents (piano, bass, drums, saxophone, guitar) generate one measure of music in parallel. They see the full history of what everyone played in previous rounds, so they can react and build on each other.

Output is a standard MIDI file.

## Setup

```bash
pip install mido anthropic openai
```

Set your API key:
```bash
export ANTHROPIC_API_KEY=your-key-here
# or
export OPENAI_API_KEY=your-key-here
```

## Run

```bash
cd explorations/ai-jam-session
python jam.py

# Options:
python jam.py --rounds 4 --tempo 100 --key "Bb major" --style "cool jazz"
python jam.py --provider openai --model gpt-4o-mini
python jam.py --output my_jam.mid
```

## Output

The MIDI file can be played with any MIDI player (e.g., VLC, Timidity++, or import into a DAW).
