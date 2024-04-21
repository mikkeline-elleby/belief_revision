# contract_belief_base.py

from belief_base import BeliefBase


def contract_belief_base(BeliefBase, priority_order, alpha):

#Create a dictionary from formula to its priority for faster access
priority_dict = {formula: i for i, formula in enumerate(priority_order)}

#Check if alpha is directly in the belief base
if alpha in BeliefBase:
    BeliefBase.remove(alpha)   #Directly remove alpha
    return BeliefBase


#Sort the belief base by priority, lower index in priority_order means higher priority 
BeliefBase.sort(key=lambda x: priority_dict.get(x, len(priority_order)))

#Removing formulas from lowest to highest priority until alpha is no entailed
for formula in reversed(BeliefBase):
    temp_belief_base = BeliefBase[:]
    temp_belief_base.remove(formula)

    #if not entails(temp_belief_base, alpha):
    #   return temp_belief_base

return BeliefBase  #Return the contracted belief base if contraction is necessary

