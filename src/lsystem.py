"""
Class for string-based LSystems in Python with turtle graphics
"""
from .ruleset import Ruleset

class LSystem():
    """
    Simple string-based LSystem

    Arg:
        axiom: System initial state
        rules: Dictionary: character -> Rule
    """
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.ruleset = Ruleset(rules)

    def process_string(self, s):
        out = []
        for c in s:
            out.append(self.ruleset.replace(c))
        return "".join(out)

    def generate(self, num_generations):
        curr_string = self.axiom
        for g in range(num_generations):
            curr_string = self.process_string(curr_string)
        
        return curr_string