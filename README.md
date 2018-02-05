# Pascal Interpreter written in Python
Implementation of the exercises suggested by the series of articles: [Let's Build a Simple Interpreter](https://ruslanspivak.com/lsbasi-part1/)
Each directory contains an upgraded version of an interpreter. These programs allow you to write code in the shell that is then parsed and interpreted.


See the README in each directory for precise instructions on how to use each interpreter.

# 1 - arithmetic expressions interpreter (calculator)
Handles binary operations (with whitespaces between)

# 2 - extended calculator
Handles binary operations (any operator) and repeated operations (only with + and -)

# 3 - extended calculator (sums and multiplications)
Handles binary operations, and repeated operations (only with consistent operations, i.e. all algebric sums or all algebric multiplications)

# 4 - context-free-grammar parser
Uses explicitly the concept of a grammar, to implement a parser that can interpret any kind of expression with any operation sign. Correctly handles multiplications and divisions before summations.

# 5 - parenthesis parser
Handles arithmetic expressions with parentheses, using additional recursion in the grammar definition.
