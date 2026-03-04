# Complete Example: ML Experiment Workflow

## What this program does

A PhD researcher is studying how different attention mechanisms affect
transformer performance on text classification. They need to:

1. Load and preprocess a dataset
2. Define model variants with different configurations
3. Run training experiments across hyperparameter combinations
4. Track metrics, save checkpoints
5. Compare results across runs
6. Generate a results table for their paper

This is a realistic day-to-day workflow. Let's write the WHOLE thing.

---

## The program

```
-- ============================================================
-- Domain: what things ARE
-- ============================================================

Dataset = {
    name,
    source: Path | URL,
    split: { train: Float, val: Float, test: Float },
}

Sample = { text, label: Int }

Model = {
    name,
    arch: Architecture,
    params: { [String]: Any },    -- hyperparameters
}

-- Question: is this the right way to do sum types / variants?
-- This feels like it needs algebraic data types.
Architecture =
    | Transformer { heads: Int, layers: Int, d_model: Int, attention: AttentionType }
    | LSTM { hidden: Int, layers: Int, bidirectional: Bool }

AttentionType =
    | Standard
    | Linear
    | FlashAttention
    | SlidingWindow { window: Int }

Run = {
    model: Model,
    dataset: Dataset,
    config: TrainConfig,
    metrics: [Metric],          -- accumulated over training
    artifacts: [Path],          -- checkpoints, plots, etc.
    status: Pending | Running | Done | Failed { reason: String },
    started: Time?,
    finished: Time?,
}

TrainConfig = {
    epochs: Int = 10,           -- defaults
    batch_size: Int = 32,
    lr: Float = 1e-3,
    optimizer: Adam | SGD | AdamW = AdamW,
    scheduler: Cosine | Linear | None = Cosine,
    device: CPU | GPU { id: Int } | Auto = Auto,
    seed: Int = 42,
}

Metric = { epoch: Int, step: Int, name: String, value: Float }

Experiment = {
    name,
    description: String?,
    runs: [Run],
    created: Time,
}


-- ============================================================
-- Data pipeline
-- ============================================================

-- QUESTION: How does the pipeline verb work? Is |> enough or do
-- we need a dedicated pipeline concept for lazy/streaming data?

load_data(source: Path | URL) -> [Sample] =
    read(source)
    |> parse_csv(header: true)
    |> map({ text: .text, label: int(.label) })

preprocess(samples: [Sample]) -> [Sample] =
    samples
    |> map(.text -> lowercase -> strip -> remove_punctuation)
    |> filter(.text.length > 0)
    |> filter(.label in 0..num_classes)

-- QUESTION: should split be a verb? It's a very common operation.
-- Or is it just a function?
split_data(samples: [Sample], ratio: { train, val, test }) -> { train, val, test } =
    samples
    |> shuffle(seed: config.seed)
    |> partition(ratio)


-- ============================================================
-- Model definition
-- ============================================================

-- QUESTION: This is where it gets hard. Model definition in ML
-- is deeply imperative -- layers, forward pass, weight init.
-- How much of this can we capture at intent level vs needing
-- to drop to Layer 2 logic?

-- Option A: Declarative model spec (high level, limited)
transformer_classifier(vocab_size, num_classes, attention: AttentionType) =
    model:
        embed       = Embedding(vocab_size, d_model: 256)
        encoder     = TransformerEncoder(layers: 4, heads: 8, attention: attention)
        pool        = MeanPool
        classifier  = Linear(256, num_classes)

    forward(x):
        x -> embed -> encoder -> pool -> classifier

-- Option B: More explicit, closer to PyTorch (low level, flexible)
-- forward(x) =
--     h = self.embed(x)
--     h = self.encoder(h)
--     h = h.mean(dim=1)
--     self.classifier(h)

-- QUESTION: Which is right? Probably both -- Option A for the
-- common case, Option B as an override. But the boundary is
-- very fuzzy here. Neural net architecture IS the logic layer
-- for ML researchers. It's not boilerplate -- it's the creative
-- work. So maybe the language shouldn't try to abstract this
-- too hard.


-- ============================================================
-- Training
-- ============================================================

-- QUESTION: Is "train" a verb? It's domain-specific to ML.
-- If "store" and "serve" are built-in verbs, is "train"?
-- Probably not -- it's domain-specific. So this is a function,
-- not a verb. But then... what IS the relationship between
-- domain-specific operations and the verb system?

train(model, data, config: TrainConfig) -> Run =
    run = Run { model, dataset: data, config, status: Running, started: now() }

    for epoch in 1..config.epochs:
        for batch in data.train |> batches(config.batch_size):
            loss = model(batch.text) |> cross_entropy(batch.label)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            log metric: { epoch, step, name: "train_loss", value: loss.item() }

        -- validation
        val_metrics = evaluate(model, data.val)
        log metric: { epoch, step: epoch * steps_per_epoch,
                      name: "val_accuracy", value: val_metrics.accuracy }
        log metric: { epoch, step: epoch * steps_per_epoch,
                      name: "val_loss", value: val_metrics.loss }

        -- checkpoint
        if val_metrics.accuracy > best_accuracy:
            best_accuracy = val_metrics.accuracy
            save checkpoint: model, path: "checkpoints/{run.id}/best.pt"

    run with { status: Done, finished: now() }

evaluate(model, data) -> { accuracy: Float, loss: Float } =
    model.eval()
    predictions = data |> batches(32) |> map(batch -> model(batch.text))
    {
        accuracy: (predictions.argmax(-1) == data.labels).mean(),
        loss: predictions |> cross_entropy(data.labels) |> mean(),
    }


-- ============================================================
-- Experiment: run multiple configurations
-- ============================================================

-- This is the part researchers do ALL THE TIME and it's always
-- a mess of bash scripts, hydra configs, and W&B sweeps.

experiment "attention_comparison":
    description: "Comparing attention mechanisms on IMDB sentiment"

    dataset = load_data("data/imdb.csv") |> preprocess |> split_data(0.8, 0.1, 0.1)

    -- Sweep over attention types
    for attention in [Standard, Linear, FlashAttention, SlidingWindow(128)]:
        for lr in [1e-3, 3e-4, 1e-4]:
            model = transformer_classifier(
                vocab_size: 30000,
                num_classes: 2,
                attention: attention,
            )
            train(model, dataset, config: { lr, epochs: 15, batch_size: 64 })


-- ============================================================
-- Analysis: compare results
-- ============================================================

-- QUESTION: Is this a query? A pipeline? What's the right
-- abstraction for "look at my experiment results and summarize"?

results(experiment: "attention_comparison") =
    experiment.runs
    |> where(.status == Done)
    |> group(.model.params.attention)
    |> summarize(
        best_val_acc: max(.metrics |> where(.name == "val_accuracy") |> max(.value)),
        mean_val_acc: mean(.metrics |> where(.name == "val_accuracy") |> last(.value)),
        best_lr: argmax(.metrics |> where(.name == "val_accuracy") |> max(.value), over: .config.lr),
    )


-- ============================================================
-- Output: generate table for paper
-- ============================================================

-- QUESTION: Is "render" a verb? Is "export"?

results(experiment: "attention_comparison")
|> sort(.best_val_acc, descending)
|> render table:
    columns:
        "Attention"     <- .attention
        "Best Val Acc"  <- .best_val_acc |> format("{:.1%}")
        "Mean Val Acc"  <- .mean_val_acc |> format("{:.1%}")
        "Best LR"       <- .best_lr |> format("{:.0e}")
    format: latex
    caption: "Comparison of attention mechanisms on IMDB sentiment classification"
    label: "tab:attention-comparison"
    output: "tables/attention_comparison.tex"


-- ============================================================
-- Configuration (backends)
-- ============================================================

-- QUESTION: What are the right backends for ML?
-- Storage for checkpoints, tracking for metrics, compute for training.

storage: LocalFS { root: "experiments/" }
tracking: MLflow { uri: "http://localhost:5000" }
    -- alternative: tracking: Wandb { project: "attention-study" }
    -- alternative: tracking: CSV { dir: "results/" }
compute: Auto
    -- alternative: compute: SLURM { partition: "gpu", gpus: 1 }
    -- alternative: compute: Local { device: GPU(0) }
```

