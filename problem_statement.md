# Problem-5: Backward Chaining

Implement a Prolog-like backward chaining system using a depth-first strategy.

1. Accept rules from a text file (as per the language specification) and convert them
   into XML.
2. Accept the goal from a similar file.
3. Show the final proof for the goal (if possible, graphically as a tree).
4. One should be able to opt for more than one solution on giving a goal.
5. Allow the use of Cut.
6. The algorithm should output either a substitution or FALSE, along with a trace in
   a text file.

## Example

Input:
input.txt -- XML Parser -- input.xml
query.txt -- XML Parser -- query.xml

Output:
The algorithm should output either a substitution or FALSE,
along with a trace in a text file.