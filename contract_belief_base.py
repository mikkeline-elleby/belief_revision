# contract_belief_base.py

from belief_base import BeliefBase
from entailment import resolution
from copy import deepcopy

def contract_belief_base(belief_base, priority_order, alpha):
    #Ensure the belief_base is an instance of BeliefBase
    if not isinstance(belief_base, BeliefBase):
        raise ValueError("belief_base must be an instance of BeliefBase")

    #Copy the original formula to avoid modifying the original belief base directly 
    formulas_set = deepcopy(belief_base.formulas)

    #Check if alpha is directly in the belief base
    if alpha in formulas_set:
        belief_base.remove_formula(alpha)   #Directly remove alpha
        return deepcopy(formulas_set)      #Return a deepcopy of the modified belief base formulas as a set. 


    #Convert priority_order to a list of formulas sorted by external priority indications
    sorted_formulas = sorted(formulas_set, key=lambda x: priority_order.index(x) if x in priority_order else len(priority_order))

    #Removing formulas from lowest to highest priority until alpha is no entailed
    for formula in reversed(sorted_formulas):
        temp_belief_base = BeliefBase()    #Creating a new temporary BeliefBase instance
        temp_belief_base.formulas = {f: formulas_set[f] for f in formulas_set if f !=formula}

    
    #Simulate the resolution function to check if the base still intails alpha
    if not resolution(list(temp_belief_base.formulas.keys()), alpha):
        return set(temp_belief_base.formulas.keys())    #Return modified formulas as a set

    #new_belief_base = BeliefBase()
    #new_belief_base.formulas = formulas_set
    
    ## Return the original belief base if contraction is not possible (unchanged as contraction was not successful)
    return set(belief_base.formulas.keys()) 
