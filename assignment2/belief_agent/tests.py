"""
    Unit testing algorithm using AGM postulates.
"""
from revision import *
from belief_base import BeliefBase


# Init beleifs, belief bases, and revision module
print("\nAGM POSTULATES UNIT TESTING")
print("---"*50)
print("test 1:")
revision = BeliefRevision()

belief = "~A|~B"
belief_base = BeliefBase()
belief_base.expand("A", display=False)
# belief_base.expand("~A")
belief_base.expand("A|B", display=False)
belief_base.expand("A=>B", display=False)

belief_2 = "~(A&B)"
belief_base_2 = BeliefBase()
belief_base_2.expand("A", display=False)
belief_base_2.expand("A|B", display=False)
belief_base_2.expand("A=>B", display=False)


# Verify AGM postulates
results = revision.verify_agm_postulates(belief_base=belief_base, belief=belief, belief_base_2=belief_base_2, belief_2=belief_2)

print(results)
print("---"*50)

# TEST 2
print("test 2:")
belief_base = BeliefBase()
belief_base.expand("p", display=False)
belief_base.expand("p|q", display=False)
belief_base.expand("p&q", display=False)
belief_base.expand("p<<>>q", display=False)
belief = "~p"
results = revision.verify_agm_postulates(belief_base=belief_base, belief=belief, belief_base_2=None, belief_2=None)

print(results)
print("---"*50)

# TEST 3
print("test 3:")
belief_base = BeliefBase()
belief_base.expand("p", display=False)
belief_base.expand("p|q", display=False)
belief_base.expand("p&q", display=False)
belief_base.expand("p<<>>q", display=False)

belief_base2 = BeliefBase()
belief_base2.expand("p", display=False)
belief_base2.expand("p|q", display=False)
belief_base2.expand("p&q", display=False)
belief_base2.expand("p<<>>q", display=False)

belief_base2.expand("~p", display=False)

results = revision.verify_agm_postulates(belief_base=belief_base, belief=belief, belief_base_2=belief_base2, belief_2=None)
print(results)
print("---"*50)

# TEST 4
print("test 4:")
belief_base = BeliefBase()
belief_base.expand("p")
belief_base.expand("p|q")
belief_base.expand("p&q")
belief_base.expand("p<<>>q")

belief_base2 = BeliefBase()
belief_base2.expand("p")
belief_base2.expand("p|q")
belief_base2.expand("p&q")
belief_base2.expand("p<<>>q")

belief_base2.expand("c")

belief = "c"

results = revision.verify_agm_postulates(belief_base=belief_base, belief=belief, belief_base_2=belief_base2, belief_2=None)
print(results)
print("---"*50)

# TEST 5
belief_base= BeliefBase()
belief_base.expand("p")
belief_base.expand("p|q")

belief = "~p"
results = revision.verify_agm_postulates(belief_base=belief_base, belief=belief, belief_base_2=None, belief_2=None)

