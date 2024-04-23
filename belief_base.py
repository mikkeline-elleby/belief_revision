# belief_base.py

from entailment import resolution  

class BeliefBase: 
    def __init__(self):
        self.formulas = {}  #Change to dictionary to store formulas with priority

    def add_formula(self, formula, priority):
        self.formulas[formula] = priority
        return self

    def remove_formula(self, formula):
        if formula in self.formulas:
            del self.formulas[formula]

    def contract_formula(self, alpha):
        #Check if alpha is directly in the belief base
        if alpha in self.formulas: 
            self.remove_formula(alpha)
            return True
        
    #Check if the belief base entails alpha using the resolution method
        if resolution(list(self.formulas.keys()), alpha):
        
        #Removing the least important formulas to stop entailment of alpha 
            sorted_formulas = sorted(self.formulas.items(), key=lambda item: item[1])   #Sort by prioritry, lowest first
            for formula, _ in sorted_formulas:
            
                #Temporarily remove the formula
                temp_priority = self.formulas.pop(formula)
           
                #Check if alpha is still entailed without this formula
                if not resolution(list(self.formulas.keys()), alpha):
                    return True     #Successful contraction withpout this formula 
            
                #Restore the formula if contraction is not successful
                self.formulas[formula] = temp_priority

        return False    #Return False if contraction was not possible

    def query_formula(self, formula):
        return formula in self.formulas
    
