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
    def contract(belief_base: BeliefBase, belief: str, display: bool = True) -> bool:
        """
        Contract the belief base to remove a belief.
        """
        return belief_base.contract(belief, display=display)
    
    @staticmethod
    def revise(belief_base: BeliefBase, belief: str, display: bool = True) -> bool:
        """
        Revise the belief base with a new belief.
        This implements the Levi Identity: K * A = (K ÷ ¬A) + A (slides 10 page 38)
        Revising a belief base with a new belief includes:
        1. Checking if the new belief is consistent with the existing beliefs 
        2. If it is consistent, simply adding it (expansion)
        3. If it's inconsistent, removing the minimal set of exist. beliefs that conflict with the new belief (contraction), and then adds the new belief
        """
        return belief_base.revise(belief, display=display)

    @staticmethod
    def are_logically_equivalent_bases(base1, base2):
        """Check if two belief bases are logically equivalent."""
        # Convert both bases to CNF
        cnf_base1 = []
        for belief in base1.beliefs:
            cnf_base1.extend(to_cnf(belief))
        
        cnf_base2 = []
        for belief in base2.beliefs:
            cnf_base2.extend(to_cnf(belief))
        
        # remove duplicates and sort
        cnf_base1 = list(set(tuple(sorted(clause)) for clause in cnf_base1))
        cnf_base2 = list(set(tuple(sorted(clause)) for clause in cnf_base2))
        
        # sorth the clauses themselves for consistent comparison
        cnf_base1.sort()
        cnf_base2.sort()
        
        return cnf_base1 == cnf_base2
    
    @staticmethod
    def verify_agm_postulates(belief_base, belief, belief_base_2=None, belief_2=None):
        """
        Verify that the belief revision operations satisfies the following AGM postulates:
        
        1. Success: φ ∈ B * φ
        2. Inclusion: B * φ ⊆ B + φ
        3. Vacuity: If ¬φ ∉ B, then B * φ = B + φ
        4. Consistency: B * φ is consistent if φ is consistent
        5. Extensionality: If (φ <<>> Ψ) ∈ Cn(∅), then B * φ = B * Ψ
        """
        results = {}

        parsed_belief = parse_formula(belief)

        original_beliefs = belief_base.beliefs.copy()
        
        # copy of the belief base for testing
        test_base = belief_base.__class__()
        for b in original_beliefs:
            test_base.add_belief(b, display=False)

        # 1. Verify Success postulate: φ ∈ B * φ
        # This checks if the belief is in the revised belief base
        # "New information should be accepted in the revised belief set."
        test_base.revise(parsed_belief, display=False)
        if belief in test_base.beliefs:
            results["1. Success"] = True
        else:
            results["1. Success"] = False

        # 2. Verify Inclusion postulate: B * φ ⊆ B + φ
        # "B revised with φ should be a subset of B expanded with φ."

        # create a base for revision and revise parsed belief
        revision_base = belief_base.__class__()
        for b in original_beliefs:
            revision_base.add_belief(b, display=False)
        revision_base.revise(parsed_belief, display=False)

        # create a base for expansion and expand with parsed belief
        expansion_base = belief_base.__class__()
        for b in original_beliefs:
            expansion_base.add_belief(b, display=False)
        expansion_base.expand(parsed_belief, display=False)

        # check if revised beliefs are a subset of expanded beliefs
        inclusion_check_passed = True
        for b in revision_base.beliefs:
            # if not expansion_base.entails(b):
            if b not in expansion_base.beliefs:
                inclusion_check_passed = False
                break

        results["2. Inclusion"] = inclusion_check_passed

        # 3. Verify Vacuity postulate: If ¬φ ∉ B, then B * φ = B + φ
        # "If the new belief doesn't contradict the existing beliefs, then revision should be the same as expansion."
        
        # reset test base and create a new revision base
        revision_base = belief_base.__class__()
        for b in original_beliefs:
            revision_base.add_belief(b, display=False)
        
        # check if negated formula is entailed by test base
        negated = negate_formula(parsed_belief)
        if negated not in revision_base.beliefs:
            # apply revision
            revision_base.revise(parsed_belief, display=False)
            after_revision = set(revision_base.beliefs)
            
            # reset and apply expansion
            expansion_base = belief_base.__class__()
            for b in original_beliefs:
                expansion_base.add_belief(b, display=False)
            expansion_base.expand(parsed_belief)
            after_expansion = set(expansion_base.beliefs)
            
            # check if the results are the same
            results["3. Vacuity"] = after_revision == after_expansion
        else:
            results["3. Vacuity"] = "N/A - ¬φ is in B"

        # 4. Verify Consistency postulate: B * φ is consistent if φ is consistent
        # first check if belief itself is consistent (not a contradiction) - a formula is inconsistent if it entails its own negation
        # "When the doctor learns ¬Flu, they must revise other beliefs to maintain consistency. They can't simultaneously believe Flu and ¬Flu."
        # "ensures that the revision operation maintains consistency in the belief base when the new belief itself is consistent."
        
        # belief_consistent = False

        # reset test base
        test_base = belief_base.__class__()
        for b in original_beliefs:
            test_base.add_belief(b, display=False)
        test_base.add_belief(parsed_belief, display=False)

        belief_consistent = test_base.entails(parsed_belief)
        
        results["4. Consistency"] = belief_consistent

        # 5. Verify Extensionality postulate: If (φ <<>> Ψ) ∈ Cn(∅), then B * φ = B * Ψ
        # this checks if the belief is equivalent to another belief in the base
        # "If two beliefs are equivalent, revising with one should be the same as revising with the other."
        if belief_2 and belief_base_2:
            
            # reset test base
            test_base = belief_base.__class__()
            for b in original_beliefs:
                test_base.add_belief(b, display=False)
            
            # Parse and copy belief base 2 for testing
            parsed_belief_2 = parse_formula(belief_2)

            original_beliefs_2 = belief_base_2.beliefs.copy()


            test_base_2 = belief_base_2.__class__()
            for b_2 in original_beliefs_2:
                test_base_2.add_belief(b_2, display=False)

            # Revise belief base with belief
            test_base.revise(parsed_belief, display=False)
            # Revise belief_base_2 with belief_2
            test_base_2.revise(parsed_belief_2, display=False)


            # If the resulting beliefs in both belief bases are the same, then extensionality is satisfied
            are_same = BeliefRevision.are_logically_equivalent_bases(test_base, test_base_2)
            if are_same:
                results["5. Extensionality"] = True
            else:
                print(parsed_belief)
                print(parsed_belief_2)
                print(test_base.beliefs)
                print(test_base_2.beliefs)
                results["5. Extensionality"] = False

        else:
            results["5. Extensionality"] = "N/A - no Ψ is provided"

        # print(test_base.beliefs)

        return results