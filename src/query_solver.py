# from turtle import update
from inspect import trace
import sys
from copy import deepcopy

from xml_parsers import INBUILT_PREDICATES_LOWER
from unification import match
from utils import evaluate_builtin_predicate, evaluate_term, copy_clause, simplify, apply_substitution, trace_file

# TODO
# 1. simplify:  Add check for circularity in substitution.


def solve_goals(kb, goals, mgu={}, negated=False, cuts=0):

    '''
    Perform backward chaining by repeatedly popping head from goals and trying to 
    solve it. It checks if it is cut, negation, inbuilt predicate or user-defined predicate and performs the appropriate computation. It is mutually recursive with backward_chaining function.

    Args:
    1. kb: A dictionary {PredicateTerm : [PredicateTerm]}.
    2. goals: [PredicateTerm]
    3. mgu: {VariableTerm: Term}
    4. negated: True if the top level predicate is not, false otherwise.
    4. cuts: keeps track of the number cuts to be reached.

    Returns:
    1. True if a solution exists, false otherwise.
    '''

    if not goals:
        if negated:
            return True

        s = (f"MGU:\n")
        for k, v in mgu.items():
            s += f"{k} : {v}\n"
        print(f"{s}\n", file=trace_file)

        variables_present = False
        s = ''
        for v in mgu:
            if v.clause == 'q':
                variables_present = True
                # simplified_val = apply_substitution(v, mgu)
                simplified_val = simplify(v, mgu)
                eval_simple_val = evaluate_term(simplified_val)
                s += (f"{v.name} = {eval_simple_val}\n")
                print(f"{v.name} = {eval_simple_val}", file=trace_file)
        
        s = s[:-1]
        # For True or False queries
        if not variables_present:
            print("True")
            print("True", file=trace_file)
            sys.exit(0)


        explore_more = input(f"{s} ")
        if explore_more == ";":
            print("\nUser chose to continue\n", file=trace_file)
            return True
        else:
            sys.exit(0)

    goal = goals[0]

    print(f"\nSolving goal: {goal}", file=trace_file)

    mgu_copy = deepcopy(mgu)

    # Solve for cuts predicate
    if goal.name == "cut":
        cuts -= 1
        print(f"cuts count: {cuts}", file=trace_file)
        return solve_goals(kb, goals[1:], mgu_copy, False, cuts)

    # Solve for not predicate
    elif goal.name == "not":
        print("Recognized as negation", file=trace_file)
        if not solve_goals(kb, goal.args, mgu_copy, True, cuts):
            return solve_goals(kb, goals[1:], mgu_copy, negated, cuts)
        else:
            return False
    
    # Solve for other inbuilt predicates. The arguments of the predicates must
    # already be ground terms.
    elif goal.name in INBUILT_PREDICATES_LOWER:
        print("Recognized as inbuilt predicate", file=trace_file)
        if evaluate_builtin_predicate(goal):
            print("Returned True!\n", file=trace_file)
            return solve_goals(kb, goals[1:], mgu_copy, negated, cuts)
        else:
            print("Returned False!\n", file=trace_file)
            return False

    # Solve for user-defined predicates using backward-chaining
    else:
        print("Recognized as user-defined predicate", file=trace_file)
        return backward_chaining(kb, goal, goals[1:], mgu_copy, negated, cuts)
   

def backward_chaining(kb, goal, rest, mgu, negated, cuts):
    '''
    Tries to match the given goal with a clause in the KB. If a match is found then
    the resulting substitution is applied on the rest of the subgoals in body and
    goals to get an updated goal list. solve_goals is called on the updated goals.

    Args:
    1. kb: Same KB
    2. goal: PredicateTerm
    3. rest: Rest of the goals
    4. mgu: Same as solve_goals
    5. negated: Same as solve_goals
    6. cuts: Same as solve_goals

    Returns:
    True if solution exists, false otherwise.
    '''
    
    solution_exists = False
    
    for head in kb:

        # suffix_variables(head, kb[head], i)
        head_copy, body_copy = copy_clause(head, kb[head])
        
        # print("Matching Goal with:", head)
        unifier = match(goal, head_copy, deepcopy(mgu))
            
        # Check if match succeeded
        if unifier is None:
            # print("Failed matching.")
            continue

        # Reduction
        body_copy_s = ""
        for g in body_copy:
            body_copy_s += str(g) + ", "
        body_copy_s = body_copy_s[:-2]
        print(f"\ngoal: {goal}\nmatch: {head_copy}:-{body_copy_s}", file=trace_file)

        s = (f"Unifier:\n")
        for k, v in unifier.items():
            s += f"{k} :{v}\n"
        print(f"{s}\n", file=trace_file)

        for g in body_copy:
            if g.name == "cut":
                cuts += 1
                print(f"cuts count: {cuts}", file=trace_file)


        updated_goals = body_copy + rest
        updated_goals = [apply_substitution(g, unifier) for g in updated_goals]
        
        if updated_goals:
            s = ("NEW GOALS:\n")
            for g in updated_goals:
                s += str(g) + "\n"
        else:
            s = ("No Goals Left\n")

        print(f"{s}\n", file=trace_file)


        is_solved = solve_goals(kb, updated_goals, unifier, negated, cuts)
        
        if is_solved:
            solution_exists = True
            if cuts > 0:
                return True
    
    if not solution_exists:
        print("Failed to match Goal!", file=trace_file)

    return solution_exists

