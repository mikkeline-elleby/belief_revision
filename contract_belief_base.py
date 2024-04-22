# contract_belief_base.py

from belief_base import BeliefBase


def contract_belief_base(belief_base, priority_order, alpha):
    #Ensure the belief_base is an instance of BeliefBase
    if not isinstance(belief_base, BeliefBase):
        raise ValueError("belief_base must be an instance of BeliefBase")

    #Create a set from formulas
    formulas_set = set(belief_base.formulas.keys())

    #Check if alpha is directly in the belief base
    if alpha in formulas_set:
        belief_base.remove_formula(alpha)   #Directly remove alpha
        return formulas_set


    #Convert priority_order to a list of formulas sorted by external priority indications
    sorted_formulas = sorted(formulas_set, key=lambda x: priority_order.index(x) if x in priority_order else len(priority_order))

    #Removing formulas from lowest to highest priority until alpha is no entailed
    for formula in reversed(sorted_formulas):
        temp_belief_base = BeliefBase()    #Creating a new temporary BeliefBase instance
        temp_belief_base.formulas = {f: belief_base.formulas[f] for f in belief_base.formulas if f !=formula}

    
    #Simulate the entails function to check if the base still intails alpha
    if not entails(temp_belief_base, alpha):
        return set(temp_belief_base.formulas.keys())    #Return modified formulas as a set

    return formulas_set  #Return the contracted belief base if contraction is necessary

