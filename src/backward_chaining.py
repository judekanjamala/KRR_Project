# from turtle import update
import sys

from classes import CompoundTerm, VariableTerm

# TODO
# 1. simplify:  Add check for circularity in substitution.
# 2. evaluate_term: handles integer numbers only.
# 3. match: should return a fresh dictionary each time. 



def match(term1, term2, unifier):

    # print("Matching:")
    # print("TERM1:", term1)
    # print("TERM2:",term2 )
    # print("Unifier:")
    # for k, v in unifier.items():
    #     print(k,":", v)
    
    # print("\n")
    
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
        if term1.name != term2.name:
            return None
    
        elif len(term1.args) == len(term2.args):
            for i, term1_arg in enumerate(term1.args):
                unifier = match(term1_arg, term2.args[i], unifier)
                if unifier is None:
                    return None

            return unifier
        else:
            return None

    
    else:
        return None

def var_match(var_term, term2, unifier):
    if term2.is_compound and var_term in term2.variables:
        return None

    elif var_term.name in unifier:
        return match(unifier[var_term], term2, unifier)
    
    else:
        unifier[var_term] = term2
        return unifier


def apply_substitution(term, sub):
    if term.is_constant:
        return term

    elif term.is_variable:
        if term in sub:
            return sub[term]
        else:
            return term

    elif term.is_compound:
        instantiated_args = []
        # print(term)
        for arg in term.args:
            # print(arg)
            instantiated_args.append(apply_substitution(arg, sub))
        
        # print(instantiated_args)
        return CompoundTerm(term.name, instantiated_args)


def suffix_variables(head, body, suffix):
    
    for var in head.variables:
        var.name += str(suffix)
    
    for goal in body:
        for var in goal.variables:
            var.name += str(suffix)
    
    return

def evaluate_term(term):

    if term.is_constant:
        if term.val == "nil":
            return []
        
        else:
            return term.val
        
    if term.is_variable:
        return term.name
    
    elif term.is_compound:
        if term.name == "cons":
            head = evaluate_term(term.args[0])
            return [head] + evaluate_term(term.args[1])

        elif term.name == "add":
            arg1 = evaluate_term(term.args[0])
            arg2 = evaluate_term(term.args[1])
            if isinstance(arg1, int) and isinstance(arg2, int):
                val = arg1 + arg2
            else:
                val = f"({arg1} + {arg2})"
            return val
        
        elif term.name == "eq":
            arg1 = evaluate_term(term.args[0])
            arg2 = evaluate_term(term.args[1])

            val = f"({arg1} = {arg2})"
            return val
        
        elif term.name == "not":
            arg1 = evaluate_term(term.args[0])
            val = f"(not {arg1})"
            return val

        elif term.name == "ne":
            arg1 = evaluate_term(term.args[0])
            arg2 = evaluate_term(term.args[1])

            val = f"({arg1} != {arg2})"
            return val
        
        elif term.name == "gt":
            arg1 = evaluate_term(term.args[0])
            arg2 = evaluate_term(term.args[1])

            val = f"({arg1} > {arg2})"
            return val
        
        else:

            s = f"{term.name}("
            for arg in term.args:
                s += f"{evaluate_term(arg)}, "

            s = s[:-2] + ")"

            return s



def simplify(term, sub, visited=set()):

    if term.is_constant:
        return term
    
    elif term.is_variable:
        if term in sub:
            # visited.add(term)
            return simplify(sub[term], sub)
        else:
            return term
        
    elif term.is_compound:
        args = [simplify(arg, sub) for arg in term.args]

        return CompoundTerm(term.name, args)


def replace_variables(term, sub):

    if term.is_constant:
        return term

    elif term.is_variable:
        return sub[term]
    
    elif term.is_compound:
        args = [replace_variables(arg, sub) for arg in term.args]

        return CompoundTerm(term.name, args)


def refresh_variables(head, body):
    old_to_new = {}
    
    old_vars = head.variables
    for g in body:
        old_vars = old_vars.union(g.variables)

    old_to_new = {old_var: VariableTerm(old_var.name, old_var.clause) for old_var in old_vars}

    head = replace_variables(head, old_to_new)

    refreshed_body = [replace_variables(goal, old_to_new) for goal in body]

    return head, refreshed_body


def solve_goals(kb, goals, mgu={}):
    
    solved = False
    if goals:
        
        goal = goals.pop(0)


        print(f"Solving goal:\n{goal}\n")

        if goal.name == "not":
            print(f"Checking unsolvability of {goal.args[0].name}")
            return not solve_goals(kb, goal.args, mgu)

            
        
        # Search for matching clause heads
        for i, head in enumerate(kb):

            # suffix_variables(head, kb[head], i)
            head, body = refresh_variables(head, kb[head])
            unifier = match(goal, head, mgu)
                

            # unifier = simplify(unifier)
            
            # Check if match succeeded
            if unifier is None:
                continue
            
            else:
                # Reduction

                print(f"Head:\n{head}\n\nUnifier:")
                for k, v in unifier.items():
                    print(k,":", v)
                print("\n")

                updated_goals = body + goals
                updated_goals = [apply_substitution(g, unifier) for g in updated_goals]
                
                print("NEW GOALS:")
                for g in updated_goals:
                    print(g)
                print("\n")
                if solve_goals(kb, updated_goals, unifier):
                    solved = True
                

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
            solved = False
        else:
            sys.exit(0)

    return solved

