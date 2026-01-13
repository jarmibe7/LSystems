"""
Stochastic LSystem ruleset
"""
import numpy as np

class Rule():
    """
    Stochastic rule, where mutation probabilities add to 1

    Args:
        mutations: List of (mutation, prob) tuples
    """
    def __init__(self, mutations):
        self.mutations = np.zeros((len(mutations),))
        self.probs = np.zeros((len(mutations),))
        for mut, prob in mutations:

        # Assert sum of probs == 1


class Ruleset():
    """
    Stochastic LSystem ruleset, where each rule's probabilities add to 1

    Args:
        rules: List of rules
    """
    def __init__(self, rules):
        for
