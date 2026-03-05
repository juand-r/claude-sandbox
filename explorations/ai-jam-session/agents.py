"""AI agents that play instruments in the jam session."""

import os
import anthropic
import openai
from config import LLMConfig, SessionConfig


SYSTEM_PROMPTS = {
    "piano": """You are a jazz pianist in a live jam session. Your role:
- Provide harmonic support with chord voicings
- Comp behind soloists, leaving space
- Occasionally add melodic fills between phrases
- Use jazz voicings (7ths, 9ths, 13ths) -- not just triads
- Listen to what others are playing and react musically
- Leave some beats empty -- silence is music too""",

    "bass": """You are a jazz bassist in a live jam session. Your role:
- Lay down the harmonic and rhythmic foundation
- Play walking bass lines that outline the chord changes
- Lock in with the drummer's kick pattern
- Keep it steady but add occasional variations
- Mostly quarter notes and eighth notes, some syncopation
- Stay in the low register (octaves 1-3)""",

    "drums": """You are a jazz drummer in a live jam session. Your role:
- Drive the rhythm and energy of the group
- Keep a steady groove while adding fills and variations
- Use the ride cymbal as your main timekeeping element
- Add kick and snare for accents and groove
- Use hi-hat for texture
- Listen and react -- busier when energy is high, simpler when it's laid back
- Leave some space; don't overplay

Available drum sounds: kick, snare, rimshot, hihat_closed, hihat_open, ride, ride_bell, crash, tom_high, tom_mid, tom_low, tom_floor, clap, cowbell""",

    "vibraphone": """You are a vibraphone player in a live jam session. Your role:
- Play melodic lines and take solos
- Use a mix of single notes and two-note intervals
- Let notes ring -- the vibraphone sustains beautifully
- Use space between phrases -- don't play continuously
- React to what the rhythm section is doing
- Add occasional chromatic approaches and passing tones
- Range: roughly F3 to F6""",

    "strings": """You are a string ensemble in a live jam session. Your role:
- Provide warm harmonic pads and sustained chords
- Play long, sustained notes that fill out the harmony
- Use smooth voice leading between chords
- Stay mostly in the background -- support, don't dominate
- Occasionally swell in dynamics for expression
- Keep it simple -- 2 to 4 note chords, not busy lines
- Leave space for the other instruments""",
}


def note_format_instructions(beats_per_round: int) -> str:
    max_beat = beats_per_round - 0.25
    unit = "measure" if beats_per_round == 4 else f"{beats_per_round}-beat segment"
    return f"""
Output EXACTLY one {unit} of music in this text format, one event per line:

For melodic notes:
NOTE <pitch> <start_beat> <duration> <velocity>

Example:
NOTE C4 0.0 0.5 0.8
NOTE Eb4 0.5 0.25 0.7
NOTE G4 1.0 1.0 0.9

- pitch: note name + octave (C4 = middle C). Use flats (Bb, Eb) not sharps.
- start_beat: position in the segment (0.0 to {max_beat})
- duration: in beats (0.25 = sixteenth, 0.5 = eighth, 1.0 = quarter, 2.0 = half)
- velocity: 0.0 to 1.0 (softness/loudness)
- IMPORTANT: all notes must start within 0.0 to {max_beat} beats.

For rests (optional, for clarity):
REST <start_beat> <duration>

Output ONLY the note lines. No explanation, no commentary. Just the notes.
"""


def drum_format_instructions(beats_per_round: int) -> str:
    max_beat = beats_per_round - 0.25
    unit = "measure" if beats_per_round == 4 else f"{beats_per_round}-beat segment"
    return f"""
Output EXACTLY one {unit} of drums in this text format, one event per line:

DRUM <sound> <start_beat> <duration> <velocity>

Example:
DRUM ride 0.0 0.5 0.7
DRUM kick 0.0 0.25 0.8
DRUM hihat_closed 0.5 0.25 0.5
DRUM snare 1.0 0.25 0.9

- sound: one of kick, snare, rimshot, hihat_closed, hihat_open, ride, ride_bell, crash, tom_high, tom_mid, tom_low, tom_floor, clap, cowbell
- start_beat: position in the segment (0.0 to {max_beat})
- duration: in beats
- velocity: 0.0 to 1.0
- IMPORTANT: all hits must start within 0.0 to {max_beat} beats.

Output ONLY the drum lines. No explanation, no commentary. Just the drum hits.
"""


