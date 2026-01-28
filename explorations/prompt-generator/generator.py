#!/usr/bin/env python3
"""
Prompt generator that creates surprising project ideas by combining random elements.
"""

import argparse
import random

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


def generate_prompt(rng: random.Random) -> str:
    """Generate a single random prompt."""
    template = rng.choice(TEMPLATES)
    return template.format(
        domain=rng.choice(DOMAINS),
        format=rng.choice(FORMATS),
        constraint=rng.choice(CONSTRAINTS),
        twist=rng.choice(TWISTS),
    )


def main():
    parser = argparse.ArgumentParser(description="Generate random project prompts")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of prompts")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    for i in range(args.count):
        if args.count > 1:
            print(f"\n[{i + 1}]")
        print(generate_prompt(rng))


if __name__ == "__main__":
    main()
