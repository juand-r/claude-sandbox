"""
Example: A short text on Bayesian reasoning, annotated as a knowledge space.

The text covers: prior probability, likelihood, Bayes' theorem, and
a medical testing example. There are two natural entry paths:
1. Start with the formal/mathematical side (priors, likelihood, theorem)
2. Start with the intuitive/example side (medical test, base rates)

This lets us test whether the knowledge space formalism handles the
path-dependent convergence correctly.
"""

from knowledge_space import Concept, TextNode, ReaderState, KnowledgeSpace


# --- Concepts ---

c_probability = Concept("prob", "Probability basics",
    "What a probability is, values between 0 and 1")
c_conditional = Concept("cond_prob", "Conditional probability",
    "P(A|B) -- probability of A given B")
c_prior = Concept("prior", "Prior probability",
    "P(H) -- probability of hypothesis before seeing evidence")
c_likelihood = Concept("likelihood", "Likelihood",
    "P(E|H) -- probability of evidence given hypothesis")
c_bayes_theorem = Concept("bayes", "Bayes' theorem",
    "P(H|E) = P(E|H)P(H)/P(E)")
c_base_rate = Concept("base_rate", "Base rate",
    "Prevalence of a condition in the population")
c_false_positive = Concept("false_pos", "False positive",
    "Test says positive when condition is absent")
c_medical_testing = Concept("med_test", "Medical testing intuition",
    "Why a positive test doesn't mean you're sick")
c_base_rate_neglect = Concept("br_neglect", "Base rate neglect",
    "The cognitive bias of ignoring base rates")


# --- Text Nodes ---

node_prob_intro = TextNode(
    id="prob_intro",
    title="What is Probability?",
    content="""
    A probability is a number between 0 and 1 that represents how likely
    something is to happen. 0 means impossible, 1 means certain. If you
    flip a fair coin, the probability of heads is 0.5.
    """,
    teaches=frozenset({c_probability}),
    requires=frozenset(),
)

node_conditional = TextNode(
    id="conditional",
    title="Conditional Probability",
    content="""
    Sometimes we want to know the probability of something *given* that
    something else has happened. We write P(A|B) and read it as "the
    probability of A given B." For example, the probability it rains
    given that there are dark clouds is higher than the unconditional
    probability of rain.
    """,
    teaches=frozenset({c_conditional}),
    requires=frozenset({c_probability}),
)

node_prior = TextNode(
    id="prior",
    title="Prior Probability",
    content="""
    Before seeing any evidence, we have some belief about how likely
    a hypothesis is. This is the prior probability, P(H). It represents
    our state of knowledge before new data arrives. For example, before
    testing, the prior probability that a randomly selected person has
    a rare disease is the disease's prevalence in the population.
    """,
    teaches=frozenset({c_prior, c_base_rate}),
    requires=frozenset({c_probability}),
)

node_likelihood = TextNode(
    id="likelihood",
    title="Likelihood",
    content="""
    The likelihood P(E|H) asks: if the hypothesis is true, how probable
    is the evidence we observed? This is not the same as P(H|E) -- a
    subtle but critical distinction. A test might be very likely to come
    back positive if you have a disease (high likelihood), but that
    doesn't tell you the probability you have the disease given a
    positive test.
    """,
    teaches=frozenset({c_likelihood}),
    requires=frozenset({c_conditional}),
)

node_bayes = TextNode(
    id="bayes_theorem",
    title="Bayes' Theorem",
    content="""
    Bayes' theorem combines prior and likelihood:

        P(H|E) = P(E|H) * P(H) / P(E)

    It tells us how to update our beliefs when we see new evidence.
    The posterior P(H|E) is proportional to the likelihood times the prior.
    """,
    teaches=frozenset({c_bayes_theorem}),
    requires=frozenset({c_prior, c_likelihood}),
)

# --- Alternative entry: intuitive path ---

node_medical_setup = TextNode(
    id="medical_setup",
    title="A Surprising Medical Test",
    content="""
    Suppose a disease affects 1 in 1000 people. A test for it is 99%
    accurate: if you have the disease, the test is positive 99% of the
    time, and if you don't, the test is negative 99% of the time.

    You test positive. What's the probability you actually have the disease?

    Most people guess around 99%. The real answer is about 9%.
    """,
    teaches=frozenset({c_base_rate, c_false_positive}),
    requires=frozenset(),
)

