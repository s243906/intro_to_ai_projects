"""
    Unit testing algorithm using AGM postulates.
"""
from revision import *
from belief_base import BeliefBase


# Init beleifs, belief bases, and revision module
revision = BeliefRevision()

belief = "~A|~B"
belief_base = BeliefBase()
belief_base.expand("A")
# belief_base.expand("~A")
belief_base.expand("A|B")
belief_base.expand("A=>B")


belief_2 = "~(A&B)"
belief_base_2 = BeliefBase()
belief_base_2.expand("A")
belief_base_2.expand("A|B")
belief_base_2.expand("A=>B")


# Verify AGM postulates
# 
results = revision.verify_agm_postulates(belief_base=belief_base, belief=belief, belief_base_2=belief_base_2, belief_2=belief_2)

print("---"*50)
print(results)

# print(belief_base.beliefs)
