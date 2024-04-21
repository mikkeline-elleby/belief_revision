# revision_operations.py
from entailment import resolution
from agm_postulates import check_agm_revision_postulates
from copy import deepcopy

def contract_belief_base(belief_base, priority_order):
    # Implement contraction logic here
    pass

def _expand_belief_base(belief_base, new_formula):
    # expansion can only be done if resolution is consistent
    belief_base.add_formula(new_formula)


def belief_revision(belief_base, new_formula):
    # make copy of belief base for AGM checking
    B_old = deepcopy(belief_base)

    # check resolution to determine if revision is needed
    if not resolution(belief_base, new_formula):
        contract_belief_base(belief_base, new_formula)
        _expand_belief_base(belief_base, new_formula)

        # check AGM postulates between old and new belief set, as well as sentence
        check_agm_revision_postulates(B_old, new_formula, belief_base)
