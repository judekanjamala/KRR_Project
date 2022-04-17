import argparse
import sys


from xml_parsers import parse_KB, parse_query

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
    
    # kb = parse_KB(args.kb)
    # for key, val in kb.items():
    #     print(key,":")
    #     for v in val:
    #         print("\t", v)
        
    #     print("\n")

    query = parse_query(args.query)

    for goal in query:
        print(goal)


if __name__ == "__main__":
    main()