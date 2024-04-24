from belief_base import BeliefBase
from formulas import *
import copy

# script for testing
B = BeliefBase()

p = "p"
q = "q"
r = "r"
o = "o"

# Example complex formulas
formula = r 
formula6 = o
formula1 = p
formula2 = q
formula3 = implication(p, conjunction(q, r))  # p → (q ∧ r)
formula4 = disjunction(p,q)
formula5 = "not(q)"

print("Revision 1 ==== added p")
B.revision(formula1)
print("end formula:", B.formulas)

print("Revision 2 ==== added r")
B.revision(formula)
print("end formula:", B.formulas)

print("Revision 3 ==== added o")
B.revision(formula6)
print("end formula:", B.formulas)

print("Revision 4 ==== added q")
B.revision(formula2)
print(B.formulas)

print("Revision 5 ==== added or(p,q)")
B.revision(formula4)
print(B.formulas)

print("Revision 6 ==== added not(q)")
B.revision(formula5)
print(B.formulas)
