from belief_base import BeliefBase
from formulas import *
from agm_postulates import check_agm_revision_postulates

import copy

# script for testing
B = BeliefBase()

p = "p"
q = "q"
r = "r"

# Example complex formulas
formula1 = p
formula2 = q
formula3 = implication(p, conjunction(q, r))  # p → (q ∧ r)

print("Revision 1")
B.revision(formula1)

print("Revision 2")
B.revision(formula2)

print("Revision 3")
B.revision(formula3)


formula4 = conjunction("a","b")
for x in B.formulas:
    print(x)

# B = revise.belief_revision(B, formula4)