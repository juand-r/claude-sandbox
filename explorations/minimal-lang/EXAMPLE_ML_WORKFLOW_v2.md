# Complete Example v2: ML Experiment Workflow

## Revised thesis

The language doesn't replace PyTorch/HuggingFace. It orchestrates them.
The model code is the researcher's creative work -- leave it alone.
The boilerplate is everything AROUND the model: config, experiment
management, tracking, analysis, reproduction.

The language is the glue. PyTorch is the engine.

---

## The program

```
-- ============================================================
-- Domain
-- ============================================================

Dataset = {
    name,
    source: Path | URL,
    split_ratio: { train: Float, val: Float, test: Float } = { 0.8, 0.1, 0.1 },
}

Experiment = {
    name,
    description: String?,
    runs: [Run],
}

Run = {
    config: Config,
    metrics: [{ step: Int, name: String, value: Float }],
    artifacts: [Path],
    status: Pending | Running | Done | Failed { reason },
}


-- ============================================================
-- Model: this is PyTorch, called from the language
-- ============================================================

-- The model lives in a .py file. The researcher writes it in
-- PyTorch because that's where they think. We just reference it.

import model from "models/transformer.py"
    -- expects: model(config) -> nn.Module
    -- The language doesn't parse or understand this code.
    -- It just knows: call this with a config, get a model back.

-- Alternative: inline Python for small models
model(config) = python"""
    import torch.nn as nn
    class Classifier(nn.Module):
        def __init__(self):
            super().__init__()
            self.encoder = AutoModel.from_pretrained(config.backbone)
            self.head = nn.Linear(768, config.num_classes)
        def forward(self, x):
            return self.head(self.encoder(**x).last_hidden_state[:, 0])
    return Classifier()
"""


-- ============================================================
-- Data pipeline
-- ============================================================

data = load("data/imdb.csv")
    |> map({ text: .review, label: int(.sentiment) })
    |> filter(.text.length > 0)
    |> shuffle(seed: 42)
    |> split(0.8, 0.1, 0.1)


-- ============================================================
-- Training: the PATTERN, not the implementation
-- ============================================================

-- This is what every training loop looks like. The researcher
-- shouldn't rewrite this skeleton every time. They should only
-- specify what's DIFFERENT from the standard loop.

-- Standard training with hooks for customization:
train(model, data, config) -> Run =
    standard_loop:
        loss: cross_entropy
        optimizer: config.optimizer(model.parameters(), lr: config.lr)
        scheduler: config.scheduler

    -- Only write the parts that are non-standard:
    on batch_end(step, loss):
        log "train_loss": loss.item()

    on epoch_end(epoch, model):
        val = evaluate(model, data.val, metric: accuracy)
        log "val_accuracy": val
        if val > best:
            save model -> "checkpoints/best.pt"

-- Or, if the researcher needs full control of the loop:
-- override train(model, data, config) = python"..."


-- ============================================================
-- Experiment: the main event
-- ============================================================

-- THIS is where the language earns its keep.
-- Compare: the equivalent in bash + hydra + slurm is 100+ lines
-- across 5+ files.

experiment "attention_study":
    description: "Effect of backbone choice on IMDB sentiment"

    sweep:
        backbone: ["bert-base", "roberta-base", "distilbert-base"]
        lr: [1e-4, 3e-5, 1e-5]
        epochs: [5, 10]

    each(config):
        m = model({ backbone: config.backbone, num_classes: 2 })
        train(m, data, config)

    -- 3 backbones * 3 lrs * 2 epochs = 18 runs
    -- The system handles: parallelism, GPU allocation, failure
    -- recovery, progress tracking. You didn't ask for any of it.


-- ============================================================
-- Analysis: query your results
-- ============================================================

-- This replaces 50 lines of pandas + matplotlib

best_runs = experiment("attention_study").runs
    |> where(.status == Done)
    |> group(.config.backbone)
    |> each: best(by: .final("val_accuracy"))

best_runs |> render table:
    "Backbone"  <- .config.backbone
    "Best LR"   <- .config.lr
    "Val Acc"   <- .final("val_accuracy") |> pct(1)
    "Epochs"    <- .config.epochs
    format: latex
    output: "paper/tables/backbone_comparison.tex"

-- Training curves plot
experiment("attention_study").runs
    |> group(.config.backbone)
    |> render plot:
        x: .step
        y: .metric("val_accuracy")
        color: .config.backbone
        title: "Validation Accuracy by Backbone"
        output: "paper/figures/training_curves.pdf"


-- ============================================================
-- Reproduction: someone reads your paper and wants to rerun
-- ============================================================

-- The entire experiment is re-runnable from this file.
-- No hidden state. No "oh you also need to set this env var."
-- The language captures the full specification.
--
-- $ minimal-lang run experiment_file.ml --experiment attention_study
--
-- It knows what data to fetch, what model to build, what configs
-- to sweep, where to save results. Because you already said all of it.


-- ============================================================
-- Backends
-- ============================================================

tracking: Wandb { project: "attention-study", entity: "my-lab" }
    -- swap to: tracking: MLflow { uri: "http://localhost:5000" }
    -- swap to: tracking: CSV { dir: "results/" }

compute: SLURM { partition: "gpu-a100", gpus_per_run: 1, max_concurrent: 4 }
    -- swap to: compute: Local { device: auto }
    -- swap to: compute: AWS { instance: "p3.2xlarge" }

storage: LocalFS { root: "experiments/" }
    -- swap to: storage: S3 { bucket: "my-experiments" }
```

