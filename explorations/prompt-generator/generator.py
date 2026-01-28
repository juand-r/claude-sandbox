#!/usr/bin/env python3
"""
Prompt generator that creates surprising project ideas by combining random elements.
"""

import argparse
import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# === WORD LISTS (edit these to customize) ===

DOMAINS = [
    "a personal finance tracker",
    "a recipe manager",
    "a habit tracker",
    "a bookmark organizer",
    "a mood journal",
    "a reading list",
    "a workout log",
    "a plant watering reminder",
    "a quote collector",
    "a decision maker",
    "a countdown timer",
    "a password generator",
    "a color palette tool",
    "a markdown previewer",
    "a pomodoro timer",
    "a flashcard system",
    "a URL shortener",
    "a pastebin clone",
    "a chat room",
    "a polling system",
    "a kanban board",
    "a note-taking app",
    "a weather dashboard",
    "a file organizer",
    "a code snippet manager",
]

FORMATS = [
    "as a CLI tool",
    "as a single HTML file",
    "as a REST API",
    "as a Discord bot",
    "as a browser extension",
    "as a TUI (terminal UI)",
    "using only bash scripts",
    "as a static site generator",
    "as a WebSocket server",
    "as a Slack bot",
    "using SQLite for everything",
    "as a serverless function",
    "as a Chrome DevTools extension",
    "using only vanilla JavaScript",
    "as a GraphQL API",
]

CONSTRAINTS = [
    "in under 100 lines of code",
    "with no external dependencies",
    "that works offline",
    "using only the standard library",
    "that fits in a single file",
    "with real-time sync",
    "that's fully keyboard-navigable",
    "with undo/redo support",
    "that exports to multiple formats",
    "with fuzzy search",
    "that auto-saves continuously",
    "with vim keybindings",
    "that works in the terminal and browser",
    "with a plugin system",
    "that's embeddable in other apps",
]

TWISTS = [
    "but everything is stored as plain text files",
    "but it uses AI to suggest improvements",
    "but it gamifies the experience with points/streaks",
    "but it has a retro/ASCII aesthetic",
    "but it syncs via git",
    "but it speaks/reads aloud",
    "but it generates visualizations",
    "but it learns from your patterns",
    "but all data is encrypted client-side",
    "but it works peer-to-peer with no server",
    "but it has a time-travel/history feature",
    "but it can import from 5+ existing services",
    "but it uses natural language commands",
    "but it's designed for collaborative use",
    "but it has an API others can build on",
]

TEMPLATES = [
    "Build {domain} {format} {constraint}, {twist}.",
    "Create {domain} {format}. Requirement: {constraint}. Twist: {twist}.",
    "Implement {domain} {constraint}. Deliver it {format}, {twist}.",
    "{domain} — {format}, {constraint}. The catch: {twist}.",
    "Challenge: {domain} {format}. Must be {constraint}, {twist}.",
]


def load_word_list(name: str) -> list[str]:
    """Load a word list from the words/ directory."""
    path = SCRIPT_DIR / "words" / f"{name}.txt"
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def load_all_words() -> dict[str, list[str]]:
    """Load all word lists."""
    return {
        "nouns": load_word_list("nouns"),
        "verbs": load_word_list("verbs"),
        "adjectives": load_word_list("adjectives"),
    }


def generate_wild_cards(rng: random.Random, words: dict[str, list[str]],
                        nouns: int = 3, verbs: int = 2, adjectives: int = 1) -> str:
    """Generate the wild card injection string."""
    parts = []

    if words["nouns"] and nouns > 0:
        sampled = rng.sample(words["nouns"], min(nouns, len(words["nouns"])))
        parts.append(f"nouns: {', '.join(sampled)}")

    if words["verbs"] and verbs > 0:
        sampled = rng.sample(words["verbs"], min(verbs, len(words["verbs"])))
        parts.append(f"verbs: {', '.join(sampled)}")

    if words["adjectives"] and adjectives > 0:
        sampled = rng.sample(words["adjectives"], min(adjectives, len(words["adjectives"])))
        parts.append(f"adjectives: {', '.join(sampled)}")

    if not parts:
        return ""

    return "\n\n🎲 Wild cards — incorporate these somehow: " + "; ".join(parts)


def generate_prompt(rng: random.Random, words: dict[str, list[str]] | None = None,
                    wild_cards: bool = True) -> str:
    """Generate a single random prompt."""
    template = rng.choice(TEMPLATES)
    base = template.format(
        domain=rng.choice(DOMAINS),
        format=rng.choice(FORMATS),
        constraint=rng.choice(CONSTRAINTS),
        twist=rng.choice(TWISTS),
    )

    if wild_cards and words:
        base += generate_wild_cards(rng, words)

    return base


def main():
    parser = argparse.ArgumentParser(description="Generate random project prompts")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of prompts")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--no-wild", action="store_true", help="Disable wild card words")
    parser.add_argument("--nouns", type=int, default=3, help="Number of random nouns (default: 3)")
    parser.add_argument("--verbs", type=int, default=2, help="Number of random verbs (default: 2)")
    parser.add_argument("--adjectives", type=int, default=1, help="Number of random adjectives (default: 1)")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    words = load_all_words() if not args.no_wild else None

    for i in range(args.count):
        if args.count > 1:
            print(f"\n[{i + 1}]")
        print(generate_prompt(rng, words, wild_cards=not args.no_wild))


if __name__ == "__main__":
    main()
