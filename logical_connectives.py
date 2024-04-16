# logical_connectives.py

def conjunction(p, q):
    return p and q

def disjunction(p, q):
    return p or q

def negation(p):
    return not p

def implication(p, q):
    return (not p) or q

def equivalence(p, q):
    return p == q

def exclusive(p, q):
    return (p or q) and not (p and q)

def nor(p, q):
    return not (p or q)

def nand(p, q):
    return not (p and q)