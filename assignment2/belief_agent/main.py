"""
Main entry point for the belief revision system.
"""

from belief_base import BeliefBase
from revision import BeliefRevision

def display_menu():
    """Display the main menu options."""
    print("\n====== Belief Revision System ======")
    print("1. Add a belief (Expansion)")
    print("2. Revise belief base")
    print("3. Contract belief base")
    print("4. Display belief base")
    print("5. Check entailment")
    print("6. Verify AGM postulates")
    print("7. Exit")
    print("===================================")

def main():
    """Main function for the belief revision system."""
    print("Welcome to the Belief Revision System!")
    print("This system allows you to add, revise, and query beliefs.")
    print("Beliefs should be entered in propositional logic format.")
    print("Operators: & (AND), | (OR), ~ (NOT), => (IMPLIES), <<>> (BICONDITIONAL)")
    
    belief_base = BeliefBase()
    revision = BeliefRevision()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            # Simply adds a new belief to your belief base without checking for conflicts.
            belief = input("Enter a belief to add: ").strip()
            if revision.expand(belief_base, belief):
                print("Belief added successfully.")
            else:
                print("Failed to add belief.")
                
        elif choice == "2":
            # Adds a new belief while ensuring your belief base remains consistent.
            belief = input("Enter a belief to revise with: ").strip()
            if revision.revise(belief_base, belief):
                print("Belief base revised successfully.")
            else:
                print("Failed to revise belief base.")
                
        elif choice == "3":
            # Removes a belief (and possibly others) so that the specified belief is no longer entailed by the belief base.
            belief = input("Enter a belief to contract: ").strip()
            if revision.contract(belief_base, belief):
                print("Belief contracted successfully.")
            else:
                print("Failed to contract belief.")
                
        elif choice == "4":
            # Shows all current beliefs in your belief base along with their priority values.
            belief_base.display()
            
        elif choice == "5":
            # Tests whether a given belief logically follows from your current belief base.
            belief = input("Enter a belief to check entailment: ").strip()
            if belief_base.entails(belief):
                print(f"The belief base entails '{belief}'.")
            else:
                print(f"The belief base does NOT entail '{belief}'.")
                
        elif choice == "6":
            # Tests whether belief revision operations satisfy theoretical requirements for rational belief revision.
            belief = input("Enter a belief to verify AGM postulates: ").strip()
            results = revision.verify_agm_postulates(belief_base, belief)
            print("\nAGM Postulates Verification:")
            for postulate, result in results.items():
                result_text = "Satisfied" if result is True else "Not satisfied" if result is False else result
                print(f"  {postulate}: {result_text}")
                
        elif choice == "7":
            print("Thank you for using the Belief Revision System. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()