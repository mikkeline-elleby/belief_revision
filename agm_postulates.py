# AGM postulates for revision

from formulas import *
from copy import deepcopy

def check_agm_revision_postulates(old_belief_set, belief, belief_set):
    """Checking AGM revision postulates for a given p set and p """

    result = list()

    # make copies of input to ensure not changing the belief set
    B_old = deepcopy(old_belief_set)
    p = deepcopy(belief)
    B_new = deepcopy(belief_set)

    # testing all five postulates
    result.append(success_postulate(p, B_new))
    result.append(inclusion_postulate(B_old, p, B_new))
    result.append(vacuity_postulate(B_old, p, B_new))
    result.append(consistency_postulate(p, B_new))
    result.append(extenstionality_postulate(B_old, p, B_new))

    # determine the successes
    success = result.count("success")
    failure = result.count("failure")

    print(f"Success-rate: {success}/{success+failure} = {success/(success+failure)}")


def success_postulate(p, B_new):
    """p is included in the set of B revised by p"""

    if p in B_new.formulas:
        return "success"
    else:
        print(f"Success postule not valid for B * {p}")
        return "failure"


def inclusion_postulate(B_old, p, B_new):
    """B revised by p - is a subset of B expanded by p"""

    B_old.expansion(p)

    # check if all sentences of new belief set is present in previous belief set
    for x in B_new.formulas:
        if not (x in B_old.formulas):
            print(f"Inclusion Postulate not satisfied for B * {p}")
            return "failure"

    return "success"


def vacuity_postulate(B_old, p, B_new):
    """If not p is not in B, then B revised by p is equal to B expanded by p"""

    # determine if not p is present in Belief Set B
    for x in B_old.formulas:
        if negation(p) in x:
            return "neutral"

    # if not p not present B_new == B + p
    B_old.expansion(p)
    print("B_old:", B_old.formulas)
    print("B_new:", B_new.formulas)
    if B_old == B_new:
        return "success"
    else:
        print(f"Vacuity Postulate not satisfied by B * {p}")
        return "failure"


def consistency_postulate(p, B_new):
    """B revised by p is consistent if p is consistent"""
    # check if belief p is consistent

    if check_consistency({""}, p):

        # check is new belief set is consistent
        if check_consistency(B_new.formulas, "") == "consistent":
            return "success"
        else:
            print(f"Consistency Postulate not satisfied by B * {p}")
            return "failure"

    # new belief in inconsistent
    return "neutral"


def extenstionality_postulate(B_old, p, B_new):
    """If p <-> q in Cn(Ø), then B * p == B * q"""
    success = False

    for formula in B_old.formulas:
        a, b = find_equivalence(p, formula)

        if (a != False and b!= False and (a == p or b == p)):
            # B * q == B * p
            B_old.revise(q)
            if B_old == B_new:
                return success == True
            else:
                print(f"Extensionality Postulate not satisfied by B * {p}")
                return "failure"

    if success:
        return "success"
    else:
        return "neutral"

###################################
# AGM Postulates helper functions #
###################################

def check_consistency(B, p):
    ...

def find_equivalence(p, formula):
    if formula[0:2] == "bi":
        if (p in formula):
            formula_stripped = formula.replace("bi", "").strip("()")
            a, b = formula_stripped.split(",", 1)

            return a,b
    return False, False

if __name__ == '__main__':
    ...
    # print(find_equivalence("p", "bi(p,q)"))
    # print(find_equivalence("w", "bi(p,q)"))
    # print(find_equivalence("q", "bi(p,q)"))
    # print(find_equivalence("p", "bi(p,and(q,w)"))