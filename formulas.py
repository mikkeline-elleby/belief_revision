# helper functions for formatting sentences correctly

def conjunction(p, q):
    """Conjunction: and(p,q)"""
    return f"and({p},{q})"

def disjunction(p, q):
    """Disjunction: or(p,q)"""
    return f"or({p},{q})"

def negation(p):
    """Negation: not(p)"""
    return f"not({p})"

def implication(p, q):
    """Implication: imp(p,q)"""
    return f"imp({p},{q})"

def equivalence(p, q):
    """Equivalence: bi(p,q)"""
    return f"bi({p},{q})"

if __name__ == '__main__':
    # Example propositional variables
    p = "p"
    q = "q"
    r = "r"
    # Example complex formulas
    formula1 = conjunction(p, q)
    formula2 = disjunction(p, negation(q))
    formula3 = implication(p, conjunction(q, r))
    print(f"Formula1: {formula1}, formula2: {formula2}, formula3: {formula3}")
