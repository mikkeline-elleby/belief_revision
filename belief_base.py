# belief_base.py

from entailment import resolution  
import itertools
import re
from copy import deepcopy
from agm_postulates import check_agm_revision_postulates

VARIABLE_REGEX = re.compile(r"and|or|not|imp|bi|([a-zA-Z])")

def parenthesis_valid(variable):
    c = 0
    for letter in variable:
        if letter == "(":
            c += 1
        elif letter == ")":
            c -= 1
        if c < 0:
            return False
    return c == 0

def create_valid_formula(variables):
    new_variables = []
    current_variable = []

    for var in variables:
        current_variable.append(var)

        if parenthesis_valid(','.join(current_variable)):
            new_variables.append(','.join(current_variable))
            current_variable = []
    
    return new_variables


def parse_formula(formula):
    parts = formula.split('(')
    operator = parts[0]
    variables = create_valid_formula(('('.join(parts[1:])).rstrip(')').split(','))
    return operator, variables

def evaluate_formula(formula, truth_assignment):

    operator, variables = formula

    if variables == [''] : 
        return truth_assignment[operator]

    def evaluate(var):
        return truth_assignment[var] if var in truth_assignment else evaluate_formula(parse_formula(var), truth_assignment)

    if operator == 'and':
        return all(evaluate(var) for var in variables)
    elif operator == 'or':
        return any(evaluate(var) for var in variables)
    elif operator == 'not':
        return not evaluate(variables[0])
    elif operator == 'imp':
        return not evaluate(variables[0]) or evaluate(variables[1])
    elif operator == 'bi':
        return evaluate(variables[0]) == evaluate(variables[1])

def find_variable(formula):
    variables = []
    for match in VARIABLE_REGEX.findall(formula):
        if match is not None and match != "":
            variables.append(match)
    return variables

def entrenchment(formula_str):
    #count number of satisfiable formulas 
    formula = parse_formula(formula_str)
    variables = find_variable(formula_str)
    truth_assignments = itertools.product([True, False], repeat=len(variables))
    satisfiable_count = sum(evaluate_formula(formula, dict(zip(variables, assignment))) for assignment in truth_assignments)
    return satisfiable_count

# Example usage
formula_str = "p"

satisfiable_count = entrenchment(formula_str)
print("Number of satisfiable formulas:", satisfiable_count)

def subset_of_set(s, size):
    #finds the subset of a set
    if size <= 0 or len(s) == 0 or size > len(s):
        return set()

    if size == len(s):
        return s

    without_element = subset_of_set(s[1:], size)
    with_element = {frozenset({next(iter(s))}).union(e) for e in subset_of_set(s[1:], size - 1)}
    return with_element.union(without_element)

##############################################################################################

##############################################################################################

class BeliefBase: 
    def __init__(self):
        self.formulas = set()  # STILL SET :P 

    def expansion(self, alpha):
        #add alpha to the belief base 
        self.formulas.add(alpha)
        return self

    def contraction(self, alpha):
        #alpha is removed from the belief base.

        for length in range(len(self.formulas), 0, -1):
            valid_kb = set()
            
            for sub_kb in subset_of_set(self.formulas, length):
                print(sub_kb)
                negated_alpha = "not(" + alpha + ")"
                print(negated_alpha)
                if not resolution([sub_kb], alpha):
                    valid_kb.add(sub_kb)

            if len(valid_kb) > 0:
                best_kb = set()
                best_score = 0

                for kb in valid_kb:
                    score = entrenchment(kb)
                    if score > best_score:
                        best_kb = kb
                        best_score = score
                        print(best_kb)

                self.formulas = set(best_kb)
                return 

    def revision(self, new_formula):
        # make copy of belief base for AGM checking
        B_old = deepcopy(self)
        
        # check resolution to determine if revision is needed
        if resolution(list(self.formulas), new_formula):
            return 
        
        else:
            self.contraction(new_formula)
            self.expansion(new_formula)
        
        # check AGM postulates between old and new belief set, as well as sentence
        check_agm_revision_postulates(B_old, new_formula, self)
        return 
