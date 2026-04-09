"""
Experiment: compile a perceptron to a Boolean circuit, apply von Neumann
redundancy, and measure fault tolerance via random gate failures.

Demonstrates that the redundant circuit maintains correct output even when
a significant fraction of its gates fail on every forward pass, while
the original circuit degrades rapidly.
"""

import numpy as np
import time
from circuit import Circuit, von_neumann_redundancy


# ====================================================================== #
#  Fixed-point utilities                                                  #
# ====================================================================== #

def int_to_bits(value: int, num_bits: int) -> list:
    """Signed integer -> list of bits (LSB first, two's complement)."""
    if value < 0:
        value = (1 << num_bits) + value
    return [(value >> i) & 1 for i in range(num_bits)]


def bits_to_int(bits: list, signed: bool = True) -> int:
    """List of bits (LSB first) -> integer."""
    value = sum(b << i for i, b in enumerate(bits))
    if signed and bits[-1] == 1:
        value -= (1 << len(bits))
    return value


def float_to_fixed(value: float, num_bits: int, frac_bits: int) -> int:
    """Float -> fixed-point integer (clamped to range)."""
    max_val = (1 << (num_bits - 1)) - 1
    min_val = -(1 << (num_bits - 1))
    return max(min_val, min(max_val, int(round(value * (1 << frac_bits)))))


def fixed_to_float(int_val: int, frac_bits: int) -> float:
    """Fixed-point integer -> float."""
    return int_val / (1 << frac_bits)


# ====================================================================== #
#  Perceptron compiler                                                    #
# ====================================================================== #

def compile_perceptron(weights: list, bias: float,
                       num_bits: int = 8, frac_bits: int = 4) -> tuple:
    """
    Compile a perceptron  y = sign(w . x + b)  to a Boolean circuit.

    Weights are baked in as constants (constant multipliers = smaller circuit).
    Inputs are k-bit signed fixed-point numbers.

    Returns (circuit, quantized_weights_int, quantized_bias_int).
    """
    n_inputs = len(weights)
    circ = Circuit()

    # Create input wires: num_bits per input variable
    input_groups = []
    for _ in range(n_inputs):
        bits = [circ.add_input() for _ in range(num_bits)]
        input_groups.append(bits)

    # Quantize weights and bias to fixed-point integers
    w_ints = [float_to_fixed(w, num_bits, frac_bits) for w in weights]
    b_int = float_to_fixed(bias, num_bits, frac_bits)

    # Accumulator width: needs to hold sum of products + bias without overflow.
    # Each product is at most |w_max| * |x_max| = 128 * 128 = 16384.
    # After right-shift by frac_bits: 16384 >> 4 = 1024 (fits in 12 bits signed).
    # Sum of n products: up to n * 1024.  Plus bias: up to 127.
    # For n=2: max ~2175.  16 bits signed is plenty.
    acc_width = 2 * num_bits  # 16 bits for 8-bit inputs

    # Multiply each input by its weight (constant multiply + right-shift)
    products = []
    for i in range(n_inputs):
        # Full product: (num_bits + weight_bits + 1) bits, but we use acc_width
        full_product = circ.add_constant_multiply(
            input_groups[i], w_ints[i], result_width=2 * num_bits
        )

        # Right-shift by frac_bits to align fixed point:
        # product has 2*frac_bits fractional bits, we want frac_bits.
        # Take bits [frac_bits : frac_bits + acc_width], sign-extend.
        shifted = full_product[frac_bits:]
        sign = shifted[-1] if shifted else circ.add_constant(0)
        while len(shifted) < acc_width:
            shifted.append(sign)
        products.append(shifted[:acc_width])

    # Sum all products
    acc = products[0]
    for i in range(1, len(products)):
        acc, _ = circ.add_ripple_adder(acc, products[i])
        acc = list(acc)

    # Add bias (sign-extended to acc_width)
    b_bits = int_to_bits(b_int, num_bits)
    b_wires = [circ.add_constant(b) for b in b_bits]
    b_sign = b_wires[-1]
    while len(b_wires) < acc_width:
        b_wires.append(b_sign)
    b_wires = b_wires[:acc_width]

    acc, _ = circ.add_ripple_adder(acc, b_wires)
    acc = list(acc)

    # Output: 1 if result >= 0 (i.e., sign bit is 0)
    sign_bit = acc[acc_width - 1]
    output = circ.add_not(sign_bit)
    circ.set_outputs([output])

    return circ, w_ints, b_int


# ====================================================================== #
#  Verification                                                           #
# ====================================================================== #

def reference_perceptron(x_ints, w_ints, b_int, frac_bits):
    """Compute the expected perceptron output in Python (matching circuit semantics)."""
    # Each product is computed as full integer multiply, then arithmetic right-shift
    # by frac_bits.  Python's >> does arithmetic shift on negatives.
    total = sum((w * x) >> frac_bits for w, x in zip(w_ints, x_ints)) + b_int
    return 1 if total >= 0 else 0


def verify_circuit(circ, w_ints, b_int, num_bits, frac_bits, num_tests=200):
    """Verify the compiled circuit matches the reference on random inputs."""
    rng = np.random.RandomState(123)
    max_val = (1 << (num_bits - 1)) - 1
    min_val = -(1 << (num_bits - 1))
    n_inputs = len(w_ints)

    errors = 0
    for _ in range(num_tests):
        x_ints = [int(rng.randint(min_val, max_val + 1)) for _ in range(n_inputs)]
        expected = reference_perceptron(x_ints, w_ints, b_int, frac_bits)

        input_bits = []
        for x in x_ints:
            input_bits.extend(int_to_bits(x, num_bits))

        actual = circ.evaluate(input_bits)[0]
        if actual != expected:
            errors += 1
            if errors <= 3:  # print first few mismatches for debugging
                print(f"  MISMATCH: x={x_ints} expected={expected} got={actual}")

    return num_tests - errors, num_tests


