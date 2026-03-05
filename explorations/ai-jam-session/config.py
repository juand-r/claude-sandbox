"""Session configuration for the AI jam session."""

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class LLMConfig:
    """LLM provider configuration."""
    provider: Literal["anthropic", "openai"] = "anthropic"
    model: str = "claude-sonnet-4-20250514"
    temperature: float = 0.9
    max_tokens: int = 1024


@dataclass
class SessionConfig:
    """Configuration for a jam session."""
    # Musical parameters
    tempo: int = 120           # BPM
    key: str = "C minor"       # Key signature
    time_signature: tuple[int, int] = (4, 4)
    num_rounds: int = 8        # Number of measures to generate

    # LLM settings (default for all agents; can be overridden per agent)
    llm: LLMConfig = field(default_factory=LLMConfig)

    # Style direction for the session
    style: str = "jazz fusion with a relaxed groove"

    # Output
    output_file: str = "jam_output.mid"

    @property
    def beats_per_measure(self) -> int:
        return self.time_signature[0]

    @property
    def ticks_per_beat(self) -> int:
        return 480  # Standard MIDI resolution


# General MIDI instrument numbers (0-indexed)
GM_INSTRUMENTS = {
    "piano": 0,        # Acoustic Grand Piano
    "bass": 32,        # Acoustic Bass
    "saxophone": 66,   # Tenor Sax
    "guitar": 26,      # Jazz Guitar
}

# General MIDI drum map (channel 10, note numbers)
GM_DRUMS = {
    "kick": 36,
    "snare": 38,
    "rimshot": 37,
    "hihat_closed": 42,
    "hihat": 42,       # alias
    "hihat_open": 46,
    "ride": 51,
    "ride_bell": 53,
    "crash": 49,
    "tom_high": 50,
    "tom_mid": 47,
    "tom_low": 45,
    "tom_floor": 43,
    "clap": 39,
    "cowbell": 56,
}

# Instrument ranges (MIDI note numbers) for validation
INSTRUMENT_RANGES = {
    "piano": (36, 96),      # C2 to C7
    "bass": (28, 60),       # E1 to C4
    "saxophone": (49, 80),  # Db3 to Ab5
    "guitar": (40, 84),     # E2 to C6
}
