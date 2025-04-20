"""
Logic module for belief revision.
Handles propositional logic operations including CNF conversion and resolution.
"""
from typing import Union

def parse_formula(formula: str) -> Union[str, None]:
    """
    Parse a propositional formula string into a standardized format.
    """
    formula = formula.strip()
    
    # check if it's just a literal
    if is_literal(formula):
        return formula
    
    # handle biconditional
    # the biconditional is converted to a conjunction of implications early in processing to simplify the
    # CNF conversion and standardize all formulas to use only core logical operators (AND, OR, NOT, IMPLIES)
    if "<<>>" in formula:
        parts = formula.split("<<>>")
        if len(parts) != 2:
            print(f"Invalid biconditional formula: {formula}")
            return None
        return f"({parts[0]}=>{parts[1]})&({parts[1]}=>{parts[0]})"
    
    return formula

def is_literal(formula: str) -> bool:
    """
    Check if a formula is a literal (a simple proposition or its negation).
    """
    if not formula:
        return False
    
    # positive literal case: just a char
    if len(formula) == 1 and formula.isalpha():
        return True
    
    # negative literal case: negated char
    if len(formula) == 2 and formula[0] == '~' and formula[1].isalpha():
        return True
    
    return False

def negate_formula(formula):
    """
    Negate a formula.
    
    Args:
        formula (str): The formula to negate
        
    Returns:
        str: The negated formula
    """
    if is_literal(formula):
        if formula.startswith('~'):
            return formula[1:]
        else:
            return f"~{formula}"
    
    return f"~({formula})"

def to_cnf(formula):
    """
    Convert a formula to Conjunctive Normal Form (CNF).
    
    This is a simplified version that handles basic propositional logic.
    For more complex formulas, a full CNF conversion algorithm would be needed.
    
    Args:
        formula (str): The formula to convert
        
    Returns:
        list: A list of clauses in CNF, where each clause is a list of literals
    """
    # Handle literals directly
    if is_literal(formula):
        return [[formula]]
    
    # Basic processing for simple conjunctions and disjunctions
    if "&" in formula:
        # Split by conjunction
        parts = formula.split("&")
        result = []
        for part in parts:
            part = part.strip()
            # Remove surrounding parentheses if present
            if part.startswith('(') and part.endswith(')'):
                part = part[1:-1].strip()
            
            cnf_part = to_cnf(part)
            result.extend(cnf_part)
        return result
    
    if "|" in formula:
        # Split by disjunction
        parts = formula.split("|")
        clause = []
        for part in parts:
            part = part.strip()
            # Remove surrounding parentheses if present
            if part.startswith('(') and part.endswith(')'):
                part = part[1:-1].strip()
            
            if is_literal(part):
                clause.append(part)
        
        return [clause] if clause else []
    
    # Handle negations with De Morgan's laws
    if formula.startswith('~('):
        inner = formula[2:-1].strip()
        if "&" in inner:
            # ~(A & B) = ~A | ~B
            parts = inner.split("&")
            new_formula = "|".join([f"~({part.strip()})" for part in parts])
            return to_cnf(new_formula)
        
        if "|" in inner:
            # ~(A | B) = ~A & ~B
            parts = inner.split("|")
            new_formula = "&".join([f"~({part.strip()})" for part in parts])
            return to_cnf(new_formula)
    
    # Handle implications: A => B = ~A | B
    if "=>" in formula:
        parts = formula.split("=>")
        if len(parts) != 2:
            print(f"Invalid implication formula: {formula}")
            return []
        
        left = parts[0].strip()
        right = parts[1].strip()
        new_formula = f"~({left})|({right})"
        return to_cnf(new_formula)
    
    # If we can't handle it, return an empty result
    print(f"Could not convert to CNF: {formula}")
    return []

def resolve(clause1, clause2):
    """
    Apply resolution to two clauses.
    
    Args:
        clause1 (list): First clause as a list of literals
        clause2 (list): Second clause as a list of literals
        
    Returns:
        tuple: (bool, list) - Whether resolution was successful, and the resulting clause
    """
    # Try to find complementary literals
    for lit1 in clause1:
        for lit2 in clause2:
            if (lit1 == negate_literal(lit2)) or (negate_literal(lit1) == lit2):
                # Create a new clause by resolving the two clauses
                resolved = [l for l in clause1 if l != lit1] + [l for l in clause2 if l != lit2]
                # Remove duplicates
                resolved = list(set(resolved))
                return True, resolved
    
    return False, []

def negate_literal(literal):
    """
    Negate a literal.
    
    Args:
        literal (str): The literal to negate
        
    Returns:
        str: The negated literal
    """
    if literal.startswith('~'):
        return literal[1:]
    else:
        return f"~{literal}"

def check_entailment(knowledge_base, query):
    """
    Check if a query is entailed by the knowledge base using resolution.
    
    Args:
        knowledge_base (list): List of CNF clauses
        query (str): The query formula
        
    Returns:
        bool: True if the query is entailed, False otherwise
    """
    # Convert query to CNF
    query_cnf = to_cnf(query)
    
    # For entailment check, we add the negation of the query to the KB
    # and check for unsatisfiability (which proves entailment)
    negated_query = negate_formula(query)
    negated_query_cnf = to_cnf(negated_query)
    
    # Create a combined set of clauses
    clauses = knowledge_base.copy()
    for clause in negated_query_cnf:
        if clause not in clauses:
            clauses.append(clause)
    
    # Apply resolution until we derive the empty clause or can't resolve further
    resolved_clauses = []
    while True:
        new_clause_added = False
        
        # Generate all pairs of clauses to attempt resolution
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                success, resolved = resolve(clauses[i], clauses[j])
                
                if success:
                    # If we derive the empty clause, the KB entails the query
                    if not resolved:
                        return True
                    
                    # Add the new clause if we haven't seen it before
                    if resolved not in clauses and resolved not in resolved_clauses:
                        resolved_clauses.append(resolved)
                        new_clause_added = True
        
        # Add all new clauses to the set of clauses
        for clause in resolved_clauses:
            if clause not in clauses:
                clauses.append(clause)
        resolved_clauses = []
        
        # If no new clauses were added, we're done
        if not new_clause_added:
            return False