"""
Boolean circuit framework for compiling neural networks to fault-tolerant circuits.

Implements:
- Boolean circuit representation and evaluation
- Fixed-point arithmetic subcircuits (adders, constant multipliers)
- Von Neumann redundancy construction (majority voting)
- Batch evaluation with fault injection (vectorized with numpy)
"""

import numpy as np
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict, Tuple


class GateType(Enum):
    INPUT = "input"
    CONSTANT = "constant"
    NOT = "not"
    AND = "and"
    OR = "or"
    XOR = "xor"
    THRESHOLD = "threshold"  # Outputs 1 if sum(inputs) >= threshold


@dataclass
class Gate:
    gate_type: GateType
    inputs: List[int]       # Wire IDs of gate inputs
    output: int             # Wire ID of gate output
    threshold: int = 0      # For THRESHOLD gates
    constant_value: int = 0 # For CONSTANT gates


class Circuit:
    """
    A Boolean circuit: a DAG of gates connected by wires.

    Gates are stored in topological order. Each wire carries a single bit (0 or 1).
    Bits are LSB-first in all multi-bit operations (bits[0] = least significant).
    """

    def __init__(self):
        self.gates: List[Gate] = []
        self.wire_count: int = 0
        self.input_wires: List[int] = []
        self.output_wires: List[int] = []

    def _new_wire(self) -> int:
        w = self.wire_count
        self.wire_count += 1
        return w

    # ------------------------------------------------------------------ #
    #  Primary gates                                                      #
    # ------------------------------------------------------------------ #

    def add_input(self) -> int:
        w = self._new_wire()
        self.input_wires.append(w)
        self.gates.append(Gate(GateType.INPUT, [], w))
        return w

    def add_constant(self, value: int) -> int:
        w = self._new_wire()
        self.gates.append(Gate(GateType.CONSTANT, [], w, constant_value=value))
        return w

    def add_not(self, a: int) -> int:
        w = self._new_wire()
        self.gates.append(Gate(GateType.NOT, [a], w))
        return w

    def add_and(self, a: int, b: int) -> int:
        w = self._new_wire()
        self.gates.append(Gate(GateType.AND, [a, b], w))
        return w

    def add_or(self, a: int, b: int) -> int:
        w = self._new_wire()
        self.gates.append(Gate(GateType.OR, [a, b], w))
        return w

    def add_xor(self, a: int, b: int) -> int:
        w = self._new_wire()
        self.gates.append(Gate(GateType.XOR, [a, b], w))
        return w

    def add_threshold(self, inputs: List[int], threshold: int) -> int:
        """Output 1 if at least `threshold` of the `inputs` are 1."""
        w = self._new_wire()
        self.gates.append(Gate(GateType.THRESHOLD, list(inputs), w, threshold=threshold))
        return w

    def add_majority(self, inputs: List[int]) -> int:
        """Output the majority value of inputs (must be odd count)."""
        n = len(inputs)
        return self.add_threshold(inputs, (n + 1) // 2)

    def set_outputs(self, wires: List[int]):
        self.output_wires = list(wires)

    # ------------------------------------------------------------------ #
    #  Arithmetic subcircuits                                             #
    # ------------------------------------------------------------------ #

    def add_half_adder(self, a: int, b: int) -> Tuple[int, int]:
        """Returns (sum_bit, carry_bit)."""
        s = self.add_xor(a, b)
        c = self.add_and(a, b)
        return s, c

    def add_full_adder(self, a: int, b: int, cin: int) -> Tuple[int, int]:
        """Returns (sum_bit, carry_out)."""
        s1, c1 = self.add_half_adder(a, b)
        s2, c2 = self.add_half_adder(s1, cin)
        cout = self.add_or(c1, c2)
        return s2, cout

    def add_ripple_adder(self, a_bits: List[int], b_bits: List[int],
                         cin: Optional[int] = None) -> Tuple[List[int], int]:
        """
        Add two k-bit numbers. Returns (sum_bits, carry_out).
        Both inputs must have the same number of bits.
        """
        assert len(a_bits) == len(b_bits), \
            f"Bit widths must match: {len(a_bits)} vs {len(b_bits)}"
        if cin is None:
            cin = self.add_constant(0)
        sum_bits = []
        carry = cin
        for i in range(len(a_bits)):
            s, carry = self.add_full_adder(a_bits[i], b_bits[i], carry)
            sum_bits.append(s)
        return sum_bits, carry

    def add_constant_multiply(self, x_bits: List[int], constant: int,
                              result_width: Optional[int] = None) -> List[int]:
        """
        Multiply a signed k-bit number x by a signed integer constant.

        Uses shift-and-add: for each set bit in |constant|, shift x and add.
        Much smaller than a general multiplier when the constant is known at
        circuit-compile time.

        Returns a result_width-bit signed result (sign-extended as needed).
        """
        k = len(x_bits)
        c_abs = abs(constant)

        if result_width is None:
            result_width = k + (c_abs.bit_length() if c_abs > 0 else 1) + 1

        if c_abs == 0:
            return [self.add_constant(0)] * result_width

        # Identify set bits in |constant|
        set_bits = [i for i in range(c_abs.bit_length()) if (c_abs >> i) & 1]

        # Generate shifted, sign-extended copies of x
        sign = x_bits[-1]  # MSB = sign bit of x

        def shift_and_extend(shift: int) -> List[int]:
            shifted = [self.add_constant(0)] * shift + list(x_bits)
            while len(shifted) < result_width:
                shifted.append(sign)
            return shifted[:result_width]

        partials = [shift_and_extend(s) for s in set_bits]

        # Sum partial products
        acc = partials[0]
        for pp in partials[1:]:
            acc, _ = self.add_ripple_adder(acc, pp)
            acc = list(acc)

        # Negate result if constant was negative
        if constant < 0:
            inverted = [self.add_not(b) for b in acc]
            zeros = [self.add_constant(0)] * result_width
            acc, _ = self.add_ripple_adder(inverted, zeros,
                                           cin=self.add_constant(1))
            acc = list(acc)

        return acc

    # ------------------------------------------------------------------ #
    #  Evaluation                                                         #
    # ------------------------------------------------------------------ #

    def evaluate(self, input_values: List[int]) -> List[int]:
        """Evaluate the circuit with no faults. For debugging/verification."""
        wire_vals: Dict[int, int] = {}
        input_idx = 0

        for gate in self.gates:
            if gate.gate_type == GateType.INPUT:
                wire_vals[gate.output] = input_values[input_idx]
                input_idx += 1
                continue
            if gate.gate_type == GateType.CONSTANT:
                wire_vals[gate.output] = gate.constant_value
                continue

            ins = [wire_vals[i] for i in gate.inputs]

            if gate.gate_type == GateType.NOT:
                wire_vals[gate.output] = 1 - ins[0]
            elif gate.gate_type == GateType.AND:
                wire_vals[gate.output] = 1 if (ins[0] and ins[1]) else 0
            elif gate.gate_type == GateType.OR:
                wire_vals[gate.output] = 1 if (ins[0] or ins[1]) else 0
            elif gate.gate_type == GateType.XOR:
                wire_vals[gate.output] = ins[0] ^ ins[1]
            elif gate.gate_type == GateType.THRESHOLD:
                wire_vals[gate.output] = 1 if sum(ins) >= gate.threshold else 0
            else:
                raise ValueError(f"Unknown gate type: {gate.gate_type}")

        return [wire_vals[w] for w in self.output_wires]

    def evaluate_batch(self, input_values: List[int], fault_prob: float,
                       num_trials: int, seed: int = 42) -> np.ndarray:
        """
        Evaluate the circuit num_trials times with random independent gate faults.

        Each non-input, non-constant gate independently fails with probability
        fault_prob on each trial, outputting a uniformly random bit.

        Returns array of shape (num_trials, num_outputs).
        """
        rng = np.random.RandomState(seed)

        # Pre-allocate wire values: shape (wire_count, num_trials)
        wire_vals = np.zeros((self.wire_count, num_trials), dtype=np.int8)
        input_idx = 0

        for gate in self.gates:
            out = gate.output

            if gate.gate_type == GateType.INPUT:
                wire_vals[out, :] = input_values[input_idx]
                input_idx += 1
                continue
            if gate.gate_type == GateType.CONSTANT:
                wire_vals[out, :] = gate.constant_value
                continue

            # Compute correct output (vectorized across trials)
            if gate.gate_type == GateType.NOT:
                correct = 1 - wire_vals[gate.inputs[0]]
            elif gate.gate_type == GateType.AND:
                correct = wire_vals[gate.inputs[0]] & wire_vals[gate.inputs[1]]
            elif gate.gate_type == GateType.OR:
                correct = wire_vals[gate.inputs[0]] | wire_vals[gate.inputs[1]]
            elif gate.gate_type == GateType.XOR:
                correct = wire_vals[gate.inputs[0]] ^ wire_vals[gate.inputs[1]]
            elif gate.gate_type == GateType.THRESHOLD:
                input_sum = wire_vals[gate.inputs].sum(axis=0, dtype=np.int32)
                correct = (input_sum >= gate.threshold).astype(np.int8)
            else:
                raise ValueError(f"Unknown gate type: {gate.gate_type}")

            # Inject faults
            if fault_prob > 0:
                fault_mask = rng.random(num_trials) < fault_prob
                random_bits = rng.randint(0, 2, num_trials, dtype=np.int8)
                wire_vals[out] = np.where(fault_mask, random_bits, correct)
            else:
                wire_vals[out] = correct

        return np.column_stack([wire_vals[w] for w in self.output_wires])

    def stats(self) -> Dict:
        """Circuit statistics."""
        counts: Dict[str, int] = {}
        for g in self.gates:
            t = g.gate_type.value
            counts[t] = counts.get(t, 0) + 1
        logic_gates = sum(v for k, v in counts.items()
                          if k not in ("input", "constant"))
        return {
            "total_gates": len(self.gates),
            "logic_gates": logic_gates,
            "wires": self.wire_count,
            "inputs": len(self.input_wires),
            "outputs": len(self.output_wires),
            "by_type": counts,
        }


# ====================================================================== #
#  Von Neumann Redundancy Construction                                    #
# ====================================================================== #

def von_neumann_redundancy(original: Circuit, N: int) -> Circuit:
    """
    Apply von Neumann's redundancy construction to a Boolean circuit.

    Each wire is replaced by a bundle of N wires.
    Each logic gate is replaced by N independent copies, followed by N
    independent majority-vote restoration gates.

    Input and constant wires are simply replicated (no faults on them).

    The resulting circuit tolerates transient gate failures: if each gate
    fails independently with probability epsilon < ~1/6, the output error
    probability decreases exponentially with N.

    Args:
        original: The circuit to make fault-tolerant.
        N: Bundle size (must be odd, >= 3). Higher = more reliable.

    Returns:
        A new Circuit with the same logical function but fault tolerance.
    """
    assert N >= 1 and N % 2 == 1, "N must be a positive odd number"

    circ = Circuit()
    bundles: Dict[int, List[int]] = {}  # original wire -> list of N new wires

    for gate in original.gates:
        if gate.gate_type == GateType.INPUT:
            bundle = [circ.add_input() for _ in range(N)]
            bundles[gate.output] = bundle

        elif gate.gate_type == GateType.CONSTANT:
            bundle = [circ.add_constant(gate.constant_value) for _ in range(N)]
            bundles[gate.output] = bundle

        else:
            # Step 1: N independent copies of the gate
            temps = []
            for i in range(N):
                inputs_i = [bundles[inp][i] for inp in gate.inputs]

                if gate.gate_type == GateType.NOT:
                    t = circ.add_not(inputs_i[0])
                elif gate.gate_type == GateType.AND:
                    t = circ.add_and(inputs_i[0], inputs_i[1])
                elif gate.gate_type == GateType.OR:
                    t = circ.add_or(inputs_i[0], inputs_i[1])
                elif gate.gate_type == GateType.XOR:
                    t = circ.add_xor(inputs_i[0], inputs_i[1])
                elif gate.gate_type == GateType.THRESHOLD:
                    t = circ.add_threshold(inputs_i, gate.threshold)
                else:
                    raise ValueError(f"Unsupported: {gate.gate_type}")
                temps.append(t)

            # Step 2: Majority restoration — each bundle wire is the
            # majority vote of all N temp wires.  Each majority gate is
            # itself a threshold gate that can fail independently.
            bundle = [circ.add_majority(temps) for _ in range(N)]
            bundles[gate.output] = bundle

    # Final outputs: one majority vote per original output
    final_outputs = []
    for w in original.output_wires:
        final_outputs.append(circ.add_majority(bundles[w]))
    circ.set_outputs(final_outputs)

    return circ
