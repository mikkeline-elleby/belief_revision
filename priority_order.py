import itertools
import re

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

VARIABLE_REGEX = re.compile(r"and|or|not|imp|bi|([a-zA-Z])")

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
formula_str = "and(imp(or(a,d),c),b)"

satisfiable_count = entrenchment(formula_str)
print("Number of satisfiable formulas:", satisfiable_count)
