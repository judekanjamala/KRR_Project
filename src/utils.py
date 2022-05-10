from classes import CompoundTerm, VariableTerm

trace_file = open("trace.txt", 'w')

def apply_substitution(term, sub):
    '''
    Takes a term and substitution dictionary and replaces variables in the term with
    available substitution.

    Args:
    1. term: Term
    2. sub: A dictionary {VariableTerm: Term}

    Returns:
    1. Substituted term.
    '''
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
    '''
    It takes a term and a dictionary mapping VariableTerms to VariableTerms and
    replaces all variableTerms in the term with dictionary value. It is a helper
    function.

    Args:
    1. term: Term
    2. sub: A dictionary {VariableTerm: VariableTerm}

    Returns:
    1.  term with replaced variables.
    '''

    if term.is_constant:
        return term

    elif term.is_variable:
        return sub[term]
    
    elif term.is_compound:
        args = [replace_variables(arg, sub) for arg in term.args]

        return CompoundTerm(term.name, args)


def copy_clause(head, body):
    '''
    It takes a clause head and body and generates duplicate of the clause having
    fresh variables for matching purposes during backward chaining.

    Args:
    1. head: PredicateTerm
    2. body: [PredicateTerm]  

    Returns:
    1. (head, refereshed body): duplicates of head and body.
    '''
    old_to_new = {}
    
    old_vars = head.variables
    for g in body:
        old_vars = old_vars.union(g.variables)

    old_to_new = {old_var: VariableTerm(old_var.name, old_var.clause) for old_var in old_vars}

    head = replace_variables(head, old_to_new)

    refreshed_body = [replace_variables(goal, old_to_new) for goal in body]

    return head, refreshed_body


def evaluate_builtin_predicate(predicate):
    '''
    Takes a binary PredicateTerm whose arguments are ground terms (do not contain variables)
    and evaluates it according to the semantics of prolog.

    Args:
    1. predicate: PredicateTerm

    Result:
    1. Boolean value.
    '''
    
    # Convert arguments in predicate to python values.
    arg1, arg2,  = map(evaluate_term,  predicate.args)
    
    if predicate.name == " true":
        return True
    elif predicate.name == "false":
        return False
    elif predicate.name == "not":
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
    '''
    It takes a term and converts into a python value. It is a helper function.

    Args:
    1. term: Term

    Returns:
    1. Some value corresponding to the term.
    '''

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


def simplify(term, sub, visited=set()):
    '''
    Takes a term and dictionary of substitutions that can be applied on the term so
    that long chains of variables are eliminated and only non-variable terms are left
    in the term.

    Args:
    1. term: Term
    2. sub: {VariableTerm: Term}

    Returns: Simplified term.
    '''
    
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