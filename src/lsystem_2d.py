"""
Class for 2D LSystems in Python with turtle graphics
"""
from src.ruleset import Ruleset

class LSystem2D():
    """
    Simple 2D LSystem

    Arg:
        axiom: System initial state
        rules: Dictionary: character -> Rule
    """
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.ruleset = Ruleset(rules)

    def process_string(self, s):
        s_new = ""
        for c in s:
            s_new = s_new + self.ruleset.replace(c)

        return s_new

    def generate(self, num_generations):
        curr_string = self.axiom
        for g in range(num_generations):
            curr_string = self.process_string(curr_string)
        
        return curr_string