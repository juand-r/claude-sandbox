"""Tests for the core effect system and verb framework."""

import warnings
import pytest
from effects import Effect, perform, handle, handle_many, UnhandledEffectError
from verbs import verb, VerbStarted, VerbCompleted, VerbFailed, UndeclaredEffectWarning, list_verbs, get_verb, _registry
from ml_effects import Log, LogParams, Save, AllocCompute, ReleaseCompute, Progress
from ml_verbs import train, evaluate, sweep, analyze, render_table, Config, Run


# ===========================================================================
# Effect system tests
# ===========================================================================

class TestEffects:

    def test_perform_with_handler(self):
        """Effects dispatch to the correct handler."""
        class Greet(Effect):
            def __init__(self, name):
                self.name = name

        results = []
        with handle(Greet, lambda e: results.append(e.name)):
            perform(Greet("world"))

        assert results == ["world"]

    def test_perform_without_handler_raises(self):
        """Unhandled effects raise UnhandledEffectError."""
        class Orphan(Effect):
            pass

        with pytest.raises(UnhandledEffectError):
            perform(Orphan())

    def test_handler_returns_value(self):
        """Handlers can return values to the performer."""
        class GetAnswer(Effect):
            pass

        with handle(GetAnswer, lambda e: 42):
            result = perform(GetAnswer())

        assert result == 42

    def test_nested_handlers_override(self):
        """Inner handlers shadow outer handlers for the same effect type."""
        class Say(Effect):
            pass

        results = []

        with handle(Say, lambda e: results.append("outer")):
            perform(Say())
            with handle(Say, lambda e: results.append("inner")):
                perform(Say())
            perform(Say())

        assert results == ["outer", "inner", "outer"]

    def test_handle_many(self):
        """handle_many installs multiple handlers at once."""
        class A(Effect):
            pass
        class B(Effect):
            pass

        results = []
        with handle_many({
            A: lambda e: results.append("a"),
            B: lambda e: results.append("b"),
        }):
            perform(A())
            perform(B())

        assert results == ["a", "b"]

    def test_handlers_cleaned_up_after_exception(self):
        """Handlers are removed even if the body raises."""
        class Temp(Effect):
            pass

        try:
            with handle(Temp, lambda e: None):
                raise ValueError("boom")
        except ValueError:
            pass

        # Handler should be gone now
        with pytest.raises(UnhandledEffectError):
            perform(Temp())

    def test_handler_inheritance(self):
        """A handler for a parent effect type catches child effects."""
        class Base(Effect):
            pass
        class Child(Base):
            pass

        results = []
        with handle(Base, lambda e: results.append(type(e).__name__)):
            perform(Child())

        assert results == ["Child"]


# ===========================================================================
# Verb system tests
# ===========================================================================

class TestVerbs:

    def test_verb_registration(self):
        """@verb registers the function in the registry."""
        # train, evaluate, sweep are registered by ml_verbs import
        assert "train" in _registry
        assert "evaluate" in _registry
        assert "sweep" in _registry

    def test_verb_schema(self):
        """Verb schema captures metadata correctly."""
        schema = get_verb("train")
        assert schema.name == "train"
        assert Log in schema.needs
        assert Save in schema.needs
        assert schema.describes != ""

    def test_verb_missing_handler_raises(self):
        """Verb raises if required effects are not handled."""
        with pytest.raises(RuntimeError, match="requires effect handlers"):
            train(model=None, data=None, config=Config(epochs=1))

    def test_verb_missing_partial_handler_raises(self):
        """Verb raises even if some (but not all) handlers are present."""
        with handle(Log, lambda e: None):
            with pytest.raises(RuntimeError, match="requires effect handlers"):
                train(model=None, data=None, config=Config(epochs=1))

    def test_verb_lifecycle_events(self):
        """Verbs emit lifecycle effects when handlers are present."""
        events = []

        def lifecycle(e):
            events.append(type(e).__name__)

        all_handlers = {
            Log: lambda e: None,
            LogParams: lambda e: None,
            Save: lambda e: None,
            AllocCompute: lambda e: {"device": "cpu"},
            ReleaseCompute: lambda e: None,
            Progress: lambda e: None,
            VerbStarted: lifecycle,
            VerbCompleted: lifecycle,
            VerbFailed: lifecycle,
        }

        with handle_many(all_handlers):
            train(model=None, data=None, config=Config(epochs=1))

        assert "VerbStarted" in events
        assert "VerbCompleted" in events

    def test_undeclared_effect_warns(self):
        """Verb warns if it performs effects not listed in `needs`."""

        class Secret(Effect):
            pass

        @verb(name="_test_sneaky", needs=[], describes="test verb")
        def sneaky():
            perform(Secret())

        with handle(Secret, lambda e: None):
            with pytest.warns(UndeclaredEffectWarning, match="Secret"):
                sneaky()

    def test_declared_effects_no_warning(self):
        """Verb does NOT warn when all performed effects are declared."""

        class Declared(Effect):
            pass

        @verb(name="_test_honest", needs=[Declared], describes="test verb")
        def honest():
            perform(Declared())

        with handle(Declared, lambda e: None):
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                honest()  # should not raise