class Agent:
    """An AI musician agent that generates one round at a time."""

    def __init__(self, instrument: str, config: SessionConfig, llm_override: LLMConfig | None = None):
        self.instrument = instrument
        self.config = config
        self.llm_config = llm_override or config.llm

        if instrument not in SYSTEM_PROMPTS:
            raise ValueError(f"Unknown instrument: {instrument}")

        bpr = config.beats_per_round
        fmt = drum_format_instructions(bpr) if instrument == "drums" else note_format_instructions(bpr)
        session_info = (
            f"Session info:\n"
            f"- Tempo: {config.tempo} BPM\n"
        )
        if config.key:
            session_info += f"- Key: {config.key}\n"
        session_info += (
            f"- Time signature: {config.time_signature[0]}/{config.time_signature[1]}\n"
            f"- Style: {config.style}\n"
        )
        self.system_prompt = (
            f"{SYSTEM_PROMPTS[instrument]}\n\n"
            f"{session_info}\n"
            f"OUTPUT FORMAT:\n{fmt}"
        )

    def build_user_prompt(self, history_text: str, current_round: int) -> str:
        """Build the user message for this round."""
        bpr = self.config.beats_per_round
        unit = "measure" if bpr == self.config.beats_per_measure else f"{bpr}-beat segment"
        return (
            f"Round {current_round + 1} of {self.config.num_rounds}.\n\n"
            f"Here is what everyone played so far:\n{history_text}\n\n"
            f"Now play your {unit} for round {current_round + 1}. "
            f"Output ONLY the note/drum lines, nothing else."
        )

    def call_llm(self, user_prompt: str) -> str:
        """Call the LLM and return the raw text response."""
        if self.llm_config.provider == "anthropic":
            return self._call_anthropic(user_prompt)
        elif self.llm_config.provider == "openai":
            return self._call_openai(user_prompt)
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_config.provider}")

    def _call_anthropic(self, user_prompt: str) -> str:
        # Work around env where "export " may be baked into the var name
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            api_key = os.environ.get("export ANTHROPIC_API_KEY", "")
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=self.llm_config.model,
            max_tokens=self.llm_config.max_tokens,
            temperature=self.llm_config.temperature,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text

    def _call_openai(self, user_prompt: str) -> str:
        client = openai.OpenAI()  # uses OPENAI_API_KEY env var
        response = client.chat.completions.create(
            model=self.llm_config.model,
            max_tokens=self.llm_config.max_tokens,
            temperature=self.llm_config.temperature,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content

    def generate_measure(self, history_text: str, current_round: int) -> str:
        """Generate one measure of music given the session history.

        Returns the raw text output (NOTE/DRUM lines).
        """
        user_prompt = self.build_user_prompt(history_text, current_round)
        raw = self.call_llm(user_prompt)

        # Extract only NOTE/DRUM/REST lines from the response
        # (LLMs sometimes add commentary despite instructions)
        cleaned_lines = []
        for line in raw.strip().splitlines():
            stripped = line.strip()
            if stripped.upper().startswith(("NOTE ", "DRUM ", "REST ")):
                cleaned_lines.append(stripped)

        result = "\n".join(cleaned_lines)
        if not result:
            # Fallback: if no valid lines found, return the raw output
            # and let the parser deal with it
            print(f"  WARNING [{self.instrument}]: No valid lines parsed from LLM output.")
            print(f"  Raw output: {raw[:200]}")
            return raw

        return result
