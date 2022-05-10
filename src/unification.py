

def match(term1, term2, unifier={}):

    '''
    match tries to match term1 and term2.

    Args:
    1. term1: Term
    2. term2: Term
    3. unifier: {VariableTerm: Term}

    Returns:
    1. unifier: {VariableTerm: Term} if match succeed, None otherwise.

    '''
    # print(unifier)
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
    '''
    var_match matches var_term with term2 using unifier.

    Args:
    1. var_term: VariableTerm
    2. term2: Term
    3. unifier: {VariableTerm: Term}


    Returns:
    1. unifier: {VariableTerm: Term} if match succeed, None otherwise.
    '''

    if term2.is_compound and var_term in term2.variables:
        return None

    elif var_term in unifier:
        return match(unifier[var_term], term2, unifier)
    
    else:
        unifier[var_term] = term2
        return unifier

