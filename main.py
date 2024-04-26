# main.py

from belief_base import BeliefBase
from entailment import resolution

def main():
    # Create initial belief base
    belief_base = BeliefBase()

    # Get initial belief base from the user
    print("The format in the belief base is as follows:")
    print("p, not(p), and(p,q), or(p,q), imp(p,q) and bi(p,q)")
    try:
        initial_belief_base_input = input("Enter initial belief base (space-separated): ")
        belief_base.formulas = {x.strip(',') for x in initial_belief_base_input.split(' ')}
    except:
        print("Inital belief base has wrong input -> belief base is empty")

    while True:
        print("\nCurrent belief base:", belief_base.formulas)
        print("Options:")
        print("1. Check entailment")
        print("2. Contract belief base")
        print("3. Revise belief base")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            formula = input("Enter the formula to check for entailment: ")
            if resolution(belief_base.formulas, formula):
                print(f"The formula '{formula}' is entailed by the belief base.")
            else:
                print(f"The formula '{formula}' is not entailed by the belief base.")
        elif choice == '2':
            formula_to_remove = input("Enter the formula to remove from the belief base: ")
            belief_base.contraction(formula_to_remove)
            print("Belief base after contraction:", belief_base)
        elif choice == '3':
            formula_to_add = input("Enter the formula to revise the belief base with: ")
            belief_base.expansion(formula_to_add)
            print("Belief base after revision:", belief_base)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()