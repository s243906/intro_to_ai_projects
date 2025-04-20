# Belief Revision System

This is a Python implementation of a belief revision system based on the AGM (Alchourrón, Gärdenfors, and Makinson) theory of belief revision. The system allows for the representation, querying, and revision of beliefs in propositional logic.

## Components

The system consists of the following components:

1. **logic.py**: Provides functionality for handling propositional logic, including parsing formulas, converting to Conjunctive Normal Form (CNF), and checking entailment using resolution.

2. **belief_base.py**: Implements the BeliefBase class that stores beliefs and their priorities, and provides methods for adding, contracting, and revising beliefs.

3. **revision.py**: Implements the BeliefRevision class that provides AGM-compliant operations for belief expansion, contraction, and revision.

4. **main.py**: Provides a command-line interface for interacting with the belief revision system.

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Running the System

1. Clone the repository or extract the provided files to a directory.
2. Navigate to the directory in a terminal.
3. Run the following command:

```bash
cd belief_agent
python main.py
```

## Using the System

The system provides a menu-based interface with the following options:

1. **Add a belief (Expansion)**: Adds a new belief to the belief base without checking for consistency.
2. **Revise belief base**: Adds a new belief while ensuring the belief base remains consistent.
3. **Contract belief base**: Removes a belief from the belief base.
4. **Display belief base**: Shows the current beliefs and their priorities.
5. **Check entailment**: Checks if a given belief is entailed by the belief base.
6. **Verify AGM postulates**: Verifies that the belief revision operations satisfy the AGM postulates.
7. **Exit**: Exits the system.

### Input Format

Beliefs should be entered in propositional logic format using the following operators:

- `&`: Conjunction (AND)
- `|`: Disjunction (OR)
- `~`: Negation (NOT)
- `=>`: Implication (IF-THEN)
- `<<>>`: Biconditional (IF AND ONLY IF)

Examples:
- `p` (simple proposition)
- `~p` (negation)
- `p & q` (conjunction)
- `p | q` (disjunction)
- `p => q` (implication)
- `p <<>> q` (biconditional)

## Technical Details

### Belief Base

Beliefs are stored in the belief base along with their priorities. The priority of a belief is determined by its complexity, with more complex formulas generally having higher priorities.

### Belief Revision

The belief revision process follows the AGM postulates:

1. **Success**: After revision with A, A is accepted in the belief base.
2. **Inclusion**: The revised belief base is a subset of the expansion of the original belief base with A.
3. **Vacuity**: If the negation of A is not in the original belief base, then revision with A is equivalent to expansion with A.
4. **Consistency**: The revised belief base is consistent, unless A is inconsistent.
5. **Extensionality**: If A and B are logically equivalent, then revision with A is the same as revision with B.

### Contraction

Contraction is implemented using partial meet contraction, which involves finding maximal subsets of the belief base that do not entail the belief to be contracted, and then selecting a subset based on priorities.

### Entailment Checking

Entailment is checked using resolution-based theorem proving in propositional logic. The system converts formulas to CNF and applies resolution until either the empty clause is derived (indicating entailment) or no further resolutions are possible (indicating non-entailment).