---

## Design problems this example exposes

### Problem 1: ML models ARE the logic layer

For a bookstore, the business logic (pricing, discounts) is a small island
in a sea of CRUD boilerplate. For ML, the model definition and training
loop ARE the creative work. There's less boilerplate to eliminate because
the interesting part is bigger.

Where the language DOES help for ML:
- Experiment management (the nested for loop over configs is clean)
- Data pipelines (load, preprocess, split)
- Metric tracking and comparison
- Results generation (the table rendering)
- Backend configuration (swap MLflow for W&B with one line)

Where it probably CAN'T abstract much:
- Model architecture (that's the research)
- Training loop details (custom losses, gradient manipulation, etc.)
- Novel evaluation metrics

This suggests the 100:1 ratio doesn't apply here. Maybe 5:1 or 10:1.
Still valuable, but the pitch is different.

### Problem 2: The verb set is domain-specific

`store`, `serve`, `notify` make sense for web apps. For ML, the natural
verbs are different:
- `train` (run a training loop)
- `evaluate` (compute metrics on a dataset)
- `log` (record a metric or artifact)
- `save` / `load` (checkpoint management)
- `sweep` (hyperparameter search)
- `render` (generate outputs -- tables, plots)

Are these built-in verbs? Or are they a "domain pack" that extends the
base language? If the verb set is fixed, the language is limited. If
it's extensible, we need to design how domain packs work.

### Problem 3: Tensor operations need a sublanguage

`predictions.argmax(-1)`, `h.mean(dim=1)`, `cross_entropy(pred, target)`
-- these are array/tensor operations with broadcasting, dimensional
semantics, and GPU concerns. This is essentially a DSL within the
language. Do we:
- Embed a tensor sublanguage (like Julia's array syntax)?
- Delegate to an external library (like PyTorch) via escape hatch?
- Define tensor ops as another set of verbs with a backend?

### Problem 4: Mutability and training loops

Training loops are inherently stateful: model weights change,
optimizer state accumulates, best_accuracy gets updated. Our language
leans functional (pattern matching, pipelines, immutable-by-default).
Training loops fight that.

Options:
- Explicit mutable bindings (`var best_accuracy = 0`)
- Training as a fold/reduce over epochs (functional but awkward)
- Accept that some code blocks are imperative

### Problem 5: What is "log" exactly?

`log metric: { epoch, step, name, value }` -- is this a verb with a
backend (MLflow, W&B, CSV)? Or is it a side effect? If it's a verb
backed by algebraic effects, then `train` has the effect `log` and the
handler routes to MLflow. That actually works well and is consistent
with the design.

### Problem 6: Experiment = orchestration

The experiment block is really an orchestrator -- it creates multiple
runs, potentially in parallel, across machines. This is closer to a
workflow engine (Airflow, Prefect) than a function call. Does the
language need first-class support for orchestration?

```
experiment "attention_comparison":
    parallel: true
    max_concurrent: 4
    retry: { max: 2, on: [OOM, Timeout] }
    ...
```

This is a LOT of complexity hiding behind a simple-looking block.
