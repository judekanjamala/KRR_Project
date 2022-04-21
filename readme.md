# README

LOOK at notes for cut operator.

LOOK at text for not operator.

## Workflow

1. Place the input horn-clause text file inside *Input* folder.
2. At top project directory Run: `./run.sh Input/file-name`
3. The output XML file will be placed inside *Input* folder.
4. Similarly for the query text file.
5. Inside *src* folder, run: `python3 query_solver.py -k ../Input/HC-01.txt.xml -q ../Input/HC-01_query.xml`