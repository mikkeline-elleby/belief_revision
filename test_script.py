from belief_base import BeliefBase
from formulas import *
from agm_postulates import check_agm_revision_postulates

import revision_operations as revise
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
# B.add_formula(formula1, 1)
# B.add_formula(formula2, 1)
# B.add_formula(formula3, 1)

print("Revision 1")
B = revise.belief_revision(B, formula1)
print("Revision 2")
B = revise.belief_revision(B, formula2)
print("Revision 3")
B = revise.belief_revision(B, formula3)

print(B.formulas)

formula4 = conjunction("a","b")
for x in B.formulas:
    print(x)

# B = revise.belief_revision(B, formula4)