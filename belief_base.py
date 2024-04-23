from entailment import resolution  

class BeliefBase: 
    def __init__(self):
        self.formulas = set()

    def add_formula(self, formula, priority):
        self.formulas.add(formula)
        return self
    
    def revise(self, formula):
        ...

    def remove_formula(self, formula):
        if formula in self.formulas:
            self.formulas.remove(formula)

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
    
def entrenchment(B, belief):
    if belief.entrenchment is None:
        n_entrenchment = 1
        n_letters = belief.formula.atoms()
        for b in B.beliefs:
            b_letters = b.formula.atoms()
            if n_letters & b_letters:
                b.entrenchment = 0.9 * b.entrenchment
                if count_operator([belief.formula]) < count_operator([b.formula]):
                    b.entrenchment = 0.9 * b.entrenchment
                else:
                    n_entrenchment = 0.9 * n_entrenchment
    else:
        n_entrenchment = belief.entrenchment
    return n_entrenchment

def count_operator(clause, c=0):
    for sub in clause:
        if isinstance(sub, 'Or'):
            c = c + count_operator(sub.args, c+1) + len(sub.atoms()) - 1
        elif isinstance(sub, 'And'):
            c = c + count_operator(sub.args, c-1)
    return c
