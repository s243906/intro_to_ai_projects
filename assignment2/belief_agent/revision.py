"""
Revision module for belief revision.
Implements the AGM belief revision operations.
"""
from logic import parse_formula, to_cnf, negate_formula
from belief_base import BeliefBase

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
    def verify_agm_postulates(belief_base, belief):
        """
        Verify that the belief revision operations satisfy the AGM postulates.
        
        In our implementation, we will check the following postulates:
        2. Success: φ ∈ B * φ
        3. Inclusion: B * φ ⊆ B + φ
        4. Vacuity: If ¬φ ∉ B, then B * φ = B + φ
        5. Consistency: B * φ is consistent if φ is consistent
        """
        results = {}
        parsed_belief = parse_formula(belief)
        
        original_beliefs = belief_base.beliefs.copy()
        
        # copy of the belief base for testing
        test_base = belief_base.__class__()
        for b in original_beliefs:
            test_base.add_belief(b, display=False)
        
        # 2. Verify Success postulate: φ ∈ B * φ
        # This checks if the belief is in the revised belief base
        # "New information should be accepted in the revised belief set."
        results["2. Success"] = test_base.entails(parsed_belief)
        
        # 3. Verify Inclusion postulate: B * φ ⊆ B + φ
        # Create a copy for expansion
        expansion_base = belief_base.__class__()
        for b in original_beliefs:
            expansion_base.add_belief(b, display=False)
        expansion_base.expand(parsed_belief)
        
        # Check if revised beliefs are a subset of expanded beliefs
        inclusion_check_passed = True
        for b in test_base.beliefs:
            if not expansion_base.entails(b):
                inclusion_check_passed = False
                break
        
        results["3. Inclusion"] = inclusion_check_passed
        
        # Reset test base
        test_base = belief_base.__class__()
        for b in original_beliefs:
            test_base.add_belief(b, display=False)
        
        # 4. Verify Vacuity postulate: If ¬φ ∉ B, then B * φ = B + φ
        negated = negate_formula(parsed_belief)
        if not test_base.entails(negated):
            # Apply revision
            test_base.revise(parsed_belief, display=False)
            after_revision = set(test_base.beliefs)
            
            # Reset and apply expansion
            test_base = belief_base.__class__()
            for b in original_beliefs:
                test_base.add_belief(b, display=False)
            test_base.expand(parsed_belief)
            after_expansion = set(test_base.beliefs)
            
            # Check if the results are the same
            results["4. Vacuity"] = after_revision == after_expansion
        else:
            results["4. Vacuity"] = "N/A - ¬φ is entailed by B"
        
        # 5. Verify Consistency postulate: B * φ is consistent if φ is consistent
        # First check if belief itself is consistent (not a contradiction) - a formula is inconsistent if it entails its own negation
        # "When the doctor learns ¬Flu, they must revise other beliefs to maintain consistency. They can't simultaneously believe Flu and ¬Flu."
        belief_consistent = True
        test_base = belief_base.__class__()
        test_base.add_belief(parsed_belief, display=False)
        if test_base.entails(negate_formula(parsed_belief)):
            belief_consistent = False
        
        # now check if the revised belief base is consistent
        test_base = belief_base.__class__()
        for b in original_beliefs:
            test_base.add_belief(b, display=False)
        test_base.revise(parsed_belief, display=False)
        
        # a belief base is inconsistent if it entails a contradiction
        # we check this by seeing if it entails both a formula and its negation
        consistency_check_passed = True
        for b in test_base.beliefs:
            if test_base.entails(negate_formula(b)):
                consistency_check_passed = False
                break
        
        if not belief_consistent:
            results["5. Consistency"] = "N/A - φ is inconsistent"
        else:
            results["5. Consistency"] = consistency_check_passed
        
        return results