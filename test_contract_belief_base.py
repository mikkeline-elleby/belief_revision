#Test af contract_belief_base - lige pt fungere ikke helt...

import unittest
from contract_belief_base import contract_belief_base
from belief_base import BeliefBase

class ContractBeliefBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.belief_base = BeliefBase(...)      #Initialize BeliefBase (dummy data)
        self.priority_order = [...]         #Define priority order
        self.alpha = ...                #Define the belief which should contract..


    def test_contract_direct_belief(self):
        """Test that alpha is removed when it is drectly in the belief base."""
        contracted_base = contract_belief_base(self.belief_base, self.priority_order, self.alpha)
        self.assertNotIn(self.alpha, contracted_base)

    
    def test_contract_keeps_other_beliefs(self):
        """Test that other beliefs are not removed unnecessarily."""
        contracted_base = contract_belief_base(self.belief_base, self.priority_order, self.alpha)
        #Make sure some other belief that should remain is still in the contracted_base
        self.assertIn('some_other_belied', contracted_base)

if __name__ == '__main__':
    unittest.main()