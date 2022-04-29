from classes import CompoundTerm, VariableTerm


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


def evaluate_builtin_predicate(predicate, mgu):
    
    arg1, arg2,  = map(evaluate_term,  predicate.args)
    
    if predicate.name == " true":
        return True
    elif predicate.name == "false":
        return False
    elif predicate.name == "not":
        raise NotImplementedError
    elif predicate.name == "cut":
        raise NotImplementedError
    elif predicate.name == "lt":
        return arg1 < arg2
    elif predicate.name == "le":
        return arg1 <= arg2
    
    # Replace eq evaluation with a eq clause addition to kb.
    # elif predicate.name == "eq":
    #     return arg1 == arg2
    elif predicate.name == "gt":
        return arg1 > arg2
    elif predicate.name == "ge":
        return arg1 >= arg2
    elif predicate.name == "ne":
        return arg1 != arg2
    else:
        raise NotImplementedError

def evaluate_term(term):

    if term.is_constant:
        if term.val == "[]":
            return []
        
        else:
            return term.val
        
    if term.is_variable:
        return term.name
    
    elif term.is_compound:
        if term.name == "cons":
            head = evaluate_term(term.args[0])

            val = [head] + evaluate_term(term.args[1])

        elif term.name == "add":
            arg1 = evaluate_term(term.args[0])
            arg2 = evaluate_term(term.args[1])
            # if isinstance(arg1, int) and isinstance(arg2, int):
            val = arg1 + arg2
        
        elif term.name == "sub":
            arg1 = evaluate_term(term.args[0])
            arg2 = evaluate_term(term.args[1])
            val = arg1 - arg2
        
        elif term.name == "mul":
            arg1 = evaluate_term(term.args[0])
            arg2 = evaluate_term(term.args[1])
            val = arg1 * arg2

        elif term.name == "div":
            arg1 = evaluate_term(term.args[0])
            arg2 = evaluate_term(term.args[1])

            val = arg1 / arg2
        
        elif term.name == "mod":
            arg1 = evaluate_term(term.args[0])
            arg2 = evaluate_term(term.args[1])

            val = arg1 % arg2
        
        elif term.name == "neg":
            arg1 = evaluate_term(term.args[0])
            val = -1 * (arg1)

        else:

            s = f"{term.name}("
            for arg in term.args:
                s += f"{evaluate_term(arg)}, "

            val = s[:-2] + ")"

        return val


def simplify(term, sub,visited=set()):
    
    if term.is_constant:
        return term
    
    elif term.is_variable:

        if term in sub:
            sub[term] = simplify(sub[term], sub)
            return sub[term]
        else:
            return term
        
    elif term.is_compound:
        args = [simplify(arg, sub) for arg in term.args]

        return CompoundTerm(term.name, args)