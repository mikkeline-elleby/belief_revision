from contract_belief_base import *
from entailment import *

def test_agm_postulates():
    belief_base = ['p', 'q']

    # Test Success Postulate
    contracted_base = contract_belief_base(belief_base, 'p')
    assert contracted_base == belief_base, "Success Postulate test failed"

    # Test Inclusion Postulate
    contracted_base = contract_belief_base(belief_base, 'r')
    assert all(formula in belief_base for formula in contracted_base), "Inclusion Postulate test failed"

    # Test Vacuity Postulate
    contracted_base = contract_belief_base(belief_base, 'r')
    assert contracted_base == belief_base, "Vacuity Postulate test failed"

    # Test Consistency
    assert all(resolution(belief_base, formula) for formula in belief_base), "Consistency test failed"

    # Test Extensionality
    belief_base2 = ['p ∧ q']
    contracted_base1 = contract_belief_base(belief_base, 'p')
    contracted_base2 = contract_belief_base(belief_base2, 'p')
    assert contracted_base1 == contracted_base2, "Extensionality test failed"

    print("All AGM postulate tests passed.")

# Example function calls
test_agm_postulates()