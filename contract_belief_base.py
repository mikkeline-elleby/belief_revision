# contract_belief_base.py

def contract_belief_base(belief_base, priority_order):
    # Sort the priority order by priority, assuming higher priority comes first
    priority_order.sort(reverse=True)

    # Iterate over each formula in the priority order
    for formula in priority_order:
        # Check if the formula exists in the belief base
        if formula in belief_base:
            # Remove the formula and all formulas with lower priority
            belief_base = [f for f in belief_base if priority_order.index(f) >= priority_order.index(formula)]

    return belief_base

