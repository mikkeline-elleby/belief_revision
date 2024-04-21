# entailment.py

# to call this file the method resolution() should be called. This takes a belief base and an alpha and will firstly convert
# and(KB,not(alpha)) into CNF and then perform the resolution algorithm. 

CLAUSES = []
NEW = []
RESOLVENTS = []
LITERALS1 = []
LITERALS2 = []

# converts the "KB and not(alpha)" to CNF
def convert_to_CNF(formula):
    formula = eliminate_bi_and_imp_helper(formula)
    formula = de_morgans_helper(formula)
    formula = eliminate_double_negation_helper(formula)
    formula = distributive_laws_helper(formula)

    return formula


# combines the believes in the belief base and the negated alpha formula with conjunctions.
def make_formula(f,belief_base):
    if len(belief_base) == 1:
        return belief_base[0]
    else:
        b = belief_base[0]
        f = "and(" + b + "," + make_formula(f,belief_base[1:])
        return f + ")"
    

# makes sure that the comma (seperating the elements of a function fx the and-function) corresponds to the correct function
def matching_comma(formula):
    count = 0
    comma_index = 0
    for i, char in enumerate(formula):
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
        elif char == "," and count == 1:  # Comma is at the top level
            comma_index = i
            break
    return comma_index

# takes a clause and appends its literals to either LITERALS1 or LITERALS2
def to_literals(formula,id):
    if formula[0:2] == "or":
        comma_index = matching_comma(formula)
        A = formula[3:comma_index]
        B = formula[comma_index+1:-1]
        to_literals(A,id)
        to_literals(B,id)
    
    else:
        if id == "1":
            LITERALS1.append(formula)
        else: 
            LITERALS2.append(formula)

# convert a list of literals into a clause 
def from_literals_to_clause(f,literals):
    if len(literals) == 1:
        return literals[0]
    else:
        b = literals[0]
        f = "or(" + b + "," + make_formula(f,literals[1:])
        return f + ")"

# this method takes two clauses and resolve their possible complementary literals
def resolve(c1,c2):
    to_literals(c1,"1")
    to_literals(c2,"2")
    #print("c1:",c1,"c2:",c2,"LITERALS1:",LITERALS1)

    for l1 in LITERALS1:
        for l2 in LITERALS2:
            if l1 == "not(" + l2 + ")" or l2 == "not(" + l1 + ")" and LITERALS1.index(l1) < LITERALS2.index(l2):
                print("resolved", l1,"and",l2,"with",c1,"and",c2)
                #print(CLAUSES)

                LITERALS1.remove(l1)
                LITERALS2.remove(l2)
                new_literals = LITERALS1+LITERALS2
                print("new_literals",new_literals)
                
                if len(new_literals) == 0:
                    return "empty"

                new_clause = from_literals_to_clause("",new_literals)
                return new_clause

    return None

# takes a conjunction of disjunctions (clauses) and appends these clauses to the list CLAUSES
def to_clauses(formula):
    if formula[0:3] == "and":
        comma_index = matching_comma(formula)
        A = formula[4:comma_index]
        B = formula[comma_index+1:-1]
        to_clauses(A)
        to_clauses(B)
    
    else:
        CLAUSES.append(formula)


# the resoution function definition takes the belief base and an alpha, and converts the sentence and(KB,not(alpha))
# into CNF. Then it appends the clauses in the CNF formula to the global list CLAUSES.
# Lasty, the method loops through each pair of clauses to resolve possibe complementary literals.
def resolution(belief_base,alpha):
    negated_alpha = "not(" + alpha + ")"
    formula = belief_base + [negated_alpha]
    formula = make_formula("",formula)
    formula = convert_to_CNF(formula)

    print("CNF convertion completed. The sentence is:\n", formula)
    to_clauses(formula)
    print("\nThe clauses are:",CLAUSES)

    # if there is ony one clause, then we cannot obtain the empty clause
    if len(CLAUSES) == 1:
        return False # KB does not entail alpha
    

    # for each pair of clauses in CLAUSES we resolve the clauses, return true if we obtain the empty clause,
    # otherwise we unify NEW and RESOLVENTS (and empty RESOLVENTS), if NEW is just a subset of CLAUSES we return False,
    # since there would be no new clauses to add to CLAUSES. If NEW is not a subset of CLAUSES, we unify them and make
    # another iteration in the loop.
    while(True):
        for c1 in CLAUSES:
            for c2 in CLAUSES.copy():
                if c1 != c2 and CLAUSES.index(c2) > CLAUSES.index(c1):
                    r = resolve(c1,c2)
                    LITERALS1.clear()
                    LITERALS2.clear()
                    if r != None:
                        RESOLVENTS.append(r) 
                    if "empty" in RESOLVENTS:
                        return True # KB entails alpha
        NEW.extend(RESOLVENTS)
        RESOLVENTS.clear()
        print("CLAUSE",CLAUSES)
        if set(NEW).issubset(CLAUSES):
            return False # KB does not entail alpha
        
        CLAUSES.extend(NEW)
        NEW.clear()


