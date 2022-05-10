import argparse
import sys
from classes import PredicateTerm, VariableTerm

from xml_parsers import parse_KB, parse_query
from query_solver import solve_goals
from utils import trace_file

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

    print("FINISHED PARSING KB", file=trace_file)

    query = parse_query(args.query)
    print("FINISHED PARSING QUERY", file=trace_file)



    s = ("Query:\n")
    for goal in query:
        s += str(goal) + "\n"


    cuts = 0
    for g in query:
        if g.name == "cut":
            cuts = 1

    print(f"{s}\n", file=trace_file)
    print(f"{s}\n")

    kb = add_builtin_predicates(kb)

    result = solve_goals(kb, query, cuts=cuts)
    print(result)
    print(result, file=trace_file)


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

trace_file.close()