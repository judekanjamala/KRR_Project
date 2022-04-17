from ast import Constant
import xml.etree.ElementTree as ET

from classes import ConstantTerm, VariableTerm, CompoundTerm


def parse_predicate(predicate, variable_terms={}, clause_num=None):
    
    variables = collect_variables(predicate)

    for v in variables:
        if v not in variable_terms:
            variable_terms[v] = VariableTerm(v, clause_num)

    if predicate.tag == "CONS":
        predicate.attrib["name"] = "cons"

    elif predicate.tag == "ADD":
        predicate.attrib["name"] = "add"

    elif predicate.tag == "EQ":
        predicate.attrib["name"] = "eq"

    elif predicate.tag == "FUNCTION":
        predicate.attrib["name"] = "function"

    elif predicate.tag == "CUT":
        predicate.attrib["name"] = "cut"

    elif predicate.tag == "NOT":
        predicate.attrib["name"] = "not"

    elif predicate.tag == "NE":
        predicate.attrib["name"] = "ne"

    elif predicate.tag == "GT":
        predicate.attrib["name"] = "gt"
    
    arg_terms = []
    for arg in predicate:
        
        if arg.tag == "CONSTANT":
            arg_terms.append(ConstantTerm(val=arg.text))
        
        elif arg.tag == "INTEGER":
            arg_terms.append(ConstantTerm(val=int(arg.text)))
        
        elif arg.tag == "VARIABLE":
            arg_terms.append(variable_terms[arg.text])
        
        elif arg.tag == "NIL":
            arg_terms.append(ConstantTerm(val='nil'))
        
        else:
            arg_terms.append(parse_predicate(arg, variable_terms))

    # print("Current")
    # print(predicate.tag, predicate.attrib)
    # print(arg.tag,arg.text)

    return CompoundTerm(name=predicate.attrib["name"], args=arg_terms)


def collect_variables(predicate):

    variables = set()

    for v in predicate.iter('VARIABLE'):
       variables.add(v.text)

    return variables


def parse_rule(rule, count):

    variables = set()
    for goal in rule:
        variables = variables.union(collect_variables(goal))
    
    variable_terms = {}
    for v in variables:
        variable_terms[v] = VariableTerm(v, count)
    
    head = parse_predicate(rule[0], variable_terms, count)

    body = []
    for goal in rule[1:]:
        body.append(parse_predicate(goal, variable_terms, count))
    
    return head, body


def parse_KB(file):

    tree = ET.parse(file)

    program = tree.getroot()

    kb = {}
    for i, clause in enumerate(program):
        
        if clause.tag == "FACT":
            fact = parse_predicate(clause[0], clause_num=i)
            kb[fact] = []
        
        elif clause.tag == "RULE":
            head, body = parse_rule(clause, i)
            kb[head] = body
        
    return kb


def parse_query(file):
    tree = ET.parse(file)

    query = tree.getroot()[0]

    goals = []
    for goal in query:
        goals.append(parse_predicate(goal, clause_num='q'))
    
    return goals

    
