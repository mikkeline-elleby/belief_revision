from belief_base import *
from formulas import *
import copy

# script for testing
B = BeliefBase()

p = "p"
q = "q"
r = "r"
s = "s"

print("############ \nSECOND CASE\n############")
formula1 = p
print(f"Revision 1: B * {formula1}")
B.revision(formula1)
print(f"Belief base after 1. revision: {B.formulas} \n")

formula2 = equivalence(s,q)
print(f"Revision 2: B * {formula2}")
B.revision(formula2)
print(f"Belief base after 2. revision: {B.formulas} \n")

formula3 = negation(p)
print(f"Revision 3: B * {formula3}")
B.revision(formula3)
print(f"Belief base after 3. revision: {B.formulas} \n")

formula4 = negation(q)
print(f"Revision 4: B * {formula4}")
B.revision(formula4)
print(f"Belief base after 4. revision: {B.formulas} \n")

formula5 = s
print(f"Revision 5: B * {formula5}")
B.revision(formula5)
print(f"Belief base after 5. revision: {B.formulas} \n")

formula6 = r
print(f"Revision 6: B * {formula6}")
B.revision(formula6)
print(f"Belief base after 6. revision: {B.formulas} \n")

formula7 = negation(disjunction(p,q))
print(f"Revision 7: B * {formula7}")
B.revision(formula7)
print(f"Belief base after 7. revision: {B.formulas} \n")

formula8 = equivalence(q,s)
print(f"Revision 8: B * {formula8}")
B.revision(formula8)
print(f"Belief base after 8. revision: {B.formulas} \n")

formula9 = negation(s)
print(f"Revision 9: B * {formula9}")
B.revision(formula9)
print(f"Belief base after 9. revision: {B.formulas} \n")

