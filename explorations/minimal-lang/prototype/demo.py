#!/usr/bin/env python3
"""
Demo: ML experiment workflow using the verb/effect system.

This demonstrates the core thesis: the researcher writes ONLY the parts
that require human judgment (model, training customization, experiment
definition). The system handles everything else (logging, checkpointing,
resource allocation, progress tracking, result analysis).

Equivalent to ~200 lines of Python + YAML + bash in a traditional setup.

Run: python demo.py
"""

from effects import handle, handle_many
from verbs import list_verbs, get_verb
from ml_effects import Log, LogParams, Save, Load, AllocCompute, ReleaseCompute, Progress
from ml_verbs import train, evaluate, sweep, analyze, render_table, Config, Run
from handlers import local_dev_handlers, CSVLogger
from verbs import VerbStarted, VerbCompleted, VerbFailed


def main():
    print("=" * 60)
    print("MINIMAL-LANG PROTOTYPE: ML Experiment Workflow")
    print("=" * 60)

    # -----------------------------------------------------------------
    # Show registered verbs (the system knows what operations exist)
    # -----------------------------------------------------------------
    print("\nRegistered verbs:")
    for v in list_verbs():
        effects = [e.__name__ for e in v.needs]
        print(f"  {v.name}: needs {effects}")
        print(f"    {v.describes}")

    # -----------------------------------------------------------------
    # Backend configuration
    # In the language, this would be:
    #     tracking: Console
    #     storage: LocalFS { root: "artifacts/" }
    #     compute: Local
    # -----------------------------------------------------------------
    handlers = local_dev_handlers()

    # -----------------------------------------------------------------
    # The experiment
    # In the language, this would be:
    #     experiment "lr_study":
    #         sweep:
    #             lr: [0.1, 0.01, 0.001]
    #             epochs: [5, 10]
    #         each(config):
    #             train(model(config), data, config)
    # -----------------------------------------------------------------

    with handle_many(handlers):
        # Single training run
        print("\n" + "=" * 60)
        print("PART 1: Single training run")
        print("=" * 60)

        config = Config(lr=0.01, epochs=5, optimizer="adam")
        run = train(model=None, data=None, config=config)

        print(f"\nResult: val_accuracy = {run.final('val_accuracy'):.4f}")

        # Sweep
        print("\n" + "=" * 60)
        print("PART 2: Hyperparameter sweep")
        print("=" * 60)

        runs = sweep(
            verb_fn=train,
            base_config={"optimizer": "adam"},
            sweep_params={
                "lr": [0.1, 0.01, 0.001],
                "epochs": [5, 10],
            },
        )

        # Analysis
        print("\n" + "=" * 60)
        print("PART 3: Results analysis")
        print("=" * 60)

        results = analyze(runs)
        print(f"\nSummary:")
        print(f"  Total runs:    {results['total_runs']}")
        print(f"  Completed:     {results['completed']}")
        print(f"  Failed:        {results['failed']}")
        print(f"  Best config:   {results['best_config']}")
        print(f"  Best accuracy: {results['best_val_accuracy']:.4f}")

        # Table
        print(f"\nResults table:")
        table = render_table(runs, {
            "LR": lambda r: r.config.lr,
            "Epochs": lambda r: r.config.epochs,
            "Val Acc": lambda r: r.final("val_accuracy"),
            "Train Loss": lambda r: r.final("train_loss"),
        })
        print(table)

    # -----------------------------------------------------------------
    # Demonstrate effect swapping
    # In the language, this would be:
    #     tracking: CSV { dir: "csv_results/" }
    #     (everything else unchanged)
    # -----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("PART 4: Swap tracking backend (Console -> CSV)")
    print("=" * 60)

    csv_logger = CSVLogger("csv_results")
    csv_logger.set_run_id("demo_run_001")

    # Swap ONLY the Log handler -- everything else stays the same
    swapped_handlers = dict(handlers)
    swapped_handlers[Log] = csv_logger

    with handle_many(swapped_handlers):
        config = Config(lr=0.01, epochs=3, optimizer="adam")
        run = train(model=None, data=None, config=config)
        print(f"  Result: val_accuracy = {run.final('val_accuracy'):.4f}")
        print(f"  (Metrics written to csv_results/)")

    csv_logger.close()

    # -----------------------------------------------------------------
    # Demonstrate missing handler detection
    # -----------------------------------------------------------------
    print("\n" + "=" * 60)
    print("PART 5: Missing handler detection")
    print("=" * 60)

    # Only install Log handler -- train needs more than that
    try:
        with handle(Log, lambda e: None):
            train(model=None, data=None, config=Config(epochs=1))
    except RuntimeError as e:
        print(f"  Caught: {e}")
        print("  (The system tells you exactly what's missing)")


if __name__ == "__main__":
    main()
