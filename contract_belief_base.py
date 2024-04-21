# contract_belief_base.py

from belief_base import BeliefBase


def contract_belief_base(belief_base, priority_order, alpha):
    #Ensure the belief_base is an instance of BeliefBase
    if not isinstance(belief_base, BeliefBase):
        raise ValueError("belief_base must be an instance of BeliefBase")

#Create a dictionary from formula to its priority for faster access
priority_dict = {formula: i for i, formula in enumerate(priority_order)}

#Check if alpha is directly in the belief base
if alpha in belief_base.formulas:
    belief_base.remove(alpha)   #Directly remove alpha
    return belief_base.formulas


#Sort the belief base by priority, lower index in priority_order means higher priority 
sorted_formulas = sorted(belief_base.formulas, key=lambda x: priority_dict.get(x, len(priority_order)))

#Removing formulas from lowest to highest priority until alpha is no entailed
for formula in reversed(sorted_formulas):
    temp_belief_base = BeliefBase[:]
    temp_belief_base.formulas = {f: belief_base.formulas[f] for f in belief_base.formulas if f !=formula}

    #if not entails(temp_belief_base, alpha):
    #   return temp_belief_base

return belief_base.formulas  #Return the contracted belief base if contraction is necessary

