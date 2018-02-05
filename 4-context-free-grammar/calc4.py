"""
Interpreter for arithmetic expressions. (i.e. calculator)
This version can handle arithmetic expressions, from grammar:
m_expr: factor ((*|/) factor)*
expr: m_expr ((+|-) factor)*
factor: INTEGER
"""

# Types of tokens:
# numbers, summation signs (+,-), multiplication signs (*,/), EOF
INTEGER, S_SIGN, M_SIGN, EOF = 'INTEGER', '+|-', '*|/', 'EOF'

"""
class representing a token.
Internally, the token is represented by a type (see above)
and a value (the specific number, or the specific symbol, or None)
"""
class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, ..., 9, '+',..., '/', None
        self.value = value
    """
    checks whether this token is of type EOF or not
    """
    def iseof(self):
        return self.type == EOF
    """
    str represents the object in readable way, as a user
    would want to read it
    """
    def __str__(self):
        """
        string representation of the class instance
        Examples:
            Token(INTEGER, 3)
            Token(SIGN, '+')
        """
        return 'Token({type}, {value})'.format(
            type = self.type,
            value = repr(self.value)
        )
    """
    implement __repr__ for any class you implement. The goal is
    to give an unambiguous description (not necessarily readable or
    verbose, or user-friendly).
    If __str__ is not implemented, it deafults to __repr__. That's why
    repr has higher priority.
    In a container (for example, a list of Tokens in this case), the
    representation of the container's elements makes use of __repr__
    and not __str__.
    The aim of __repr__ is also that of giving meaningful loggin information
    """
    def __repr__(self):
        return self.__str__()

"""
Lexer (or scanner), class that reads the input, and is able to
recognize and parse and get tokens, ignoring whitespaces.
"""
class Lexer(object):
    summation_signs = ['+','-']
    multiplication_signs = ['*','/']
    def __init__(self, text):
        # client string input
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    def error(self):
        raise Exception("Invalid character")
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    # parse all whitespaces until you find a non-whitespace
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    # parse all consecutive digits until a non-digit is found
    def parse_integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    # parse the current sign and return it
    def parse_sign(self):
        sign = self.current_char
        self.advance()
        return sign
    """
    method that reads on and gets the next token in the text.
    OUTPUT: It can return an integer token, a sign token, raise an
    exception if nothing was found, or it returns an EOF token if
    current_char is None (that means that EOF was reached).
    """
    def get_next_token(self):
        # LEXER
        while self.current_char is not None:
            # skip whitespaces until it encounters a non-whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            # if it finds a digit, read all digits and store an integer
            if self.current_char.isdigit():
                return Token(INTEGER, self.parse_integer())
            # sum or difference
            if self.current_char in self.summation_signs:
                return Token(S_SIGN, self.parse_sign())
            # multiplication or division
            if self.current_char in self.multiplication_signs:
                return Token(M_SIGN, self.parse_sign())
            # parsing error if no known token was found
            self.error()
        # end of file reached if current_char is None
        return Token(EOF, None)
# END LEXER

"""
Interpreter. Takes tokens from lexer, and is able to 'eat' them (
type-check them, move forward by getting the next tokens, and
interpret the whole sentence)
"""
class Interpreter(object):
    def __init__(self,lexer):
        self.lexer = lexer
        # initialize token to first token
        self.current_token = self.lexer.get_next_token()
    # Syntax error - error in the interpretation
    def error(self):
        raise Exception("Invalid syntax")
    # check for validity of token (optionally checks for a custom
    # range of values), and if the test passes, get next token
    def eat(self, token_type, token_values=[]):
        if self.current_token.type == token_type:
            # just check for type. Optionally, you can check for a range of values
            if not token_values or (self.current_token.value in token_values):
                self.current_token = self.lexer.get_next_token()
        else:
            # raise syntax error
            self.error()
    """
    method referring to 'factor' word in grammar (see at the beginning)
    factor : INTEGER
    OUTPUT: an INTEGER token
    """
    def factor(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value
    """
    method referring to 'm_expr' in the grammar (multiplication expression)
    m_expr: factor (M_SIGN factor)*
    OUTPUT: a number with the result of the chain of multiplications/divisions
    """
    def m_expr(self):
        # first 'factor' term in the 'expr' definition
        result = self.factor()
        # go on with the chain
        while self.current_token.type == M_SIGN:
            token = self.current_token
            self.eat(M_SIGN)
            if token.value == '*':
                result = result * self.factor()
            elif token.value == '/':
                result = result / self.factor()
        # returns the result of the expression
        return result
    """
    method for 'expr' in the grammar (summations chain of m_expressions)
    expr: m_expr (S_SIGM m_expr)*
    OUTPUT: an number with the result of the chain
    """
    def expr(self):
        # read and compute the first multiplicative expression
        # (the first chain of multiplications / divisions)
        # (it could also be a single number)
        result = self.m_expr()
        # go on with the chain (we want summations signs that
        # separate the various m_expressions)
        while self.current_token.type == S_SIGN:
            # eat the summation sign
            token = self.current_token
            self.eat(S_SIGN)
            if token.value == '+':
                # call m_expr() which reads and compute the
                # next chain of multiplications/divisions (it
                # could also be a single number) and add it to
                # the current result
                result = result + self.m_expr()
            elif token.value == '-':
                result = result - self.m_expr()
        # return the final result afterwards
        return result
# END INTERPRETER

# main loop function
def main():
    while True:
        try:
            # waits for an input text from the client
            text = input('calc> ')
        except EOFError:
            break
        # if the text is not valid, prompt again a 'calc> '
        # and wait for an input text
        if not text:
            continue
        # Constructs and Lexer object
        # The Lexer reads and store the written text
        lexer = Lexer(text)
        # Construct the interpreter object.
        # The interpreter parses each token, and is coded to
        # recognize a certain grammar (see the structure at
        # the beginning of the file)
        interpreter = Interpreter(lexer)
        # parse and interpret the expression
        result = interpreter.expr()
        # give the result (if any)
        print(result)

if __name__ == '__main__':
    """
    if you are directly running this module,
    fire up the 'calc> ' interpreter. Otherwise, this is
    just a module containing the class definition for the
    calculator Interpreter
    """
    main()
