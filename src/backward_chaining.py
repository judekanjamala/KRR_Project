from turtle import update
from collections import deque
import sys


def match(term1, term2, unifier):

    if term1.is_constant and term2.is_constant:
        if term1.val == term2.val:
            return unifier
        else:
            return None
    
    elif term1.is_variable:
        return var_match(term1, term2, unifier)
    
    elif term2.is_variable:
        return var_match(term2, term1, unifier)
    
    elif term1.is_compound and term2.is_compound:
        if len(term1.args) != len(term2.args):
            return None
    
        for i, term1_arg in enumerate(term1.args):
            unifier = match(term1_arg, term2.args[i], unifier)
            if unifier is None:
                return None

        return unifier
    
    else:
        return None

def var_match(var_term, term2, unifier):
    if var_term in term2.variables:
        return None

    elif var_term.name in unifier:
        return match(unifier[var_term], term2, unifier)
    
    else:
        unifier[var_term] = term2
        return unifier


def apply_substitution(term, sub):
    if term.is_atomic:
        return term

    elif term.is_compound:
        instantiated_args = []
        for arg in term.args:
            instantiated_args.append(instantiate_term(arg, var_sub))
        
        return Term(term.name, instantiated_args)


def suffix_variables(head, body, suffix):
    
    for var in head.variables:
        var.name += str(suffix)
    
    for goal in body:
        for var in goal.variables:
            var.name += str(suffix)
    
    return


# def simplify(sub):
#     s


def solve_goals(KB, goals, mgu={}):
    
    solved = False
    if goals:
        
        goal = goals.pop(0)
        print(f"Solving goal: {goal}")
        
        # Search for matching clause heads
        for i, head in enumerate(KB):
            # suffix_variables(head, KB[head], i)
            unifier = match(goal, head, mgu)
            # unifier = simplify(unifier)
            
            # Check if match succeeded
            if unifier is None:
                continue
            
            else:
                # Reduction

                print(f"Goal {goal} matched head {head} under unifier: {unifier}")

                body = KB[head]
                updated_goals = body + goals
                updated_goals = [apply_substitution(g, unifier) for g in updated_goals]
                
                if solve_goals(KB, updated_goals, unifier):
                    solved = True

    else:
        print(f"MGU: {mgu}")

        explore_more = input("Enter c to look for more solutions:").lower()
        if explore_more == "c":
            solved = True
        else:
            sys.exit(0)

    return solved