# ====================================================================== #
#  Fault tolerance experiment                                             #
# ====================================================================== #

def run_experiment(weights, bias, num_bits=8, frac_bits=4,
                   N_values=(3, 5, 7, 11, 15),
                   fault_rates=(0.0, 0.005, 0.01, 0.02, 0.05, 0.10, 0.15),
                   num_trials=5000, num_test_inputs=20):
    """
    Full experiment:
    1. Compile perceptron to Boolean circuit
    2. Apply von Neumann redundancy at several bundle sizes
    3. Measure fraction of correct outputs under random gate faults
    """
    print("=" * 70)
    print("COMPILING PERCEPTRON TO BOOLEAN CIRCUIT")
    print("=" * 70)
    print(f"  Perceptron: y = sign({weights[0]}*x1 + {weights[1]}*x2 + {bias})")
    print(f"  Fixed-point: {num_bits}-bit, {frac_bits} fractional bits")

    original, w_ints, b_int = compile_perceptron(weights, bias, num_bits, frac_bits)

    print(f"  Quantized weights: {w_ints}  "
          f"(floats: {[fixed_to_float(w, frac_bits) for w in w_ints]})")
    print(f"  Quantized bias:    {b_int}  "
          f"(float: {fixed_to_float(b_int, frac_bits)})")

    stats = original.stats()
    print(f"\n  Original circuit:")
    print(f"    Logic gates : {stats['logic_gates']}")
    print(f"    Total nodes : {stats['total_gates']}  "
          f"(incl. {stats['by_type'].get('input', 0)} inputs, "
          f"{stats['by_type'].get('constant', 0)} constants)")
    print(f"    Wires       : {stats['wires']}")

    # Verify
    print(f"\n  Verifying correctness on 200 random inputs...")
    correct, total = verify_circuit(original, w_ints, b_int, num_bits, frac_bits)
    print(f"    {correct}/{total} correct")
    if correct < total:
        print("  ERROR: circuit does not match reference. Aborting.")
        return None

    # Build redundant circuits
    print(f"\n{'=' * 70}")
    print("VON NEUMANN REDUNDANCY")
    print("=" * 70)

    redundant = {}
    for N in N_values:
        rc = von_neumann_redundancy(original, N)
        rs = rc.stats()
        redundant[N] = rc
        print(f"  N={N:2d}:  {rs['logic_gates']:>6d} logic gates  "
              f"({rs['logic_gates'] / stats['logic_gates']:5.1f}x)   "
              f"{rs['wires']:>6d} wires")

    # Generate test inputs
    print(f"\n{'=' * 70}")
    print("FAULT TOLERANCE TEST")
    print("=" * 70)

    rng_inputs = np.random.RandomState(42)
    max_val = (1 << (num_bits - 1)) - 1
    min_val = -(1 << (num_bits - 1))
    n_vars = len(weights)

    test_cases = []  # list of (input_bits, expected_output)
    for _ in range(num_test_inputs):
        x_ints = [int(rng_inputs.randint(min_val, max_val + 1))
                  for _ in range(n_vars)]
        input_bits = []
        for x in x_ints:
            input_bits.extend(int_to_bits(x, num_bits))
        expected = original.evaluate(input_bits)[0]
        test_cases.append((input_bits, expected))

    print(f"  {num_test_inputs} random inputs, {num_trials} fault trials each")
    print(f"  Fault rates: {list(fault_rates)}")
    print()

    # Prepare circuits dict
    circuits = {"Original": (original, 1)}
    for N in N_values:
        circuits[f"N={N:>2d}"] = (redundant[N], N)

    # Header
    name_width = 10
    print(f"{'Fault':>8s}", end="")
    for name in circuits:
        print(f"  {name:>{name_width}s}", end="")
    print()
    print("-" * (10 + (name_width + 2) * len(circuits)))

    results = {}
    total_evals = 0

    for fault_rate in fault_rates:
        row = {}
        print(f"{fault_rate:>8.3f}", end="", flush=True)

        for name, (circ, N) in circuits.items():
            total_correct = 0

            for inp_bits, expected in test_cases:
                # Replicate inputs for redundant circuit
                if N > 1:
                    eval_input = []
                    for b in inp_bits:
                        eval_input.extend([b] * N)
                else:
                    eval_input = inp_bits

                seed = hash((name, fault_rate, tuple(inp_bits))) & 0x7FFFFFFF
                outputs = circ.evaluate_batch(eval_input, fault_rate,
                                              num_trials, seed=seed)
                total_correct += int(np.sum(outputs[:, 0] == expected))
                total_evals += num_trials

            reliability = total_correct / (num_test_inputs * num_trials)
            row[name] = reliability
            print(f"  {reliability:>{name_width}.1%}", end="", flush=True)

        print()
        results[fault_rate] = row

    print(f"\n  Total gate evaluations: ~{total_evals * 100:,.0f}")

    return results


# ====================================================================== #
#  Main                                                                   #
# ====================================================================== #

if __name__ == "__main__":
    t0 = time.time()
    results = run_experiment(
        weights=[0.75, -1.25],
        bias=0.5,
        num_bits=8,
        frac_bits=4,
        N_values=[3, 5, 7, 11, 15],
        fault_rates=[0.0, 0.005, 0.01, 0.02, 0.05, 0.10, 0.15],
        num_trials=5000,
        num_test_inputs=20,
    )
    elapsed = time.time() - t0
    print(f"\n  Elapsed: {elapsed:.1f}s")
