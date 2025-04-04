"""
    A module that implements a belief base and the functions to manipulate it.
"""
class BeliefBase:
    """ Belief Base class to store and manage beliefs. """
    def __init__(self):
        """ Initialize the belief base with an empty list of beliefs. """
        self.beliefs = []

        # define valid beliefs with their description
        # note: values() are only for documentation purposes
        self.valid_beliefs = {
            "&" : "logical AND",
            "|" : "logical OR",
            "~": "logical not (negation)",
            ">>" : "logical implication",
            "<<>>": "logical biconditional (if and only if)"
        }
    
    def add_belief(self, belief: str) -> None:
        """ Add a belief to the belief base. """
        belief = self.parse_belief(belief)

        self.beliefs.append(belief)
        # TODO: add order, possibly unparsed
    
    def parse_belief(self, belief: str) -> str:
        """ Verify and parse the belief string. """
        # check 1: if belief is empty
        if not belief:
            raise ValueError("Belief cannot be empty.")

        # check 2: if belief contains only one character
        if belief.isalpha() and len(belief) == 1:
            return belief
        
        # check 3: if belief contains only valid characters
        valid_chars = set(self.valid_beliefs.keys())
        for char in belief:
            if char not in valid_chars and not char.isalpha():
                raise ValueError(f"Invalid character '{char}' in belief.")
        
        # check 4: if biconditional: TODO: maybe there's a better way to handle this
        if "<<>>" in belief:
            parts = belief.split("<<>>")

            if len(parts) != 2:
                print(f"Complex biconditional chains not supported: {belief}")
                raise ValueError("Invalid biconditional format.")
                
            # create a conjunction: (A >> B) & (B >> A): TODO: verify that
            return "(" + parts[0] + ">>" + parts[1] + ") & (" + parts[1] + ">>" + parts[0] + ")"
    
        # Return other valid formulas unchanged
        return belief