# ===========================================================================
# ML verb tests
# ===========================================================================

class TestMLVerbs:

    def _make_handlers(self, log_sink=None):
        """Create a minimal handler set for testing."""
        return {
            Log: log_sink or (lambda e: None),
            LogParams: lambda e: None,
            Save: lambda e: None,
            AllocCompute: lambda e: {"device": "cpu"},
            ReleaseCompute: lambda e: None,
            Progress: lambda e: None,
            VerbStarted: lambda e: None,
            VerbCompleted: lambda e: None,
            VerbFailed: lambda e: None,
        }

    def test_train_returns_run(self):
        """train() returns a Run with metrics."""
        with handle_many(self._make_handlers()):
            run = train(model=None, data=None, config=Config(epochs=3))

        assert isinstance(run, Run)
        assert run.status == "completed"
        assert run.final("val_accuracy") is not None
        assert run.final("train_loss") is not None

    def test_train_logs_metrics(self):
        """train() performs Log effects for each metric."""
        logged = []

        def capture_log(e):
            logged.append((e.key, e.step))

        with handle_many(self._make_handlers(log_sink=capture_log)):
            train(model=None, data=None, config=Config(epochs=3))

        # Should have logged train_loss and val_accuracy for each epoch
        keys = [k for k, _ in logged]
        assert "train_loss" in keys
        assert "val_accuracy" in keys
        assert len(logged) == 6  # 2 metrics * 3 epochs

    def test_train_with_custom_fn(self):
        """train() accepts a custom training function."""
        def my_train(model, data, config, callback):
            callback(0, loss=0.5, accuracy=0.8)
            callback(1, loss=0.3, accuracy=0.9)

        with handle_many(self._make_handlers()):
            run = train(model=None, data=None,
                       config=Config(epochs=2),
                       train_fn=my_train)

        assert run.final("accuracy") == 0.9
        assert run.final("loss") == 0.3

    def test_evaluate_returns_run(self):
        """evaluate() returns a Run with metrics."""
        with handle(Log, lambda e: None):
            run = evaluate(model=None, data=None, config=Config())

        assert isinstance(run, Run)
        assert run.final("test_accuracy") is not None

    def test_sweep_runs_all_configs(self):
        """sweep() runs all combinations in the cartesian product."""
        with handle_many(self._make_handlers()):
            runs = sweep(
                verb_fn=train,
                base_config={"optimizer": "sgd"},
                sweep_params={
                    "lr": [0.1, 0.01],
                    "epochs": [2, 3],
                },
            )

        assert len(runs) == 4  # 2 * 2
        configs = [r.config.to_dict() for r in runs]
        assert all(c["optimizer"] == "sgd" for c in configs)

    def test_sweep_handles_failures(self):
        """sweep() catches failures and continues."""
        call_count = 0

        def sometimes_fail(model, data, config):
            nonlocal call_count
            call_count += 1
            if config.lr == 0.1:
                raise ValueError("lr too high")
            return Run(config=config, metrics=__import__("ml_verbs").Metrics())

        with handle_many(self._make_handlers()):
            runs = sweep(
                verb_fn=sometimes_fail,
                base_config={},
                sweep_params={"lr": [0.1, 0.01], "epochs": [1]},
            )

        assert len(runs) == 2
        assert runs[0].status == "failed"
        assert runs[1].status == "completed"


# ===========================================================================
# Config and Metrics tests
# ===========================================================================

class TestConfig:

    def test_attribute_access(self):
        c = Config(lr=0.01, epochs=10)
        assert c.lr == 0.01
        assert c.epochs == 10

    def test_missing_attribute_raises(self):
        c = Config(lr=0.01)
        with pytest.raises(AttributeError):
            _ = c.nonexistent

    def test_to_dict(self):
        c = Config(a=1, b="two")
        assert c.to_dict() == {"a": 1, "b": "two"}


class TestAnalyze:

    def _make_run(self, lr, val_acc, status="completed"):
        from ml_verbs import Metrics
        m = Metrics()
        m.log(0, val_accuracy=val_acc)
        return Run(config=Config(lr=lr), metrics=m, status=status)

    def test_analyze_finds_best(self):
        runs = [
            self._make_run(0.1, 0.7),
            self._make_run(0.01, 0.9),
            self._make_run(0.001, 0.8),
        ]
        result = analyze(runs)
        assert result["best_val_accuracy"] == 0.9
        assert result["best_config"]["lr"] == 0.01

    def test_analyze_ignores_failed(self):
        runs = [
            self._make_run(0.1, 0.0, status="failed"),
            self._make_run(0.01, 0.8),
        ]
        result = analyze(runs)
        assert result["completed"] == 1
        assert result["failed"] == 1

    def test_render_table(self):
        runs = [
            self._make_run(0.1, 0.7),
            self._make_run(0.01, 0.9),
        ]
        table = render_table(runs, {
            "LR": lambda r: r.config.lr,
            "Acc": lambda r: r.final("val_accuracy"),
        })
        assert "LR" in table
        assert "Acc" in table
        assert "0.1000" in table
        assert "0.9000" in table


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
