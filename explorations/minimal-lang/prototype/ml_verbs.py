"""
ML domain pack: verbs for machine learning workflows.

These verbs demonstrate the key insight: the verb body contains ONLY
the logic specific to the operation. All infrastructure (logging,
checkpointing, resource allocation, progress tracking) is handled
by effects. The verb author never imports wandb, never writes SLURM
scripts, never manages GPU allocation.

Adding a new verb:
    1. Decide what effects it needs
    2. Write the function body using perform() for side effects
    3. Decorate with @verb

That's it. The system handles the rest.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Any, Callable

from effects import perform, handle, handle_many
from verbs import verb
from ml_effects import Log, LogParams, Save, Load, AllocCompute, ReleaseCompute, Progress


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class Config:
    """Training configuration. Just a dict with attribute access."""
    _data: dict[str, Any] = field(default_factory=dict)

    def __init__(self, **kwargs):
        self._data = kwargs

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            return super().__getattribute__(name)
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"Config has no attribute '{name}'")

    def __repr__(self):
        return f"Config({self._data})"

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)


@dataclass
class Metrics:
    """Accumulated metrics for a run."""
    history: list[dict[str, Any]] = field(default_factory=list)

    def log(self, step: int, **kwargs):
        entry = {"step": step, **kwargs}
        self.history.append(entry)

    def final(self, key: str) -> float | None:
        """Get the last recorded value for a metric."""
        for entry in reversed(self.history):
            if key in entry:
                return entry[key]
        return None

    def best(self, key: str, mode: str = "max") -> float | None:
        """Get the best recorded value for a metric."""
        values = [e[key] for e in self.history if key in e]
        if not values:
            return None
        return max(values) if mode == "max" else min(values)


@dataclass
class Run:
    """Result of a training or evaluation run."""
    config: Config
    metrics: Metrics
    status: str = "completed"  # completed | failed
    error: str | None = None

    def final(self, key: str) -> float | None:
        return self.metrics.final(key)


# ---------------------------------------------------------------------------
# train verb
# ---------------------------------------------------------------------------

@verb(
    name="train",
    needs=[Log, LogParams, Save, AllocCompute, ReleaseCompute, Progress],
    describes="Train a model on data using a training function",
)
def train(model: Any, data: Any, config: Config,
          train_fn: Callable | None = None) -> Run:
    """Train a model.

    The train_fn is the researcher's custom training logic.
    It receives (model, data, config, step_callback) and should call
    step_callback(step, **metrics) after each step/epoch.

    If no train_fn is provided, uses a default training loop simulation.
    """
    perform(LogParams(config.to_dict()))
    compute = perform(AllocCompute({"gpu": getattr(config, "gpu", False)}))

    metrics = Metrics()
    epochs = getattr(config, "epochs", 10)

    if train_fn is not None:
        # Researcher's custom loop
        def step_callback(step: int, **kwargs):
            metrics.log(step, **kwargs)
            for key, value in kwargs.items():
                perform(Log(key, value, step=step))
            perform(Progress(step, epochs))

        train_fn(model, data, config, step_callback)
    else:
        # Default loop: calls model's train_step if it exists,
        # otherwise simulates training (useful for testing the system)
        for epoch in range(epochs):
            if hasattr(model, "train_step"):
                step_metrics = model.train_step(data, config)
            else:
                # Simulation for demo purposes
                import random
                step_metrics = {
                    "train_loss": 1.0 / (epoch + 1) + random.gauss(0, 0.05),
                    "val_accuracy": min(0.95, 0.5 + epoch * 0.05 + random.gauss(0, 0.02)),
                }

            metrics.log(epoch, **step_metrics)
            for key, value in step_metrics.items():
                perform(Log(key, value, step=epoch))
            perform(Progress(epoch + 1, epochs))

    # Save the trained model
    best_metric = metrics.best("val_accuracy")
    perform(Save("model", model, metadata={
        "config": config.to_dict(),
        "best_val_accuracy": best_metric,
    }))

    perform(ReleaseCompute(compute))

    return Run(config=config, metrics=metrics)


# ---------------------------------------------------------------------------
# evaluate verb
# ---------------------------------------------------------------------------

@verb(
    name="evaluate",
    needs=[Log],
    describes="Evaluate a model on a dataset",
)
def evaluate(model: Any, data: Any, config: Config,
             eval_fn: Callable | None = None) -> Run:
    """Evaluate a model on data.

    eval_fn receives (model, data, config) and returns a dict of metrics.
    """
    metrics = Metrics()

    if eval_fn is not None:
        result = eval_fn(model, data, config)
    else:
        # Simulation
        import random
        result = {
            "test_accuracy": 0.85 + random.gauss(0, 0.03),
            "test_loss": 0.3 + random.gauss(0, 0.05),
        }

    metrics.log(0, **result)
    for key, value in result.items():
        perform(Log(key, value))

    return Run(config=config, metrics=metrics)


# ---------------------------------------------------------------------------
# sweep verb -- this is where the system really earns its keep
# ---------------------------------------------------------------------------

@verb(
    name="sweep",
    needs=[Log, Save, AllocCompute, ReleaseCompute, Progress],
    describes="Run a verb across a grid of configurations",
)
def sweep(
    verb_fn: Callable,
    base_config: dict[str, Any],
    sweep_params: dict[str, list[Any]],
    model_fn: Callable | None = None,
    data: Any = None,
) -> list[Run]:
    """Run a verb across all combinations of sweep parameters.

    This is the cartesian product sweep. It:
    1. Generates all config combinations
    2. Runs the verb for each
    3. Handles failures (logs and continues)
    4. Returns all runs

    In a full system, this would also handle:
    - Parallel execution across GPUs/machines
    - Early stopping of bad configs
    - Resume from partial sweeps
    - Optuna-style intelligent search

    But for the prototype, sequential + cartesian is enough to
    demonstrate the mechanism.
    """
    # Generate all configurations
    param_names = list(sweep_params.keys())
    param_values = list(sweep_params.values())
    combinations = list(itertools.product(*param_values))
    total = len(combinations)

    print(f"\nSweep: {total} configurations")
    print(f"  params: {param_names}")
    print(f"  total runs: {total}")

    runs: list[Run] = []

    for i, combo in enumerate(combinations):
        # Build config for this run
        run_config = dict(base_config)
        for name, value in zip(param_names, combo):
            run_config[name] = value
        config = Config(**run_config)

        print(f"\n=== Run {i+1}/{total}: {dict(zip(param_names, combo))} ===")

        try:
            # Build model fresh for each run (if model_fn provided)
            model = model_fn(config) if model_fn is not None else None

            # Call the verb
            run = verb_fn(model, data, config)
            runs.append(run)

        except Exception as e:
            print(f"  FAILED: {e}")
            runs.append(Run(
                config=config,
                metrics=Metrics(),
                status="failed",
                error=str(e),
            ))

        perform(Progress(i + 1, total, f"sweep progress"))

    return runs


# ---------------------------------------------------------------------------
# analyze -- query results from runs
# ---------------------------------------------------------------------------

def analyze(runs: list[Run]) -> dict[str, Any]:
    """Analyze results from a sweep.

    This is a simple utility, not a verb (no side effects needed).
    In the full language, this would be the query syntax:
        runs |> where(.status == "completed") |> best(by: .final("val_accuracy"))
    """
    completed = [r for r in runs if r.status == "completed"]
    if not completed:
        return {"message": "No completed runs"}

    best_run = max(completed, key=lambda r: r.final("val_accuracy") or 0)

    return {
        "total_runs": len(runs),
        "completed": len(completed),
        "failed": len(runs) - len(completed),
        "best_config": best_run.config.to_dict(),
        "best_val_accuracy": best_run.final("val_accuracy"),
    }


def render_table(runs: list[Run], columns: dict[str, Callable]) -> str:
    """Render runs as a formatted table.

    In the full language:
        runs |> render table:
            "Backbone" <- .config.backbone
            "Val Acc"  <- .final("val_accuracy") |> pct(1)
    """
    completed = [r for r in runs if r.status == "completed"]
    if not completed:
        return "No completed runs."

    # Build header
    col_names = list(columns.keys())
    rows = []
    for run in completed:
        row = []
        for name, extractor in columns.items():
            val = extractor(run)
            if isinstance(val, float):
                row.append(f"{val:.4f}")
            else:
                row.append(str(val))
        rows.append(row)

    # Calculate column widths
    widths = [len(name) for name in col_names]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(val))

    # Format
    header = " | ".join(name.ljust(w) for name, w in zip(col_names, widths))
    separator = "-+-".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append(" | ".join(val.ljust(w) for val, w in zip(row, widths)))

    return "\n".join(lines)
