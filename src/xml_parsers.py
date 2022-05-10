import sys
import xml.etree.ElementTree as ET

from classes import ConstantTerm, VariableTerm, FunctionTerm, PredicateTerm

INBUILT_FUNCTIONS = {"CONS", "NEG", "ADD", "SUB", "MUL", "DIV", "MOD"}
INBUILT_PREDICATES = {"LT", "LE", "EQ", "GE", "GT", "NE", "NOT", "FALSE", "TRUE", "CUT"}                     

INBUILT_PREDICATES_LOWER = {s.lower() for s in INBUILT_PREDICATES}
INBUILT_FUNCTIONS_LOWER = {s.lower() for s in INBUILT_FUNCTIONS}
INBUILT_PREDICATES_LOWER.remove("eq")

# TODO
# 1. parse_predicate:
#    1. Remove the variable collection code, instead relying on call by reference
#        property. variable_terms will add a new entry whenever a new one is
#        encountered and this will be retained when returning from the call.
#    2. Move FUNCTION PARSING to argument parsing part of parse_predicate.
# 2. Differentiate between compound terms that are functions and predicates.


def parse_function(fn, variable_terms, clause_num):
    '''
    parse_function parses a function xml element into a FunctionTerm Object.

    Args:
    1. fn: xml-element
    2. variable_terms: Dictionary {variable-name:: VariableTerm}
    3. clause_num: clause in which function is present.

    Returns:
    1. FunctionTerm
    '''

    # Parse arguments to function
    arg_terms = []
    for arg in fn:
        
        if arg.tag == "CONSTANT":
            arg_terms.append(ConstantTerm(val=arg.text))
        
        elif arg.tag == "INTEGER":
            arg_terms.append(ConstantTerm(val=int(arg.text)))
        
        elif arg.tag == "VARIABLE":
            if arg.text in variable_terms:
                arg_terms.append(variable_terms[arg.text])
        
        elif arg.tag == "NIL":
            arg_terms.append(ConstantTerm(val='[]'))
        
        elif arg.tag in INBUILT_FUNCTIONS:
            arg.attrib["name"] = arg.tag.lower()
            arg_terms.append(parse_function(arg, variable_terms, clause_num))

        elif arg.tag == "FUNCTION":
            arg_terms.append(parse_function(arg, variable_terms, clause_num))

        else:
            raise Exception(f"Unknown Argument Type: ", arg.tag)
            sys.exit(0)

    # print("CONSTRUCTING COMPOUNDTERM")
    # print(predicate.tag, predicate.attrib)
    # print(arg.tag,arg.text)

    return FunctionTerm(name=fn.attrib["name"], args=arg_terms)
   

def parse_predicate(predicate, variable_terms={}, clause_num=None):
    '''
    parse_predicate parses a predicate xml element into a PredicateTerm Object.

    Args:
    1. predicate: xml-element
    2. variable_terms: Dictionary {variable-name:: VariableTerm}
    3. clause_num: clause in which function is present.

    Returns:
    1. PredicateTerm
    '''
    
    # Collect all unique variables in the predicate.
    # print("VARIABLES", variable_terms)
    variables = collect_variables(predicate)

    for v in variables:
        if v not in variable_terms:
            variable_terms[v] = VariableTerm(v, clause_num)
    
    # Capture predicate name
    # print("VARIABLES AFTER COLLECTION", variable_terms)
    if predicate.tag == "NOT":
        arg, = predicate
        return PredicateTerm("not", args=[parse_predicate(arg)])

    elif predicate.tag in INBUILT_PREDICATES:
        predicate.attrib["name"] = predicate.tag.lower()
        
    # Parse arguments to predicate
    arg_terms = []
    for arg in predicate:
        
        if arg.tag == "CONSTANT":
            arg_terms.append(ConstantTerm(val=arg.text))
        
        elif arg.tag == "INTEGER":
            arg_terms.append(ConstantTerm(val=int(arg.text)))
        
        elif arg.tag == "VARIABLE":
            if arg.text in variable_terms:
                arg_terms.append(variable_terms[arg.text])
        
        elif arg.tag == "NIL":
            arg_terms.append(ConstantTerm(val='[]'))
        
        elif arg.tag in INBUILT_FUNCTIONS:
            arg.attrib["name"] = arg.tag.lower()
            arg_terms.append(parse_function(arg, variable_terms, clause_num))

        elif arg.tag == "FUNCTION":
            arg_terms.append(parse_function(arg, variable_terms, clause_num))

        else:
            raise Exception(f"Unknown Argument Type ", arg.tag, " in predicate ", predicate.attrib["name"])
            sys.exit(0)

    # print("CONSTRUCTING COMPOUNDTERM")
    # print(predicate.tag, predicate.attrib)
    # print(arg.tag,arg.text)

    return PredicateTerm(name=predicate.attrib["name"], args=arg_terms)


def collect_variables(predicate):
    '''
    Collect all variable names present in the predicate.

    Args:
    1. predicate: Predicate XML element.

    Returns:
    1. variables: A set, {variable-names}
    '''

    # print("COLLECTING VARIABLES")
    variables = set()

    for v in predicate.iter('VARIABLE'):
       variables.add(v.text)

    return variables


def parse_rule(rule, count):
    '''
    parse_rule parses rule XML element into a head PredicateTerm and body, a list of 
    PredicateTerms.

    Args:
    1. rule: Rule XML element.
    2. count: Serial number of the rule being processed.

    Returns:
    1. (head, body) 
    '''

    # print("PARSING RULE")

    variables = set()
    for goal in rule:
        variables = variables.union(collect_variables(goal))
    
    variable_terms = {}
    for v in variables:
        variable_terms[v] = VariableTerm(v, count)
    
    # print(f"VARIABLES:", variable_terms)
    
    # print("PARSING HEAD")
    head = parse_predicate(rule[0], variable_terms, count)

    # print("PARSING BODY")
    body = []
    for goal in rule[1:]:
        body.append(parse_predicate(goal, variable_terms, count))
    
    return head, body


def parse_KB(file):
    '''
    parse_KB takes an XML file containing the clause elements and parses into a 
    dictionary clauses having keys as heads of the clauses and values as body of the 
    clause. Facts have no bodies and are denoted by empty lists.

    Args:
    1.file: XML file (there should not be any queries in the KB file)

    Returns:
    1. kb: {PredicateTerm: [PredicateTerms]}
    '''

    tree = ET.parse(file)
    program = tree.getroot()

    kb = {}
    for i, clause in enumerate(program):
        
        i += 1
        # print(f"PARSING {i}th CLAUSE")
        if clause.tag == "FACT":
            fact = parse_predicate(clause[0], clause_num=i)
            kb[fact] = []
        
        elif clause.tag == "RULE":
            head, body = parse_rule(clause, i)
            kb[head] = body
        
    return kb


def parse_query(file):
    '''
    It parses an XML file containing a query into a list of PredicateTerms. It 
    reuses parse_rule function to parse the query XML element and is called with a 
    special count value of q to mark the predicates as being queries.

    Args:
    1. file: An XML file containing query.

    Returns:
    1. goals: A list of PredicateTerms
    '''

    tree = ET.parse(file)

    query = tree.getroot()[0]
    head, body = parse_rule(query, 'q')

    goals = [head] + body
    
    return goals

    
