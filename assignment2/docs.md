# Belief Revision System Documentation

## Overview of the Project

This project implements a belief revision system. The system allows users to manage a belief base of propositional logic formulas, with operations for expansion, contraction, and revision according to AGM postulates.

## Theoretical Background

The AGM framework provides postulates (correctness properties) that any rational belief revision system should satisfy. Our implementation:

1. Uses **partial meet contraction** as the concrete mechanism
2. Uses **priority-based selection** for choosing between remainder sets
3. **Tests against AGM postulates** to verify correctness

Important distinction: AGM postulates aren't the implementation method themselves, but rather the criteria against which our implementation is evaluated.
## Important Quotes
_In essence, entailment means "necessarily follows from" - if KB entails φ, then φ is guaranteed to be true in any world where KB is true._

_Contraction means "removing a belief" - but not by simply deleting statements. Instead, we remove just enough information so that a specific belief is no longer a logical consequence of what remains._

_Remainders are maximal subsets of your belief base that don't entail the belief you want to remove. Think of them as "what's left after removing minimal information to avoid entailing φ."_


## Implementation Structure

### 1. `logic.py`

This module handles propositional logic operations, including:

- Formula parsing and standardization
- CNF (Conjunctive Normal Form) conversion
- Resolution-based entailment checking

Key functions:
- `parse_formula()`: Standardizes propositional formulas
- `to_cnf()`: Converts formulas to CNF representation
- `check_entailment()`: Implements resolution for logical entailment

### 2. `belief_base.py`

This module defines the `BeliefBase` class that manages the collection of beliefs:

- Stores beliefs as a list of formulas
- Assigns and tracks priorities for beliefs
- Implements core operations: expansion, contraction, revision

Key methods:
- `add_belief()`: Adds a new belief with priority
- `expand()`: Simple expansion operation
- `contract()`: Implements partial meet contraction based on priorities
- `revise()`: Implements revision via the Levi Identity
- `entails()`: Checks if the belief base entails a formula

### 3. `revision.py`

This module provides the `BeliefRevision` class that:

- Wraps operations from `BeliefBase`
- Verifies AGM postulates compliance

Key methods:
- `expand()`, `contract()`, `revise()`: Wrappers for belief base operations
- `verify_agm_postulates()`: Tests if operations satisfy AGM postulates

### 4. `main.py`

The entry point for the application with a menu-based CLI:

- Options for expansion, contraction, revision
- Displaying the belief base
- Checking entailment
- Verifying AGM postulates

## Core Algorithms Explained

### Resolution for Entailment

The system uses resolution to check logical entailment:
1. Convert knowledge base to CNF
2. Add negation of the query formula
3. Apply resolution until either:
   - The empty clause is derived (proof of entailment)
   - No more resolutions are possible (proof of non-entailment)

### Partial Meet Contraction

For contraction of φ from the belief base:
1. Find all maximal subsets (remainders) that don't entail φ
2. Select the remainder with the highest sum of priorities
3. Update the belief base to this remainder

This is our concrete implementation approach, while the AGM postulates help us verify that this approach meets the theoretical requirements for rational belief revision.

### Belief Revision via Levi Identity

Revision implements the Levi Identity: K * A = (K ÷ ¬A) + A
1. Contract the negation of the new belief
2. Expand with the new belief

## Things To Do

1. **Thorough Testing**
   - Create comprehensive test cases for each component
   - Verify AGM postulates with complex examples

2. **Report Preparation**
   - Structure the report according to the assignment requirements

3. **Bug Fixing**
   - Review the CNF conversion for edge cases
   - Test complex formulas to ensure proper handling
  
4. **Mastermind Integration**
   - Decide whether to implement the optional Mastermind component
   - Design the propositional encoding for the game