# iterates over the formula until no changes are made (there are no impications or biimplications to eliminate)
def eliminate_bi_and_imp_helper(formula):
    new_formula = eliminate_bi_and_imp(formula)
    while(formula != new_formula):
        formula = new_formula
        new_formula= eliminate_bi_and_imp(formula)
    return new_formula

# recurses over the elements in the given formula and eliminates implications and biimplication
def eliminate_bi_and_imp(formula):
    # in the case of a biimplication we substitute it with its logically equivallent function: and(imp(a,b),imp(b,a))
    if formula[0:2] == "bi":
        comma_index = matching_comma(formula)
        A = formula[3:comma_index]
        B = formula[comma_index+1:-1]

        A = eliminate_bi_and_imp(A)
        B = eliminate_bi_and_imp(B)
        return "and(imp(" + A + "," + B + "),imp(" + B + "," + A + "))"
    
    # in the case of an implication we substitute it with its logically equivallent function: not(or(a,b))
    elif formula[0:3] == "imp":
        comma_index = matching_comma(formula)
        A = formula[4:comma_index]
        B = formula[comma_index+1:-1]
        return "or(not(" + eliminate_bi_and_imp(A) + ")," + eliminate_bi_and_imp(B) + ")"
    
    # a simple conjunction or disjunctions
    elif formula[0:3] == "and" or formula[0:2] == "or":
        comma_index = matching_comma(formula)
        parentises_index = formula.index("(")
        A = formula[parentises_index+1:comma_index]
        B = formula[comma_index+1:-1]
        return formula[:parentises_index+1] + eliminate_bi_and_imp(A) + "," + eliminate_bi_and_imp(B) + ")"
    
    # a simple negation
    elif formula[0:3] == "not":
        index = formula.index("(")
        return "not(" + eliminate_bi_and_imp(formula[index+1:-1]) + ")"
    
    # in the "otherwise" case the formula is a symbol and is returned
    else:
        return formula

# iterates over the formula until no changes are made (there are no negations to push inwards)
def de_morgans_helper(formula):
    new_formula = de_morgans(formula)
    while(formula != new_formula):
        formula = new_formula
        new_formula= de_morgans(formula)
    return new_formula

# A method for pushing negation inwards using De Morgan's laws
def de_morgans(formula):
    # the first De Morgan's law says that not(and(a,b)) is logically equivalent to or(not(a),not(b))
    if formula[0:7] == "not(and":
        comma_index = 4 + matching_comma(formula[4:-1])
        A = formula[8:comma_index]
        B = formula[comma_index+1:-2]
        return "or(not(" + de_morgans(A) + "),not(" + de_morgans(B) + "))"

    # the second De Morgan's law says that not(or(a,b)) is logically equivalent to and(not(a),not(b))
    elif formula[0:6] == "not(or":
        comma_index = 4 + matching_comma(formula[4:-1])
        A = formula[7:comma_index]
        B = formula[comma_index+1:-2]
        return "and(not(" + de_morgans(A) + "),not(" + de_morgans(B) + "))"
    
    # a simple negation
    elif formula[0:3] == "not":
        index = formula.index("(")
        return "not(" + de_morgans(formula[index+1:-1]) + ")"

    # a simple conjunction or disjunction
    elif formula[0:3] == "and" or formula[0:2] == "or": 
        comma_index = matching_comma(formula)
        parentises_index = formula.index("(")
        A = formula[parentises_index+1:comma_index]
        B = formula[comma_index+1:-1]
        return formula[:parentises_index+1] + de_morgans(A) + "," + de_morgans(B) + ")"
    
    # in the "otherwise" case the formula is a symbol and is returned
    else:
        return formula

