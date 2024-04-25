# AGM postulates for revision
from entailment import resolution, matching_comma
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

    print("success postulate")
    if p in B_new.formulas:
        return "success"
    else:
        print(f"Success postule not valid for B * {p}")
        return "failure"


def inclusion_postulate(B_old, p, B_new):
    """B revised by p - is a subset of B expanded by p"""

    print("inclusion postulate")
    B_old.expansion(p)

    # check if all sentences of new belief set is present in previous belief set
    for x in B_new.formulas:
        if not (x in B_old.formulas):
            print(f"Inclusion Postulate not satisfied for B * {p}")
            return "failure"

    return "success"


def vacuity_postulate(B_old, p, B_new):
    """If not p is not in B, then B revised by p is equal to B expanded by p"""

    # determine if belief set entails not(p)
    if resolution(list(B_old.formulas), negation(p)):
        return "neutral"

    print("vacuity postulate")
    # if not(p) is not entailed then B_new == B + p
    B_old.expansion(p)

    if B_old == B_new:
        return "success"
    else:
        print(f"Vacuity Postulate not satisfied by B * {p}")
        return "failure"


def consistency_postulate(p, B_new):
    """B revised by p is consistent if p is consistent"""

    # check if belief p is consistent
    if check_consistency(p):
        print("consistency postulate")

        # new belief set must also be consistent
        if check_consistency(B_new.formulas):
            return "success"
        else:
            print(f"Consistency Postulate not satisfied by B * {p}")
            return "failure"

    # new belief is inconsistent
    return "neutral"


def extenstionality_postulate(B_old, p, B_new):
    """If p <-> q in Cn(Ø), then B * p == B * q"""
    
    success = False
    for formula in B_old.formulas:
        a, b = find_equivalence(p, formula)

        if (a != False and b!= False) and (p == a or p == b):
            print("extensionality postulate", a, b)
            q = a if b == p else b
            # B * q == B * p
            print("B_old:", B_old.formulas)
            print("B_new:", B_new.formulas)
            B_old.revision(negation(q))
            print("B_old revised:", B_old.formulas)
            if B_old == B_new:
                success = True
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

def check_consistency(belief_set):
    for x in belief_set:
        if resolution(list(belief_set), negation(x)):
            return False
    return True

def find_equivalence(p, formula):
    if formula[0:2] == "bi":
        if (p in formula):
            comma_index = matching_comma(formula)
            a = formula[3:comma_index]
            b = formula[comma_index+1:-1]
            return a,b
    return False, False

if __name__ == '__main__':
    ...
    print(find_equivalence("p", "bi(p,q)"))
    print(find_equivalence("w", "bi(p,q)"))
    print(find_equivalence("q", "bi(p,q)"))
    print(find_equivalence("p", "bi(p,and(q,w)"))
    print(find_equivalence("and(p,q)", "bi(and(p,q),or(s,t))"))