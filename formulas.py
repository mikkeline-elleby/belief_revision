# Example propositional variables
p = "p"
q = "q"
r = "r"



def conjunction(p, q):
    return f"({p} ∧ {q})"

def disjunction(p, q):
    return f"({p} ∨ {q})"

def negation(p):
    return f"¬{p}"

def implication(p, q):
    return f"({p} → {q})"

def equivalence(p, q):
    return f"({p} ↔ {q})"



# Example complex formulas
formula1 = conjunction(p, q)  # p ∧ q
formula2 = disjunction(p, negation(q))  # p ∨ ¬q
formula3 = implication(p, conjunction(q, r))  # p → (q ∧ r)