# iterates over the formula until no changes are made (there are no double negations)
def eliminate_double_negation_helper(formula):
    new_formula = eliminate_double_negation(formula)
    while(formula != new_formula):
        formula = new_formula
        new_formula= eliminate_double_negation(formula)
    return new_formula

# eliminates double negations by recursing throught the formula
def eliminate_double_negation(formula):
    # in the case of a double negation
    if formula[0:7] == "not(not":
        return eliminate_double_negation(formula[8:-2])
    
    # a simple conjunction or disjunction
    elif formula[0:3] == "and" or formula[0:2] == "or":
        comma_index = matching_comma(formula)
        parentises_index = formula.index("(")
        A = formula[parentises_index+1:comma_index]
        B = formula[comma_index+1:-1]
        return formula[:parentises_index+1] + eliminate_double_negation(A) + "," + eliminate_double_negation(B) + ")"
    
    # a simple negation
    elif formula[0:3] == "not":
        return "not(" + eliminate_double_negation(formula[4:-1]) + ")"
    
    # in the "otherwise" case the formula is a symbol and is returned
    else:
        return formula

# iterates over the formula until no changes are made (there are no longer conjunctions within disjunctions)
def distributive_laws_helper(formula):
    new_formula = distributive_laws(formula)
    while(formula != new_formula):
        formula = new_formula
        new_formula= distributive_laws(formula)
    return new_formula

# the last step in the CNF convertion is elimination of conjunctions within disjunctions using
# the distributive laws.
def distributive_laws(formula):
    if formula[0:2] == "or":
        comma_index = matching_comma(formula)
        
        # the first distributive law "A or (B and C) is logically equivalent to (A or B) and (A or C)" 
        if formula[comma_index+1:comma_index+4] == "and":
            A = formula[3:comma_index]
            comma_index2 = matching_comma(formula[comma_index+1:-1]) + comma_index + 1
            B = formula[comma_index+5:comma_index2]
            C = formula[comma_index2+1:-2]
            return "and(or(" + distributive_laws(A) + "," + distributive_laws(B) + "),or(" + distributive_laws(A) + "," + distributive_laws(C) + "))"
        
        # the second distributive law "(A and B) or C) is logically equivalent to (A or C) and (B or C)" 
        elif formula[3:6] == "and":
            comma_index2 = matching_comma(formula[3:-1]) + 3
            A = formula[7:comma_index2]
            B = formula[comma_index2+1:comma_index-1]
            C = formula[comma_index+1:-1]
            return "and(or(" + distributive_laws(A) + "," + distributive_laws(C) + "),or(" + distributive_laws(B) + "," + distributive_laws(C) + "))"
        
        else:
            # the case when the disjunction does not contain any conjunctions
            A = formula[3:comma_index]
            B = formula[comma_index+1:-1]
            return "or(" + distributive_laws(A) + "," + distributive_laws(B) + ")"
    
    # a simple conjunction
    elif formula[0:3] == "and":
        comma_index = matching_comma(formula)
        parentises_index = formula.index("(")
        A = formula[parentises_index+1:comma_index]
        B = formula[comma_index+1:-1]
        return formula[:parentises_index+1] + distributive_laws(A) + "," + distributive_laws(B) + ")"
    
    # a simple negation
    elif formula[0:3] == "not":
        index = formula.index("(")
        return "not(" + distributive_laws(formula[index+1:-1]) + ")"

    # in the "otherwise" case the formula is a symbol and is returned
    else:
        return formula

if __name__ == '__main__':  
    print(resolution(["bi(r,or(p,s))","not(r)"],"not(p)"))
    #print(distributive_laws("or(a,and(b,c))")) #should give and(or(a,b),or(a,c))
    #print(distributive_laws("or(and(a,b),c)")) #should give and(or(a,c),or(b,c))
    #print(eliminate_double_negation("and(p,not(not(s)))"))    
    #print(de_morgans("and(p,not(or(w,e)))"))
    #convert_to_CNF(["and(p,q)","not(a)","or(a,b)", "or(not(a),b)","bi(not(p),a)", "imp(a,and(b,q))"],"or(p,t)")

