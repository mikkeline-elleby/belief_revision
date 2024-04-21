# belief_base.py

class BeliefBase:
    def __init__(self):
        self.formulas = set()

    def add_formula(self, formula):
        self.formulas.add(formula)
        return self

    def remove_formula(self, formula):
        self.formulas.remove(formula)

    def query_formula(self, formula):
        return formula in self.formulas
    
