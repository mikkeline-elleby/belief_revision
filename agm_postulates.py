# AGM postulates for revision
from entailment import resolution, matching_comma
from formulas import *
from copy import deepcopy, copy

def check_agm_revision_postulates(old_belief_base, belief, belief_base):
    """Checking AGM revision postulates for a given p set and p """

    result = list()

    # make copies of input to ensure not changing the belief base
    B_old = copy(old_belief_base)
    alpha = copy(belief)
    B_new = copy(belief_base)
    B_new.formulas = copy(belief_base.formulas)

    # testing all five postulates
    result.append(success_postulate(alpha, B_new))
    result.append(inclusion_postulate(B_old, alpha, B_new))
    result.append(vacuity_postulate(B_old, alpha, B_new))
    result.append(consistency_postulate(alpha, B_new))
    result.append(extenstionality_postulate(B_old, alpha, B_new))

    # determine the successes
    success = result.count("success")
    failure = result.count("failure")

    print(f"AGM Postulate Success-rate: {success}/{success+failure} = {success/(success+failure)}")


def success_postulate(alpha, B_new):
    """alpha is included in the set of B revised by alpha"""

    if alpha in B_new.formulas:
        return "success"
    else:
        print(f"Success postule not valid for B * {alpha}")
        return "failure"


def inclusion_postulate(belief_old, alpha, B_new):
    """B revised by alpha - is a subset of B expanded by alpha"""

    B_old = copy(belief_old)
    B_old.formulas = copy(belief_old.formulas)
    B_old.expansion(alpha)

    # check if all sentences of new belief base is present in previous belief base
    for x in B_new.formulas:
        if not (x in B_old.formulas):
            print(f"Inclusion Postulate not satisfied for B * {alpha}")
            return "failure"

    return "success"


def vacuity_postulate(belief_old, alpha, B_new):
    """If not alpha is not in B, then B revised by alpha is equal to B expanded by alpha"""

    B_old = copy(belief_old)
    B_old.formulas = copy(belief_old.formulas)

    # determine if belief base entails not(alpha)
    if resolution(list(B_old.formulas), negation(alpha)):
        return "neutral"

    # if not(alpha) is not entailed then B_new == B + alpha
    B_old.expansion(alpha)

    if B_old == B_new:
        return "success"
    else:
        print(f"Vacuity Postulate not satisfied by B * {alpha}")
        return "failure"


def consistency_postulate(alpha, B_new):
    """B revised by alpha is consistent if alpha is consistent"""

    # check if belief alpha is consistent
    if check_consistency(alpha):

        # new belief base must also be consistent
        if check_consistency(B_new.formulas):
            return "success"
        else:
            print(f"Consistency Postulate not satisfied by B * {alpha}")
            return "failure"

    # new belief is inconsistent
    return "neutral"


def extenstionality_postulate(belief_old, alpha, B_new):
    """If alpha <-> q in Cn(Ø), then B * alpha == B * q"""

    B_old = copy(belief_old)
    B_old.formulas = copy(belief_old.formulas)

    success = False
    for formula in B_old.formulas:
        phi = find_equivalence(alpha, formula)

        if phi != False:
            B_old.contraction(negation(phi))
            B_old.expansion(phi)

            if B_old == B_new: # B * phi == B * alpha
                success = True
            elif B_old.formulas.difference(B_new.formulas) == {phi} and B_new.formulas.difference(B_old.formulas) == {alpha}:
                success = True
            else:
                print(f"Extensionality Postulate not satisfied by B * {alpha}")
                return "failure"

    if success:
        return "success"
    else:
        return "neutral"

###################################
# AGM Postulates helper functions #
###################################

def check_consistency(belief_base):
    for x in belief_base:
        if resolution(list(belief_base), negation(x)):
            return False
    return True

def find_equivalence(alpha, formula):
    if formula[0:2] == "bi":
        if (alpha in formula):
            comma_index = matching_comma(formula)
            a = formula[3:comma_index]
            b = formula[comma_index+1:-1]

            if (alpha == a or alpha == b):
                phi = a if b == alpha else b
                return phi
    
    return False

if __name__ == '__main__':
    print(find_equivalence("p", "bi(p,q)"))
