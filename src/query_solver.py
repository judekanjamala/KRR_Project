import argparse
import sys
from classes import PredicateTerm, VariableTerm


from xml_parsers import parse_KB, parse_query
from backward_chaining import solve_goals


sys.path.append("/home/jude/Mtech/Sem_2/KRR/Project/src")

parser = argparse.ArgumentParser()

parser.add_argument('-k', '--kb',
                     help='Uses clauses from this file to construct the KB',
                     required=True)

parser.add_argument('-q', '--query',
                     help='Query is taken from this file',
                     required=True)

args = parser.parse_args()


def main():
    '''
    Driver function converts xml data into kb, query objects. Runs backward reasoning to answer query and outputs the result.
    '''
    
    kb = parse_KB(args.kb)
    # for key, val in kb.items():
    #     print(repr(key),":")
    #     for v in val:
    #         print("\t", repr(v))
        
    #     print("\n")

    print("FINISHED PARSING KB")

    query = parse_query(args.query)
    print("FINISHED PARSING QUERY")



    print("Query:")
    for goal in query:
        print(goal)

    print("\n")

    kb = add_builtin_predicates(kb)

    print(solve_goals(kb, query))


def add_builtin_predicates(kb):
    '''
    Add clauses defining eq predicate to the kb.

    Args:
    1. kb: a dictionary of clauses (head, body).

    Returns:
    1. kb: 
    '''

    num_clauses = len(kb)

    num_clauses += 1

    # Adding clause for eq predicate
    arg = VariableTerm(name='X', clause=num_clauses)
    head = PredicateTerm(name="eq", args=[arg, arg])
    kb[head] = []

    return kb



if __name__ == "__main__":
    main()