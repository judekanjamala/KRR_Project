# from turtle import update
import sys
from copy import deepcopy

from xml_parsers import INBUILT_PREDICATES_LOWER
from unification import match
from utils import evaluate_builtin_predicate, evaluate_term, refresh_variables, simplify, apply_substitution

# TODO
# 1. simplify:  Add check for circularity in substitution.


def solve_goals(kb, goals, mgu={}, cut_scope=False, depth=0):
    
    solved = False
    if goals:
        
        goal = goals[0]

        print(f"Depth: {depth}\nSolving goal: {goal}")

        if goal.name == "cut":
            solve_goals(kb, goals[1:], mgu, False, depth + 1)
            return True
        
        if goal.name == "not":
            if not solve_goals(kb, goal.args, mgu, cut_scope, depth + 1):
                return solve_goals(kb, goals[1:], mgu, cut_scope, depth + 1)
            else:
                return False
        
        if goal.name in INBUILT_PREDICATES_LOWER:
            if evaluate_builtin_predicate(goal, mgu):
                return solve_goals(kb, goals[1:], mgu, cut_scope, depth + 1)
            else:
                print("Returned False!\n")
                return False

        # Search for matching clause heads
        for i, head in enumerate(kb):

            if solved and cut_scope:
                break

            # suffix_variables(head, kb[head], i)
            head, body = refresh_variables(head, kb[head])
            
            # print("Matching Goal with:", head)
            unifier = match(goal, head, deepcopy(mgu))
                

            # unifier = simplify(unifier)
            
            # Check if match succeeded
            if unifier is None:
                # print("Failed matching.")
                continue
            
            else:
                # Reduction
                print(f"Depth: {depth}\ngoal: {goal}\nmatch: {head}")

                print(f"Unifier:")
                for k, v in unifier.items():
                    print(k,":", v)
                print("\n")

                for g in body:
                    if g.name == "cut":
                        cut_scope = True
                        

                updated_goals = body + goals[1:]
                updated_goals = [apply_substitution(g, unifier) for g in updated_goals]
                
                if updated_goals:
                    print("NEW GOALS:")
                    for g in updated_goals:
                        print(g)
                else:
                    print("All Goals Solved!!")
                print("\n")
                if solve_goals(kb, updated_goals, unifier, cut_scope, depth + 1):
                    solved = True
        
        if not solved:
            print("Failed to match Goal!")


    else:
        print(f"MGU:\n")
        for k, v in mgu.items():
            print(k,":", v)
        print("\n")

        variables_present = False
        for v in mgu:
            if v.clause == 'q':
                variables_present = True
                simplified_val = simplify(v, mgu)
                print(f"{v.name} = {evaluate_term(simplified_val)}")
        
        if not variables_present:
            print("True")
            sys.exit(0)


        explore_more = input("Enter c to look for more solutions:").lower()
        if explore_more == "c":
            solved = True
        else:
            sys.exit(0)

    return solved

