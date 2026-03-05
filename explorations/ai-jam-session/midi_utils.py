"""MIDI utilities: parse text note format, build MIDI files."""

import re
import mido
from config import GM_INSTRUMENTS, GM_DRUMS, INSTRUMENT_RANGES, SessionConfig


# Note name -> semitone offset from C
NOTE_OFFSETS = {
    "C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11,
}

# Accidentals
ACCIDENTALS = {"b": -1, "#": 1, "": 0}

# Regex for parsing note names like C4, Eb3, F#5
NOTE_RE = re.compile(r"^([A-Ga-g])([b#]?)(-?\d)$")


def note_name_to_midi(name: str) -> int:
    """Convert a note name like 'C4' or 'Eb3' to a MIDI note number.

    C4 = 60 (middle C).
    """
    m = NOTE_RE.match(name.strip())
    if not m:
        raise ValueError(f"Invalid note name: {name!r}")
    letter, accidental, octave = m.groups()
    midi_num = (int(octave) + 1) * 12 + NOTE_OFFSETS[letter.upper()] + ACCIDENTALS[accidental]
    if not 0 <= midi_num <= 127:
        raise ValueError(f"Note {name} out of MIDI range (got {midi_num})")
    return midi_num


def midi_to_note_name(midi_num: int) -> str:
    """Convert a MIDI note number back to a note name."""
    NOTE_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    octave = (midi_num // 12) - 1
    note = NOTE_NAMES[midi_num % 12]
    return f"{note}{octave}"


def parse_measure(text: str, instrument: str, beats_per_round: float | None = None) -> list[dict]:
    """Parse a text measure into a list of note events.

    Args:
        text: the raw text output from the LLM
        instrument: instrument name (for range validation)
        beats_per_round: if set, clamp note durations so they don't exceed the round boundary

    Returns list of dicts with keys:
      - type: "note" or "drum" or "rest"
      - pitch: MIDI note number (for note/drum)
      - start: start beat (float)
      - duration: duration in beats (float)
      - velocity: 0-127 (int)
    """
    events = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue

        parts = line.split()
        if len(parts) < 4:
            continue  # skip malformed lines

        cmd = parts[0].upper()

        try:
            if cmd == "NOTE" and len(parts) >= 5:
                pitch_str, start_str, dur_str, vel_str = parts[1], parts[2], parts[3], parts[4]
                midi_note = note_name_to_midi(pitch_str)
                # Validate range
                if instrument in INSTRUMENT_RANGES:
                    lo, hi = INSTRUMENT_RANGES[instrument]
                    midi_note = max(lo, min(hi, midi_note))
                start = float(start_str)
                duration = float(dur_str)
                if beats_per_round is not None:
                    duration = min(duration, beats_per_round - start)
                if duration <= 0:
                    continue
                events.append({
                    "type": "note",
                    "pitch": midi_note,
                    "start": start,
                    "duration": duration,
                    "velocity": int(float(vel_str) * 127),
                })

            elif cmd == "DRUM" and len(parts) >= 5:
                sound_name = parts[1].lower()
                start_str, dur_str, vel_str = parts[2], parts[3], parts[4]
                if sound_name not in GM_DRUMS:
                    continue  # skip unknown drum sounds
                start = float(start_str)
                duration = float(dur_str)
                if beats_per_round is not None:
                    duration = min(duration, beats_per_round - start)
                if duration <= 0:
                    continue
                events.append({
                    "type": "drum",
                    "pitch": GM_DRUMS[sound_name],
                    "start": start,
                    "duration": duration,
                    "velocity": int(float(vel_str) * 127),
                })

            elif cmd == "REST" and len(parts) >= 3:
                pass  # silence, nothing to emit

        except (ValueError, IndexError):
            continue  # skip any malformed line

    return events


def events_to_midi_messages(events: list[dict], ticks_per_beat: int) -> list[tuple[int, mido.Message]]:
    """Convert parsed events to a list of (absolute_tick, mido.Message) pairs."""
    messages = []
    for ev in events:
        if ev["type"] in ("note", "drum"):
            channel = 9 if ev["type"] == "drum" else 0  # channel 9 = drums in MIDI
            start_tick = int(ev["start"] * ticks_per_beat)
            dur_ticks = max(1, int(ev["duration"] * ticks_per_beat))
            vel = max(1, min(127, ev["velocity"]))
            messages.append((start_tick, mido.Message(
                "note_on", note=ev["pitch"], velocity=vel, channel=channel, time=0
            )))
            messages.append((start_tick + dur_ticks, mido.Message(
                "note_off", note=ev["pitch"], velocity=0, channel=channel, time=0
            )))
    # Sort by tick, with note_off before note_on at same tick
    messages.sort(key=lambda x: (x[0], 0 if x[1].type == "note_off" else 1))
    return messages


def build_midi_file(
    all_measures: dict[str, list[str]],
    config: SessionConfig,
) -> mido.MidiFile:
    """Build a complete MIDI file from all instrument measures.

    Args:
        all_measures: dict mapping instrument name -> list of text measures (one per round)
        config: session configuration
    """
    mid = mido.MidiFile(ticks_per_beat=config.ticks_per_beat)
    ticks_per_round = config.ticks_per_round

    for instrument, measures in all_measures.items():
        track = mido.MidiTrack()
        mid.tracks.append(track)

        # Track name
        track.append(mido.MetaMessage("track_name", name=instrument, time=0))

        # Tempo (only on first track)
        if len(mid.tracks) == 1:
            track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(config.tempo), time=0))

        # Program change for melodic instruments
        if instrument != "drums":
            program = GM_INSTRUMENTS.get(instrument, 0)
            ch = 0 if instrument == list(GM_INSTRUMENTS.keys())[0] else (
                list(GM_INSTRUMENTS.keys()).index(instrument) if instrument in GM_INSTRUMENTS else 0
            )
            track.append(mido.Message("program_change", program=program, channel=ch, time=0))
        else:
            ch = 9  # drums

        # Collect all messages across all measures
        all_msgs = []
        for round_idx, measure_text in enumerate(measures):
            measure_offset = round_idx * ticks_per_round
            events = parse_measure(measure_text, instrument, config.beats_per_round)
            msgs = events_to_midi_messages(events, config.ticks_per_beat)
            for abs_tick, msg in msgs:
                # Override channel for this instrument
                msg = msg.copy(channel=ch)
                all_msgs.append((measure_offset + abs_tick, msg))

        # Sort and convert absolute ticks to delta times
        all_msgs.sort(key=lambda x: (x[0], 0 if x[1].type == "note_off" else 1))
        prev_tick = 0
        for abs_tick, msg in all_msgs:
            delta = abs_tick - prev_tick
            track.append(msg.copy(time=delta))
            prev_tick = abs_tick

        # End of track
        track.append(mido.MetaMessage("end_of_track", time=0))

    return mid


def format_history_for_prompt(
    history: dict[str, list[str]],
    current_round: int,
) -> str:
    """Format the shared history into text for the LLM prompt."""
    if current_round == 0:
        return "(This is the first round. There is no history yet. You set the tone!)"

    lines = []
    for round_idx in range(current_round):
        lines.append(f"--- Round {round_idx + 1} ---")
        for instrument, measures in history.items():
            if round_idx < len(measures):
                lines.append(f"[{instrument}]")
                lines.append(measures[round_idx])
                lines.append("")
    return "\n".join(lines)
