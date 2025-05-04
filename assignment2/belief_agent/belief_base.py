"""
Belief Base module for belief revision.
Handles the storage and management of beliefs.
"""
from typing import List
from itertools import combinations
from logic import parse_formula, to_cnf, check_entailment, negate_formula, is_literal

class BeliefBase:
    """
    A class representing a belief base that can be revised.
    """
    
    def __init__(self):
        """Initialize an empty belief base."""
        self.beliefs = []  # list of beliefs in string form
        self.priorities = {}  # maps beliefs to priority values
        
    def add_belief(self, belief: str, display: bool = True) -> bool:
        """
        Add a belief to the belief base (expansion).
        """
        # parse and validate belief
        parsed_belief = parse_formula(belief)
        if parsed_belief is None:
            return False
        
        # add the belief if it's not already in the belief base
        if parsed_belief not in self.beliefs:
            self.beliefs.append(parsed_belief)
            
            # assign priority based on complexity of the formula
            priority = self._calculate_priority(parsed_belief)
            self.priorities[parsed_belief] = priority
            
            if display:
                print(f"Added belief: {parsed_belief} with priority {priority}")
                
            return True
        
        return False
    
    def expand(self, belief: str) -> bool:
        """
        Expand the belief base with a new belief.
        This is a simple addition without checking for consistency.
        """
        return self.add_belief(belief)
    
    def revise(self, belief: str, display: bool = True) -> None:
        """
        Revise the belief base with a new belief.
        This ensures the new belief is accepted while maintaining consistency.
        Check revision.py for a detailed explanation.
        """
        parsed_belief = parse_formula(belief)
        if parsed_belief is None:
            return False
        
        # if the belief is already entailed, no need to revise
        if self.entails(parsed_belief):
            if display:
                print(f"Belief '{parsed_belief}' is already entailed by the belief base - no need to revise.")
            return True
        
        # if the negation of the belief is entailed, contraction is needed
        if self.entails(negate_formula(parsed_belief)):
            if display:
                print(f"The negation of '{parsed_belief}' is entailed. Contraction needed.")
            self.contract(parsed_belief)
        
        # expand with the new belief
        return self.add_belief(parsed_belief)
    
    def contract(self, belief: str) -> bool:
        """
        Contract the belief base to remove a belief.
        Uses partial meet contraction based on priorities.
        """
        parsed_belief = parse_formula(belief)
        if parsed_belief is None:
            return False
        
        # If the belief is not entailed, no need to contract
        # example:
        # let's say we want to contract r, and r is not entailed by our belief base (e.g. we have just p => q),
        # then our belief base already doesn't believe r. There's nothing to remove or change.
        if not self.entails(parsed_belief):
            print(f"Belief '{parsed_belief}' is not entailed. No contraction needed.")
            return True
        
        # find remainders (maximal subsets that don't entail the belief)
        remainders = self._find_remainders(parsed_belief)
        
        if not remainders:
            print("Could not find valid remainders for contraction.")
            return False
        
        # select the remainder with the highest priority sum
        selected_remainder = self._select_remainder(remainders)
        
        # Update the belief base
        self.beliefs = selected_remainder
        
        # Clean up priorities for beliefs that are no longer in the base
        self._update_priorities()
        
        print(f"Contracted '{parsed_belief}'. New belief base size: {len(self.beliefs)}")
        return True
    
    def entails(self, belief: str) -> bool:
        """
        Check if the belief base entails a given belief.
        """
        # convert belief base to CNF
        kb_cnf = []
        for b in self.beliefs:
            kb_cnf.extend(to_cnf(b))
        
        # check entailment using resolution
        return check_entailment(kb_cnf, belief)
    
    def display(self):
        """Display the current belief base with priorities."""
        if not self.beliefs:
            print("Belief base is empty.")
            return
        
        print("\nCurrent Belief Base:")
        print("-" * 50)
        for belief in self.beliefs:
            priority = self.priorities.get(belief, "N/A")
            print(f"  {belief} (priority: {priority})")
        print("-" * 50)
    
    def _calculate_priority(self, belief: str) -> float:
        """
        Calculate priority value for a belief based on its complexity.
        Note: This is a simple heuristic and can be improved.
        """
        priority = 0.0

        if is_literal(belief):
            return priority
        
        # more complex formulas get higher priority, hence lower penalty value
        if "~" in belief:
            priority += 0.5
        if "&" in belief:
            priority += 1.0
        if "|" in belief:
            priority += 1.5
        if "=>" in belief:
            priority += 2.0
        if "<<>>" in belief:
            priority += 2.5
        
        return priority

    def _find_remainders(self, belief: str) -> List[List[str]]:
        """
        Find all maximal subsets of the belief base that don't entail the belief.
        """
        remainders = []
        
        # generate all possible subsets of the beliefs
        for i in range(len(self.beliefs), 0, -1):
            for subset in combinations(self.beliefs, i):
                subset_list = list(subset)
                
                # check if this subset entails the belief
                kb_cnf = []
                for b in subset_list:
                    kb_cnf.extend(to_cnf(b))
                
                if not check_entailment(kb_cnf, belief):
                    # this is a potential remainder
                    remainders.append(subset_list)
            
            # if we found remainders at this level, stop looking
            if remainders:
                break
            
        return remainders
    
    def _select_remainder(self, remainders: List[List[str]]) -> List[str]:
        """
        Select remainders based on priorities and take their intersection.
        Implements partial meet contraction.
        """
        if not remainders:
            return []

        print(f"Found {len(remainders)} potential remainders for contraction.")
        
        # calculate total priority for each remainder
        remainder_priorities = {}
        for i, remainder in enumerate(remainders):
            total_priority = sum(self.priorities.get(belief, 0) for belief in remainder)
            print(f"Remainder {i}: {remainder} has total priority {total_priority}")
            remainder_priorities[i] = total_priority
        
        # get the average priority - this is our selection function
        avg_priority = sum(remainder_priorities.values()) / len(remainder_priorities)
        
        # select all remainders with under-average priority
        selected_remainders = [remainders[i] for i, priority in remainder_priorities.items() 
                            if priority <= avg_priority]
        
        print(f"Selected {len(selected_remainders)} remainders for intersection")
        
        # in case where no remainders were selected, return the lowest priority one
        if not selected_remainders:
            selected_index = min(remainder_priorities, key=remainder_priorities.get)
            return remainders[selected_index]
        
        # take the intersection of all selected remainders
        if len(selected_remainders) == 1:
            return selected_remainders[0]
        
        # find beliefs that are in all selected remainders
        intersection = set(selected_remainders[0])
        for remainder in selected_remainders[1:]:
            intersection = intersection.intersection(set(remainder))
        
        return list(intersection)
    
    def _update_priorities(self) -> None:
        """
        Update the priorities dictionary to only contain current beliefs.
        """
        new_priorities = {}
        for belief in self.beliefs:
            if belief in self.priorities:
                new_priorities[belief] = self.priorities[belief]
            else:
                new_priorities[belief] = self._calculate_priority(belief)
        
        self.priorities = new_priorities
