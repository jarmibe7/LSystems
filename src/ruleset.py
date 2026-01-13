"""
Stochastic LSystem ruleset
"""
import numpy as np

class Rule():
    """
    Stochastic rule, where mutation probabilities add to 1

    Args:
        mappings: List of (mutation, prob) tuples
    """
    def __init__(self, mappings):
        self.mutations = np.empty((len(mappings),), dtype=object)
        self.probs = np.zeros((len(mappings),))
        for i, tup in enumerate(mappings):
            mut, prob = tup
            self.mutations[i] = mut
            self.probs[i] = prob

        # Assert sum of probs == 1
        assert self.probs.sum() == 1.0

    def sample(self):
        return np.random.choice(a=self.mutations, p=self.probs)


class Ruleset():
    """
    Stochastic LSystem ruleset, where each rule's probabilities add to 1

    Args:
        rules: Dictionary: character -> Rule
    """
    def __init__(self, rules):
        self.rule_dict = rules

    def replace(self, c):
        if c in self.rule_dict:
            return self.rule_dict[c].sample()
        else:
            raise ValueError('Character not in ruleset!')
