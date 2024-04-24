# main.py

from belief_base import BeliefBase
from entailment import resolution

# Your main logic for belief revision goes here

def main():
    # Create initial belief base
    belief_base = BeliefBase()

    # Get initial belief base from the user
    initial_belief_base_input = input("Enter initial belief base (comma-separated): ")
    belief_base.update(initial_belief_base_input.split(','))

    while True:
        print("\nCurrent belief base:", belief_base)
        print("Options:")
        print("1. Check entailment")
        print("2. Contract belief base")
        print("3. Expand belief base")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            formula = input("Enter the formula to check for entailment: ")
            if resolution(belief_base, formula):
                print(f"The formula '{formula}' is entailed by the belief base.")
            else:
                print(f"The formula '{formula}' is not entailed by the belief base.")
        elif choice == '2':
            formula_to_remove = input("Enter the formula to remove from the belief base: ")
            belief_base.contraction(formula_to_remove) 
            print("Belief base after contraction:", belief_base)
        elif choice == '3':
            formula_to_add = input("Enter the formula to add to the belief base: ")
            belief_base.expansion(formula_to_add)
            print("Belief base after expansion:", belief_base)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()