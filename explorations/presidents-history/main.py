#!/usr/bin/env python3
"""Presidents History — simple CLI for querying U.S. president data."""

import sys
from data import PRESIDENTS


def list_all():
    """Print all presidents."""
    for p in PRESIDENTS:
        print(f"  {p['number']:>2}. {p['name']} ({p['party']}, {p['term']})")


def show_president(number):
    """Show details for a president by number."""
    matches = [p for p in PRESIDENTS if p["number"] == number]
    if not matches:
        print(f"No president #{number}.")
        return
    for p in matches:
        print(f"  #{p['number']} {p['name']}")
        print(f"  Party: {p['party']}")
        print(f"  Term:  {p['term']}")
        print(f"  Fact:  {p['key_fact']}")
        print()


def search(query):
    """Search presidents by name or party (case-insensitive)."""
    q = query.lower()
    results = [p for p in PRESIDENTS if q in p["name"].lower() or q in p["party"].lower()]
    if not results:
        print(f"No results for '{query}'.")
        return
    for p in results:
        print(f"  #{p['number']} {p['name']} ({p['party']}, {p['term']}) — {p['key_fact']}")


def print_usage():
    print("Usage:")
    print("  python main.py list             — List all presidents")
    print("  python main.py show <number>    — Show details for president #N")
    print("  python main.py search <query>   — Search by name or party")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "list":
        list_all()
    elif command == "show":
        if len(sys.argv) < 3:
            print("Error: 'show' requires a president number.")
            sys.exit(1)
        try:
            num = int(sys.argv[2])
        except ValueError:
            print(f"Error: '{sys.argv[2]}' is not a valid number.")
            sys.exit(1)
        show_president(num)
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: 'search' requires a query string.")
            sys.exit(1)
        search(" ".join(sys.argv[2:]))
    else:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
