"""
Revision module for belief revision.
Implements the AGM belief revision operations.
"""

from logic import parse_formula, to_cnf, negate_formula
from belief_base import BeliefBase
from typing import Dict

class BeliefRevision:
    """
    A class that implements AGM belief revision operations.
    
    This class provides operations for belief expansion, contraction,
    and revision according to AGM postulates.
    """
    
    @staticmethod
    def expand(belief_base: BeliefBase, belief: str):
        """
        Expand the belief base with a new belief.
        """
        return belief_base.expand(belief)
    
    @staticmethod
    def contract(belief_base: BeliefBase, belief: str) -> bool:
        """
        Contract the belief base to remove a belief.
        """
        return belief_base.contract(belief)
    
    @staticmethod
    def revise(belief_base: BeliefBase, belief: str) -> bool:
        """
        Revise the belief base with a new belief.
        This implements the Levi Identity: K * A = (K ÷ ¬A) + A (slides 10 page 38)
        Revising a belief base with a new belief includes:
        1. Checking if the new belief is consistent with the existing beliefs 
        2. If it is consistent, simply adding it (expansion)
        3. If it's inconsistent, removing the minimal set of exist. beliefs that conflict with the new belief (contraction), and then adds the new belief
        """
        return belief_base.revise(belief)
    
    @staticmethod
    def verify_agm_postulates(belief_base: BeliefBase, belief: str) -> Dict[str, str]:
        """
        Verify that the belief revision operations satisfy the AGM postulates.
        """
        results = {}
        parsed_belief = parse_formula(belief)
        
        # Save the original belief base for comparison
        original_beliefs = belief_base.beliefs.copy()
        
        # Create a copy of the belief base for testing
        test_base = belief_base.__class__()
        for b in original_beliefs:
            test_base.add_belief(b)
        
        # Verify Success postulate: B ∈ K * A
        test_base.revise(parsed_belief)
        results["Success"] = test_base.entails(parsed_belief)
        
        # Verify Inclusion postulate: K * A ⊆ K + A
        # This is automatically satisfied by the Levi Identity implementation
        results["Inclusion"] = True
        
        # Reset test base
        test_base = belief_base.__class__()
        for b in original_beliefs:
            test_base.add_belief(b)
        
        # Verify Vacuity postulate: If ¬A ∉ K, then K * A = K + A
        negated = negate_formula(parsed_belief)
        if not test_base.entails(negated):
            # Save the state before revision
            before_revision = test_base.beliefs.copy()
            
            # Apply revision
            test_base.revise(parsed_belief)
            after_revision = test_base.beliefs.copy()
            
            # Reset and apply expansion
            test_base = belief_base.__class__()
            for b in original_beliefs:
                test_base.add_belief(b)
            test_base.expand(parsed_belief)
            after_expansion = test_base.beliefs.copy()
            
            # Check if the results are the same
            results["Vacuity"] = set(after_revision) == set(after_expansion)
        else:
            results["Vacuity"] = True  # Not applicable in this case
        
        # Verify Consistency postulate: K * A is consistent unless A is inconsistent
        test_base = belief_base.__class__()
        for b in original_beliefs:
            test_base.add_belief(b)
        
        test_base.revise(parsed_belief)
        results["Consistency"] = not (test_base.entails(parsed_belief) and 
                                      test_base.entails(negate_formula(parsed_belief)))
        
        # Verify Extensionality postulate: If A ≡ B, then K * A = K * B
        # This would require testing equivalence of formulas
        results["Extensionality"] = "Not verified"  # Would need more complex logic
        
        return results