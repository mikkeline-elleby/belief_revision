from contract_belief_base import *
from entailment import *

def test_agm_postulates():


    # Test Success Postulate
    contracted_base = contract(B, 'p')
    assert contracted_base == B.formulas, "Success Postulate test failed"

    # Test Inclusion Postulate
    contracted_base = contract(B, 'r')
    assert all(formula in B for formula in contracted_base), "Inclusion Postulate test failed"

    # Test Vacuity Postulate
    contracted_base = contract(B, 'r')
    assert contracted_base == B, "Vacuity Postulate test failed"

    # Test Consistency
    assert all(resolution(B, formula) for formula in B), "Consistency test failed"

    # Test Extensionality
    
    contracted_base1 = contract(B, 'p')
    contracted_base2 = contract(B2, 'p')
    assert contracted_base1 == contracted_base2, "Extensionality test failed"

    print("All AGM postulate tests passed.")

B = BeliefBase()
B2 = BeliefBase()

B.add_formula('p')
B.add_formula('q')

B2.add_formula('and(p,q)')


# Example function calls
test_agm_postulates()