node_base_rate_explanation = TextNode(
    id="base_rate_explain",
    title="Why the Base Rate Matters",
    content="""
    The key is the base rate -- only 1 in 1000 people have the disease.
    Out of 1000 people tested:
    - 1 person has it, and the test correctly identifies them (true positive)
    - 999 don't have it, but ~10 get false positives (1% of 999)

    So of ~11 positive results, only 1 actually has the disease.
    That's about 9%, not 99%.

    This is called base rate neglect: ignoring how rare the condition is
    when interpreting the test result.
    """,
    teaches=frozenset({c_medical_testing, c_base_rate_neglect}),
    requires=frozenset({c_base_rate, c_false_positive}),
)

# --- Convergence node: connects both paths ---

node_synthesis = TextNode(
    id="synthesis",
    title="Bayes' Theorem and Medical Testing",
    content="""
    The medical testing puzzle is Bayes' theorem in action:

        P(disease | positive) = P(positive | disease) * P(disease) / P(positive)

    - P(disease) = 0.001 (the base rate / prior)
    - P(positive | disease) = 0.99 (the likelihood)
    - P(positive) = P(pos|disease)*P(disease) + P(pos|no disease)*P(no disease)
                   = 0.99*0.001 + 0.01*0.999 ≈ 0.011

    So P(disease | positive) = 0.99 * 0.001 / 0.011 ≈ 0.09

    The formal machinery and the intuitive counting arrive at the same answer,
    but from different directions. The theorem gives you the general tool;
    the example gives you the intuition for why priors matter so much.
    """,
    teaches=frozenset(),  # synthesis, doesn't introduce new concepts
    requires=frozenset({c_bayes_theorem, c_medical_testing}),
)


def build_example() -> KnowledgeSpace:
    ks = KnowledgeSpace()
    for node in [
        node_prob_intro, node_conditional, node_prior, node_likelihood,
        node_bayes, node_medical_setup, node_base_rate_explanation,
        node_synthesis,
    ]:
        ks.add_node(node)
    return ks


def walk_through():
    """Demonstrate two different reading paths through the same material."""
    ks = build_example()

    print("=== Knowledge Space Validation ===")
    issues = ks.validate()
    if issues:
        for issue in issues:
            print(f"  ISSUE: {issue}")
    else:
        print("  No structural issues found.")

    print(f"\n  Entry points: {[n.id for n in ks.entry_points()]}")
    print(f"  Convergence points: {[n.id for n in ks.convergence_points()]}")
    print(f"  Total concepts: {len(ks.concepts_taught())}")

    # --- Path 1: Formal first ---
    print("\n=== Path 1: Formal/Mathematical ===")
    state = ReaderState()
    formal_order = [
        "prob_intro", "conditional", "prior", "likelihood",
        "bayes_theorem", "medical_setup", "base_rate_explain", "synthesis"
    ]
    for node_id in formal_order:
        node = ks.nodes[node_id]
        available = ks.available_from(state)
        available_ids = [n.id for n in available]
        print(f"\n  Available: {available_ids}")
        if node_id not in available_ids:
            print(f"  ** {node_id} not available yet, skipping")
            continue
        bridging = ks.bridging_summary_needed(state, node)
        if bridging:
            print(f"  ** Bridging needed for: {[c.id for c in bridging]}")
        print(f"  Reading: {node.title}")
        state = state.read(node)
        print(f"  Knowledge: {sorted(c.id for c in state.knowledge)}")

    # --- Path 2: Intuitive first ---
    print("\n\n=== Path 2: Intuitive/Example ===")
    state = ReaderState()
    intuitive_order = [
        "medical_setup", "base_rate_explain",
        "prob_intro", "conditional", "prior", "likelihood",
        "bayes_theorem", "synthesis"
    ]
    for node_id in intuitive_order:
        node = ks.nodes[node_id]
        available = ks.available_from(state)
        available_ids = [n.id for n in available]
        print(f"\n  Available: {available_ids}")
        if node_id not in available_ids:
            print(f"  ** {node_id} not available yet, skipping")
            continue
        bridging = ks.bridging_summary_needed(state, node)
        if bridging:
            print(f"  ** Bridging needed for: {[c.id for c in bridging]}")
        print(f"  Reading: {node.title}")
        state = state.read(node)
        print(f"  Knowledge: {sorted(c.id for c in state.knowledge)}")


if __name__ == "__main__":
    walk_through()
