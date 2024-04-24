from belief_base import *
from formulas import *
import copy

# script for testing
B = BeliefBase()

p = "p"
q = "q"
r = "r"
s = "s"

print("############ \nBASE CASE \n############")
formula1 = p
print(f"Revision 1: B * {formula1}")
B.revision(formula1)
print(f"Belief base after 1. revision: {B.formulas} \n")

formula2 = q
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