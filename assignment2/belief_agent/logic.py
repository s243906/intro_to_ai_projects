"""
Logic module for belief revision.
Handles propositional logic operations including CNF conversion and resolution.
"""
from typing import Union, List, Tuple

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

def negate_formula(formula: str) -> str:
    """
    Negate a formula.
    Note: the difference between this func and negate_literal
    is the () that we wrap the formula in when returning.
    """
    if is_literal(formula):
        if formula.startswith('~'):
            return formula[1:]
        else:
            return f"~{formula}"
    else:
        if formula.startswith('~('):
            return formula[2:-1]
        else:
            return f"~({formula})"

def to_cnf(formula: str) -> List[List[str]]:
    """
    Convert a formula to Conjunctive Normal Form (CNF).
    
    This is a simplified version that handles basic propositional logic.
    """
    # handle literals directly
    if is_literal(formula):
        return [[formula]]
    
    # case 1: if conjunction
    if "&" in formula:
        print(f'HOLY SHIT IM IN AND -- {formula}')

        parts = formula.split("&")
        result = []

        for part in parts:
            part = part.strip()
            # remove parentheses if exists
            if part.startswith('(') and part.endswith(')'):
                part = part[1:-1].strip()
            
            cnf_part = to_cnf(part)
            result.extend(cnf_part)
        return result
    
    # case 2: if disjunction
    if "|" in formula:
        print(f'HOLY SHIT IM IN OR -- {formula}')
        parts = formula.split("|")
        clause = []
        for part in parts:
            part = part.strip()

            if part.startswith('(') and part.endswith(')'):
                part = part[1:-1].strip()
            
            print(part, is_literal(part))

            if is_literal(part):
                clause.append(part)                
        
        return [clause] if clause else []
    
    # case 3: negations
    # we deal with them using De Morgan's laws
    if formula.startswith('~('):
        print(f'HOLY SHIT IM IN NEGATIONS -- {formula}')
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
    
    # handle implications: A => B = ~A | B
    if "=>" in formula:
        print(f'HOLY SHIT IM IN IMPLICATIONS -- {formula}')
        parts = formula.split("=>")
        if len(parts) != 2:
            print(f"Invalid implication formula: {formula}")
            return []
        
        left = parts[0].strip()
        right = parts[1].strip()
        new_formula = f"~({left})|({right})"
        return to_cnf(new_formula)
    
    # return empty if not able to convert
    print(f"Could not convert to CNF: {formula}")
    return []

def resolve(clause1: List[str], clause2: List[str]) -> Tuple[bool, List[str]]:
    """
    Apply resolution to two clauses.
    """
    # try to find complementary literals
    for lit1 in clause1:
        for lit2 in clause2:
            if (lit1 == negate_literal(lit2)) or (negate_literal(lit1) == lit2):
                # create a new clause by resolving the two clauses
                resolved = [l for l in clause1 if l != lit1] + [l for l in clause2 if l != lit2]
                # remove duplicates
                resolved = list(set(resolved))
                return True, resolved
    
    return False, []

def negate_literal(literal: str) -> str:
    """
    Negate a literal.
    """
    if literal.startswith('~'):
        return literal[1:]
    else:
        return f"~{literal}"

def check_entailment(knowledge_base: List[List[str]], query: str) -> bool:
    """
    Check if a query is entailed by the knowledge base using resolution.
    """
    # for entailment check, we add the negation of the query to the KB
    # and check for unsatisfiability (which proves entailment)
    negated_query = negate_formula(query)
    negated_query_cnf = to_cnf(negated_query)
    print(f'CONVERTED NEGATED QUERY {negated_query} TO CNF --> {negated_query_cnf}')

    # create a combined set of clauses
    # concatenate existing clauses from KB with new one(s)
    clauses = knowledge_base.copy()
    for clause in negated_query_cnf:
        if clause not in clauses:
            clauses.append(clause)
    
    # apply resolution until we derive the empty clause or can't resolve further
    resolved_clauses = []
    while True:
        new_clause_added = False
        
        # generate all pairs of clauses to attempt resolution
        for i, clause_i in enumerate(clauses):
            for j, clause_j in enumerate(clauses[i+1:], i+1):
                success, resolved = resolve(clause_i, clause_j)
                if success:
                    # if we derive the empty clause, the KB entails the query
                    # if negation leads to a contradiction (empty clause), it means:
                    # the KB and the negation of the query cannot be true simultaneously -> entailment
                    if not resolved:
                        return True
                    
                    # add the new clause if we haven't seen it before
                    if resolved not in clauses and resolved not in resolved_clauses:
                        resolved_clauses.append(resolved)
                        new_clause_added = True
        
        # add all new clauses to the set of clauses
        for clause in resolved_clauses:
            if clause not in clauses:
                clauses.append(clause)
        resolved_clauses = []
        
        # if no new clauses were added, we're done
        if not new_clause_added:
            return False