from turtle import update
import sys

def eval(term, var_sub):
    pass

def match(term1, term2, var_sub):


    if term1.is_atomic and term2.is_atomic:
        if term1 == term2:
            return var_sub
        else:
            return None
    
    elif term1.is_var:
        return var_match(term1, term2, var_sub)
    
    elif term2.is_var:
        return var_match(term2, term1, var_sub)
    
    elif len(term1) != len(term2):
        return None
    
    for i in range(len(term1)):
        var_sub = match(term1[i], term1[i], var_sub)
        if var_sub is None:
            return None

    return var_sub

def var_match(var, term2, var_sub):
    if var in term2:
        return None

    elif var in var_sub:
        var_sub = match(var_sub[var], term2, var_sub)
        return var_sub
    
    else:
        var_sub[var] = term2
        return var_sub
    

def instantiate_term(term, var_sub):
    if term.is_atomic:
        return term

    elif term.is_compound:
        instantiated_args = []
        for arg in term.args:
            instantiated_args.append(instantiate_term(arg, var_sub))
        
        return Term(term.name, instantiated_args)
    
    
def solve_goals(KB, goals, mgu={}):
    
    solved = False
    if goals:
        
        goal = goals.pop()
        print(f"Solving goal: {goal}")
        
        for head in KB:
            new_mgu = match(goal, head, mgu)
            
            # Check if match succeeded
            if new_mgu is None:
                continue
            
            else:
                print(f"Goal {goal} matched head {head} under MGU: {new_mgu}")

                body = KB[head]
                subgoals = [instantiate_term(subgoal, new_mgu) for subgoal in body[-1::-1]]
                if solve_goals(KB, goals + subgoals, new_mgu):
                    solved = True

    else:
        print(f"MGU: {mgu}")

        explore_more = input("Enter c to look for more solutions:").lower()
        if explore_more == "c":
            solved = True
        else:
            sys.exit(0)

    return solved

