"""
Metric computation from trial logs.

All metrics are computed automatically from the logs — no human judgment required.

Primary metrics:
  - success: did they escape? (binary)
  - step_efficiency: actual_turns / optimal_turns (lower is better, 1.0 is optimal)
  - message_efficiency: messages_sent / optimal_messages (lower is better, 1.0 is optimal)

Secondary metrics:
  - redundancy_score: proportion of duplicate puzzle attempts by both agents
  - info_utilization: (placeholder) what fraction of load-bearing tokens were transmitted
"""

from dataclasses import dataclass
from .models import Room
from .harness import TrialResult


@dataclass
class MetricProfile:
    """Complete metric profile for a single trial."""
    room_id: str
    difficulty: str

    # Primary
    success: bool
    step_efficiency: float      # actual / optimal (1.0 = perfect, higher = worse)
    message_efficiency: float   # messages / optimal_messages

    # Secondary
    redundancy_score: float     # 0.0 = no redundancy, 1.0 = fully redundant
    total_turns: int
    total_messages: int

    def to_dict(self) -> dict:
        return {
            "room_id": self.room_id,
            "difficulty": self.difficulty,
            "success": self.success,
            "step_efficiency": round(self.step_efficiency, 2),
            "message_efficiency": round(self.message_efficiency, 2),
            "redundancy_score": round(self.redundancy_score, 2),
            "total_turns": self.total_turns,
            "total_messages": self.total_messages,
        }

    def summary_line(self) -> str:
        """One-line summary for table output."""
        status = "PASS" if self.success else "FAIL"
        return (
            f"{self.room_id:<22} {self.difficulty:<8} {status:<6} "
            f"turns={self.total_turns:<3} msgs={self.total_messages:<3} "
            f"step_eff={self.step_efficiency:<5.2f} msg_eff={self.message_efficiency:<5.2f} "
            f"redundancy={self.redundancy_score:<4.2f}"
        )


def compute_metrics(result: TrialResult, room: Room) -> MetricProfile:
    """Compute all metrics from a trial result and room definition."""
    meta = room.metadata

    # Step efficiency: actual submit/look actions / optimal
    # We count all engine actions (submits + looks), not messages
    engine_actions = len(result.action_log)
    step_eff = engine_actions / meta.optimal_steps if meta.optimal_steps > 0 else float('inf')

    # Message efficiency
    msg_eff = (result.messages_sent / meta.optimal_messages
               if meta.optimal_messages > 0 else float('inf'))

    # Redundancy: count puzzles attempted by both agents
    redundancy = _compute_redundancy(result)

    return MetricProfile(
        room_id=result.room_id,
        difficulty=meta.difficulty,
        success=result.escaped,
        step_efficiency=step_eff,
        message_efficiency=msg_eff,
        redundancy_score=redundancy,
        total_turns=result.total_turns,
        total_messages=result.messages_sent,
    )


def _compute_redundancy(result: TrialResult) -> float:
    """
    Compute redundancy score: what fraction of puzzles were attempted by both agents?

    0.0 = no overlap (each puzzle attempted by only one agent)
    1.0 = full overlap (every puzzle attempted by both agents)
    """
    # Group submit actions by puzzle
    puzzle_submitters: dict[str, set[str]] = {}
    for entry in result.action_log:
        if entry["type"] == "submit" and entry["target"]:
            target = entry["target"]
            if target not in puzzle_submitters:
                puzzle_submitters[target] = set()
            puzzle_submitters[target].add(entry["agent"])

    if not puzzle_submitters:
        return 0.0

    # Count puzzles with submissions from both agents
    both_attempted = sum(1 for agents in puzzle_submitters.values() if len(agents) > 1)
    return both_attempted / len(puzzle_submitters)


def print_results_table(profiles: list[MetricProfile]):
    """Print a formatted results table."""
    header = (
        f"{'Room':<22} {'Diff':<8} {'Result':<6} "
        f"{'Turns':<6} {'Msgs':<6} "
        f"{'StepEff':<8} {'MsgEff':<8} "
        f"{'Redund':<7}"
    )
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    for p in profiles:
        print(p.summary_line())
    print("=" * len(header))

    # Summary stats
    n_success = sum(1 for p in profiles if p.success)
    print(f"\nSuccess rate: {n_success}/{len(profiles)} "
          f"({100 * n_success / len(profiles):.0f}%)")
    if n_success > 0:
        successful = [p for p in profiles if p.success]
        avg_step = sum(p.step_efficiency for p in successful) / n_success
        avg_msg = sum(p.message_efficiency for p in successful) / n_success
        print(f"Avg step efficiency (successful): {avg_step:.2f}")
        print(f"Avg message efficiency (successful): {avg_msg:.2f}")
