# contract_belief_base.py

def contract_belief_base(belief_base, priority_order, alpha):

#Create a dictionary from formula to its priority for faster access
priority_dict = {formula: i for i, formula in enumerate(priority_order)}

#Check if alpha is directly in the belief base
if alpha in belief_base:
    belief_base.remove(alpha)   #Directly remove alpha
    return belief_base


#Sort the belief base by priority, lower index in priority_order means higher priority 
belief_base.sort(key=lambda x: priority_dict.get(x, len(priority_order)))

#Removing formulas from lowest to highest priority until alpha is no entailed
for formula in reversed(belief_base):
    temp_belief_base = belief_base[:]
    temp_belief_base.remove(formula)

    #if not entails(temp_belief_base, alpha):
    #   return temp_belief_base

return belief_base  #Return the contracted belief base if contraction is necessary

