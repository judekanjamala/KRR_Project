import argparse
import sys


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
    
    kb = parse_KB(args.kb)
    # for key, val in kb.items():
    #     print(key,":")
    #     for v in val:
    #         print("\t", v)
        
    #     print("\n")

    print("FINISHED PARSING KB")

    query = parse_query(args.query)
    print("FINISHED PARSING QUERY")

    print("Query:")
    for goal in query:
        print(goal)

    print("\n")

    print(solve_goals(kb, query))


if __name__ == "__main__":
    main()