---

## What the human wrote vs. what the system handles

**Human wrote (~60 lines of actual content):**
- Data pipeline (load, preprocess, split)
- Model reference (pointer to PyTorch code)
- Training customizations (what to log, when to checkpoint)
- Experiment sweep definition (what configs to try)
- Analysis queries (what to compare, how to display)
- Backend configuration

**System handles:**
- Hydra/argparse config generation
- W&B / MLflow initialization + logging calls
- SLURM job scripts + submission + monitoring
- GPU allocation + memory management
- Checkpoint saving/loading mechanics
- Failure detection + retry
- Result aggregation across runs
- LaTeX table formatting
- Plot generation with proper styling
- Reproducibility metadata (git hash, package versions, timestamps)
- Data download + caching

**The researcher didn't write a single line of:**
- YAML configuration
- Bash scripts
- SLURM job files
- W&B boilerplate
- argparse setup
- Matplotlib formatting
- LaTeX table construction

That's where the boilerplate lives in ML research. Not in the model.

---

## Design problems (revised)

### Problem 1: Foreign function interface is critical

The language MUST call Python fluently. Not as an escape hatch -- as a
primary feature. The model code lives in Python. The language orchestrates
around it. The FFI needs to be:
- Zero-friction (no wrappers, no marshaling ceremony)
- Bidirectional (Python code can call back to get config values)
- Type-aware (the language knows the Python function returns nn.Module)

### Problem 2: What's a "standard_loop"?

The `standard_loop` concept in the training section is hand-wavy.
What does it actually mean? Options:
- A library of common patterns (like HuggingFace Trainer)
- A macro that expands to a full training loop
- A template with hook points

This needs real design work. The training loop is the most common
pattern an ML researcher repeats, and it's the hardest to abstract
because everyone's loop is slightly different.

### Problem 3: The sweep is secretly an orchestrator

`sweep` looks simple but it's doing a LOT:
- Generating the cartesian product of configs
- Scheduling runs (possibly on different machines)
- Handling failures and retries
- Tracking which runs are done
- Potentially doing early stopping (kill bad configs)

This is basically Optuna + SLURM + Airflow in one keyword.
Is that too much magic?

### Problem 4: "Render" is a whole ecosystem

`render table` and `render plot` each hide significant complexity.
LaTeX tables need proper formatting, escaping, alignment.
Plots need axes, legends, colors, sizing for publication.
These are currently solved by matplotlib + manual tweaking.

The question: can we provide good-enough defaults for publication
quality? Or will researchers always need to drop into matplotlib?

### Problem 5: Domain packs vs. universal verbs

This example confirms that verbs are domain-specific:
- Web: serve, store, notify, fetch
- ML: train, evaluate, sweep, log, render

The language needs a domain pack system:
```
use ml    -- provides train, evaluate, sweep, log, render
use web   -- provides serve, store, notify, fetch
```

Each pack defines verbs + backends. The core language provides the
mechanism (algebraic effects). Packs provide the vocabulary.
