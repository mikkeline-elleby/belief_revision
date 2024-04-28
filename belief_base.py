# belief_base.py

# importing python tools
import itertools
from itertools import combinations
import re
from copy import deepcopy, copy

# importing project components
from entailment import resolution
from formulas import *
from agm_postulates import check_agm_revision_postulates

VARIABLE_REGEX = re.compile(r"and|or|not|imp|bi|([a-zA-Z])")

def parenthesis_valid(variable):
    """check that we in fact have an opening and closing parenthesis to claim that this is a valid formula"""
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
    """parse the formulas"""
    parts = formula.split('(')
    operator = parts[0]
    variables = create_valid_formula(('('.join(parts[1:])).rstrip(')').split(','))
    return operator, variables


def evaluate_formula(formula, truth_assignment):
    """evaluate the fomula using the logic operators"""
    operator, variables = formula

    if variables == [''] or variables == []:
        try:
            return truth_assignment[operator]
        except KeyError:
            return False

    def evaluate(var):

        return truth_assignment[var] if var in truth_assignment else evaluate_formula(parse_formula(var), truth_assignment)

    try:
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
    except IndexError:
        return False


def find_variable(formula):
    """find the variables used in the belief base with the help of regex matching"""
    variables = []
    for match in VARIABLE_REGEX.findall(formula):
        if match is not None and match != "":
            variables.append(match)
    return variables


def entrenchment(formula_str):
    """count number of satisfiable formulas"""
    formula = parse_formula(formula_str)
    variables = find_variable(formula_str)

    #creates all the possible combination of true and false for the truth table by using the number of variables 
    truth_assignments = itertools.product([True, False], repeat=len(variables))

    #sum the number of satisfiable formulas 
    satisfiable_count = sum(evaluate_formula(formula, dict(zip(variables, assignment))) for assignment in truth_assignments)

    return satisfiable_count


def generate_subsets(input_set):
    """generate all the possible subsets of the belief base """
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

    def contraction(self, negated_alpha):
        """negated_alpha is removed from the belief base by contraction"""

        # special case if belief base only contains negated_alpha
        # then contracted belief base is empty
        if len(self.formulas) == 1:
            if next(iter(self.formulas)) == negated_alpha:
                self.formulas = set()
                return

        #create an array that will hold the valid sets 
        valid_set = []
        #generate all the possible subsets from our formulas 
        subset_of_set = generate_subsets(self.formulas)

        #fow each subset check if they are entailed by the alpha, if this is not the case add them to the valid set
        for sub_set in subset_of_set:
            new_sub_set = sub_set.split('|')
            if not resolution(new_sub_set, negated_alpha):
                valid_set.append(sub_set)

        #choose the valid set that has the highest entrenchment score 
        if len(valid_set) > 0:
            best_set = []
            best_score = 0

            for i in valid_set:
                if len(i)>1 :
                    i = i.split('|')

                score = 0
                for elem in i:
                    score += entrenchment(elem)

                if score >= best_score:
                    best_set = i
                    best_score = score

            self.formulas = set(best_set)
            return

    def revision(self, alpha):

        # first we check for entailment
        if resolution(self.formulas, alpha):
            print(f"The belief base already entails {alpha} -> nothing to revise")
            return

        # make copy of belief base for AGM checking
        B_old = BeliefBase()
        B_old.formulas = set(self.formulas)

        # revision following the levi identity
        negated_alpha = negation(alpha)
        self.contraction(negated_alpha)
        self.expansion(alpha)

        # check AGM postulates between old and new belief set, as well as alpha
        check_agm_revision_postulates(B_old, alpha, self)

        return

    def __eq__(self, other: object) -> bool:
        """Used for comparing belief base instances which is only belief set dependent"""
        return self.formulas == other.formulas

