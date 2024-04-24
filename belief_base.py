# belief_base.py

# importing python tools
import itertools
from itertools import combinations
import re
from copy import deepcopy

# importing project components
from entailment import resolution
from formulas import *
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

def generate_subsets(input_set):
    all_subsets = []
    for subset_length in range(1, len(input_set) + 1):
        for subset in combinations(input_set, subset_length):
            all_subsets.append("|".join(subset))
    return all_subsets


##############################################################################################

#  CLASS BELIEF BASE

##############################################################################################

class BeliefBase:
    def __init__(self):
        self.formulas = set()

    def expansion(self, alpha):
        #add alpha to the belief base
        self.formulas.add(alpha)
        return

    def contraction(self, alpha):
        #alpha is removed from the belief base.

        valid_set = []
        subset_of_set = generate_subsets(self.formulas)
        #print("sub set +++",subset_of_set)

        for sub_set in subset_of_set:
            # print("sub set +++",sub_set)
            new_sub_set = sub_set.split('|')
            if not resolution(new_sub_set, alpha):
                #print(alpha, "does not entail",sub_set)
                valid_set.append(sub_set)
                #print("updated valid set: ",valid_set)

        if len(valid_set) > 0:
            best_set = []
            best_score = 0

            for i in valid_set:
                if len(i)>1 : 
                    i = i.split('|')

                score = 0 
                for elem in i:
                    #print(elem) 
                    #print(score)
                    score += entrenchment(elem)
                    #print(score)
                #print(i, " has a score of ", score )
                if score >= best_score:
                    best_set = i
                    best_score = score
                    #print("score ", score, "best score", best_score)

            #print("best set:", best_set, "best set type:", type(best_set))
            self.formulas = set(best_set)
            #print(self.formulas)
            return 

    def revision(self, alpha):
        # make copy of belief base for AGM checking
        B_old = deepcopy(self)

        #levi identity
        negated_alpha = "not(" + alpha + ")"
        self.contraction(negated_alpha)
        self.expansion(alpha)


        # check AGM postulates between old and new belief set, as well as sentence
        check_agm_revision_postulates(B_old, alpha, self)

        return

    def __eq__(self, value: object) -> bool:
        """Used for comparing belief base instances only based on belief set"""
        return self.formulas == value.formulas
