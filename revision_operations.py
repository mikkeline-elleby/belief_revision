# revision_operations.py
from entailment import resolution
from agm_postulates import check_agm_revision_postulates
from copy import deepcopy
import contract_belief_base as contract

def contract_belief_base(belief_base, priority_order, new_formula):
    # Implement contraction logic here
    return contract.contract_belief_base(belief_base, priority_order, new_formula)


def _expand_belief_base(belief_base, new_formula):
    # expansion can only be done if resolution is consistent
    belief_base.add_formula(new_formula, 1)
    return belief_base


def belief_revision(belief_base, new_formula):
    if len(belief_base.formulas) == 0:
        new_belief_base = _expand_belief_base(belief_base, new_formula)
    
    # make copy of belief base for AGM checking
    B_old = deepcopy(belief_base)
    new_belief_base = None

    # check resolution to determine if revision is needed
    if resolution(list(belief_base.formulas), new_formula):
        return belief_base
    else:
        new_belief_base = contract_belief_base(belief_base, 1, new_formula)
        _expand_belief_base(new_belief_base, new_formula)

    # check AGM postulates between old and new belief set, as well as sentence
    check_agm_revision_postulates(B_old, new_formula, new_belief_base)

    return new_belief_base
