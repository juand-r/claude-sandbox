"""
Demo: interactive traversal of the eigenvalues knowledge space.

Loads the manually annotated eigenvalues text and lets you navigate it,
choosing your own path through the material.
"""

from extractor import load_knowledge_space
from knowledge_space import ReaderState


def run_interactive(ks_path: str = "texts/eigenvalues_ks.json"):
    ks = load_knowledge_space(ks_path)

    issues = ks.validate()
    if issues:
        print("Validation issues:")
        for issue in issues:
            print(f"  - {issue}")
        print()

    print("=" * 60)
    print("GARDEN OF FORKING PATHS: Eigenvalues")
    print("=" * 60)
    print(f"Total nodes: {len(ks.nodes)}")
    print(f"Total concepts: {len(ks.concepts_taught())}")
    print(f"Entry points: {[n.title for n in ks.entry_points()]}")
    print()

    state = ReaderState()

    while True:
        available = ks.available_from(state)
        if not available:
            print("\n" + "=" * 60)
            print("You have read all available material.")
            print(f"Path taken: {' -> '.join(state.history)}")
            print(f"Concepts acquired: {len(state.knowledge)}")
            break

        print("-" * 60)
        print(f"Knowledge: {sorted(c.id for c in state.knowledge) or '(none yet)'}")
        print(f"\nAvailable next ({len(available)}):")
        for i, node in enumerate(available):
            print(f"  [{i+1}] {node.title}")

        print(f"  [q] Quit")
        print()

        choice = input("Choose: ").strip()
        if choice.lower() == "q":
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                node = available[idx]

                # Check for bridging
                bridging = ks.bridging_summary_needed(state, node)
                if bridging:
                    print(f"\n  [Note: you may want context on: "
                          f"{', '.join(c.label for c in bridging)}]")

                print(f"\n{'=' * 60}")
                print(f"  {node.title}")
                print(f"{'=' * 60}")
                print(node.content.strip())
                print()
                print(f"  [Teaches: {', '.join(c.label for c in node.teaches)}]")

                state = state.read(node)
            else:
                print("Invalid choice.")
        except ValueError:
            print("Enter a number or 'q'.")

    print("\nDone.")


if __name__ == "__main__":
    run_interactive()
