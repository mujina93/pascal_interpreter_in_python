"""
Interpreter for arithmetic expressions. (i.e. calculator)
This version can handle expressions like:
* INTEGER SIGN INTEGER (with whitespaces in between)
* arbitrary chains of additions/subtractions (with whitespaces)
* arbitrary chains of multiplications/divisions (with whitespaces)
"""

# Types of tokens
INTEGER, SIGN, EOF = 'INTEGER', 'SIGN', 'EOF'

"""
class representing a token. In the calculator case, the tokens can
only be numbers, the operation signs ('+', '-','*','/') or 'EOF'
(denoting end of file).
Internally, the token is represented by a type (see types above)
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
Interpreter class. This class can read some text (simply initialize it
with the text, like Interpreter(mytext)) and interpret it, with .expr().
It will return the result.
"""
class Interpreter(object):
    """
    class variables
    """
    operation_signs = ['+','-','*','/']
    """
    constructor. Takes a string (the input text, to be parsed and
    interpreted)
    """
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos in an index into self.text
        # (starts from behind the first character)
        self.pos = 0
        # current token instance
        self.current_token = None
        # current read char (initialize by reading the first character)
        self.current_char = self.text[self.pos]
    """
    raises an error when parsing fails
    """
    def error(self):
        raise Exception('Error parsing input')
    """
    advance method. Advances the current character by one place.
    Returns None if it has reached the end of file (end of text)
    """
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    """
    method that reads on and gets the next token in the text.
    OUTPUT: It can return an integer token, a sign token, raise an
    exception if nothing was found, or it returns an EOF token if
    current_char is None (that means that EOF was reached).
    """
    def get_next_token(self):
        """
        Lexical analyzer (also known as 'scanner' or 'tokenizer')

        This method is responsible for breaking a sentence
        apart into tokens, One token at a time.
        """
        # look for a valid token (self.current_char is initially set
        # to the first character)
        while self.current_char is not None:
            # if a whitespace is encountered, skip all whitespaces
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            # if a digit is encountered, read all digits until the
            # end of the number, and return a token with that number.
            # After parse_integer(), current_char is set to the next
            # char after the number
            if self.current_char.isdigit():
                return Token(INTEGER, self.parse_integer())
            # if an operation sign is encountered, return a token
            # with it. After parse_sign(), current_char is set to
            # the next char after the sign.
            if self.current_char in self.operation_signs:
                return Token(SIGN, self.parse_sign())
            # if nothing was found, return parsing error
            self.error()
        # if current_char==None, then EOF was reached. Return the
        # appropriate token.
        return Token(EOF, None)

    """
    (this is like a parsing method for a token made of any number of
    consecutive whitespaces. The token is actually not returned, since
    it is not needed).
    skips all whitespaces found, and leave current_char pointing to
    the next non-whitespace character found
    """
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    """
    scans the text starting from the current self.current_char,
    and looks for a number (that may be composed of more than one
    digit). Once the whole number is read, the control is passed back
    to the get_next_token method. By the end of this method, current_char
    will point to the next character right after the number.
    """
    def parse_integer(self):
        # string representing the read integer number
        number = ""
        # while current_char is a digit...
        while self.current_char is not None and self.current_char.isdigit():
            # add the digit
            number += self.current_char
            # move current_char on by one step
            self.advance()
        # return the read number as an integer
        return int(number)
    """
    When this method is called, you already know that current_char is an
    operation sign. Therefore, this simply returns the current_char, and
    makes sure to self.advance() current_char thereafter (in order to
    respect the convention of having, by the end of a parse_* method,
    current_char pointing to the next character after the parsed token)
    """
    def parse_sign(self):
        # save the current char (containing the sign)
        sign = self.current_char
        # advance current_char
        self.advance()
        # return the sign
        return sign
    """
    use this function to check a token's type. Is it of the type
    you were expecting? if not, raise an error.
    AFTER THIS METHOD:
        current_token is set to the next_token
    """
    def eat(self, token_type, token_values=[]):
        """
        compare the current token type with the passed token
        type and if they match, then "eat" the current token
        and assign the next token to the self.current_token,
        otherwise raise an exception
        """
        if self.current_token.type == token_type:
            # just check for type
            # optionally, you can check for a range of values
            if not token_values or (self.current_token.value in token_values):
                self.current_token = self.get_next_token()
        else:
            self.error()

    """
    PARSER
    Try to parse and expression like INTEGER SIGN INTEGER, and compute it.
    After that, if there are more [SIGN INTEGER] couples, with SIGN = +/-
    read on and compute all the expression.
    Or, if there are more couples with * or / operations (and if the first
    operation sign was a * or /), compute the chain.
    """
    def expr(self):
        # try to parse and interpret a first expression of type
        # INTEGER SIGN INTEGER. Compute the result. After this,
        # current_token will be set on the next token.
        # op_type is '+' or '*', denoting an algebric sum or multiplication
        # (i.e. + or -, OR * or /)
        result, op_type = self.parse_ISI()
        term = Token(INTEGER, result)
        # if the first operation was an algebric sum, go on looking
        # for algebric sums. Otherwise, go on looking for algebric
        # multiplications.
        if op_type == '+':
            allowed_signs = ['+','-']
        elif op_type == '*':
            allowed_signs = ['*','/']
        else:
            raise Exception("Unexpected returned type in op_type")
        # if the next token is a sign, go on parsing, trying to
        # find an expression of type I S I S I S I ...
        # with sign plus or minus.
        while(not self.current_token.iseof()):
            op = self.current_token
            # check if the current token is a + or a -
            self.eat(SIGN,allowed_signs)
            # if the line above was ok, look for a number next
            right = self.current_token
            self.eat(INTEGER)
            # if everything was ok up to now, compute the partial result
            term = Token(INTEGER, self.compute_ISI(term,op,right))
        # if current_char was None, there is nothing more to read, return
        # the result
        return term.value

    """
    PARSER for INTEGER SIGN INTEGER
    this method starts reading the expression that the client wrote.
    It reads it, character after character, expecting an expression
    of type INTEGER PLUS INTEGER (therefore, just 3 characters, with
    2 integers and a plus sign between. NO WHITESPACES ANYWHERE! THIS
    IS REALLY STRICT!)
    If the expression is correct, and no error was rised, the interpreter
    finally interprets the expression, returning the sum of the two integers.
    """
    def parse_ISI(self):
        """
        expr -> INTEGER SIGN INTEGER
        set current token to the first token taken from the input
        """
        # gets the first meaningful character (the first number.
        # if there are whitespaces before, they are ignored, and the
        # number is returned.)
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left = self.current_token
        """
        eat the integer, i.e. checks if the first meaningful character
        is indeed an integer. Then, eat() calls get_next_token() again
        so that self.current_token becomes equal to the next meaningful
        character. Again, if there are whitespaces in between, they get
        ignored. Our hope is that the first non-whitespace character is
        an operation sign, so that the next evaluation with eat(SIGN)
        will be successfull.
        """
        self.eat(INTEGER)

        # we expect the current token to be an operation sign token
        op = self.current_token
        self.eat(SIGN)

        # we expect the current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)
        # after the above call, the self.current_token is set to EOF token

        # as additional logging information,
        # return '+' if the operation was an algebric sum (+ or -)
        # otherwise return '*' if the operation was an algebric multiplication (*, /)
        if op.value in ['+','-']:
            log = '+'
        elif op.value in ['*','/']:
            log = '*'
        else:
            log = None
            raise Exception("Unexpected operation sign")
        """
        INTERPRETATION: the expression was parsed. Now it is interpreted,
        and the operation is computed. The result is the returned.
        """
        return self.compute_ISI(left,op,right), log

    """
    return the result of the operation INTEGER SIGN INTEGER
    INPUT: integer token, sign token, integer token
    OUTPUT: integer (or float)
    """
    def compute_ISI(self,left,op,right):
        if(op.value == '+'):
            result = left.value + right.value
        elif(op.value == '-'):
            result = left.value - right.value
        elif(op.value == '*'):
            result = left.value * right.value
        elif(op.value == '/'):
            result = left.value / right.value
        return result
# END INTERPRETER CLASS

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
        # Constructs and Interpreter object
        # The inrepreter reads and store the written text
        interpreter = Interpreter(text)
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
