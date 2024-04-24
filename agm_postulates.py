# AGM postulates for revision

from formulas import *
from belief_base import *
from copy import deepcopy

def check_agm_revision_postulates(belief_set, belief, new_belief_set):
    """Checking AGM revision postulates for a given p set and p """

    result = list()

    # make copies of input to ensure not changing the belief set
    B = deepcopy(belief_set)
    p = deepcopy(belief)
    B_new = deepcopy(new_belief_set)

    # testing all five postulates
    result.append(success_postulate(p, B_new))
    result.append(inclusion_postulate(B, p, B_new))
    result.append(vacuity_postulate(B, p, B_new))
    #Sresult.append(consistency_postulate(p, B_new))
    result.append(extenstionality_postulate(B, p, B_new))

    # determine the successes
    success = result.count("success")
    failure = result.count("failure")

    print("Success-rate: ", success/(success+failure))


def success_postulate(p, B_new):
    """p is included in the set of B revised by p"""

    if p in B_new.formulas:
        return "success"
    else:
        print(f"Success postule not valid for B * {p}")
        return "failure"


def inclusion_postulate(B, p, B_new):
    """B revised by p - is a subset of B expanded by p"""

    B.expansion(p)

    # check if all sentences of new belief set is present in previous belief set
    for x in B_new.formulas:
        if not (x in B.formulas):
            print(f"Inclusion Postulate not satisfied for B * {p}")
            return "failure"
    return "success"

    # does not check for tight bound?


def vacuity_postulate(B, p, B_new):
    """If not p is not in B, then B revised by p is equal to B expanded by p"""
    
    # determine if not p is present in Belief Set B
    for x in B.formulas:
        if negation(p) in x:
            return "neutral"

    # if not p not present B_new == B + p
    B.expansion(p)
    if B == B_new:
        return "success"
    else:
        print(f"Vacuity Postulate not satisfied by B * {p}")
        return "failure"

'''
TODO : NOT FULLY IMPLEMENTED 
def consistency_postulate(p, B_new):
    """B revised by p is consistent if p is consistent"""
    # check is belief p is consistent
    if check_consistency(BeliefBase(), p):
        # check is new belief set is consistent
        if check_consistency(B_new, "") == "consistent":
            return "success"
        else:
            print(f"Consistency Postulate not satisfied by B * {p}")
            return "failure"
    
    # new belief in inconsistent
    return "neutral"
'''

def extenstionality_postulate(B, p, B_new):
    """If p <-> q in Cn(Ø), then B * p == B * q"""
    success = False
    for x in B.formulas:
        a, b = find_equivalence(p, x)
        if (a != False and b!= False and (a == p or b == p)):
            # B * q == B * p
            B.revise(q)
            if B == B_new:
                return success == True
            else:
                print(f"Extensionality Postulate not satisfied by B * {p}")
                return "failure"
    
    if success:
        return "success"
    else:
        return "neutral"

def check_consistency(B, p):
    ...

def find_equivalence(p, q):
    if ("bi" in q) and (p in q):
        q_stripped = q.replace("bi", "").strip("()")
        print(q_stripped)
        a, b = q_stripped.split(",")
        print(a,b)
        return a,b
    return False, False