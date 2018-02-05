# 4 - context-free-grammar parser
Uses explicitly the concept of a grammar, to implement a parser that can interpret any kind of expression with any operation sign. Correctly handles multiplications and divisions before summations.

Try with any kind of arithmetic expression (only integers and operations signs), like:
```
$ python3 calc4.py
calc> 17 + 25 + 4 / 4 * 5 - 0 /2*4+6*5-9
68.0
```
