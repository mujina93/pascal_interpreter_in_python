"""
Interpreter for arithmetic expressions. (i.e. calculator)
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
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos in an index into self.text
        # (starts from behind the first character)
        self.pos = -1
        # current token instance
        self.current_token = None
        # current read char
        self.current_char = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """
        Lexical analyzer (also known as 'scanner' or 'tokenizer')

        This method is responsible for breaking a sentence
        apart into tokens, One token at a time.
        """
        text = self.text

        """
        increase self.pos (the first time, self.pos is se to 0
        in this way)
        """
        self.pos += 1
        """
        is self.pos index past the end of the self.text?
        if so, then return EOF token, because there is no more
        input left to convert into tokens
        """
        if self.pos > len(text) - 1:
            return Token(EOF,None)
        """
        get a character at the positions self.pos and decide
        what token to create based on the single character
        """
        self.current_char = text[self.pos]

        """
        look for a valid token. Ignore whitespaces
        """
        while(True):
            """
            if a whitespace is parsed, ignore it and read on,
            until the lexer/scanner finds a non-whitespace character
            """
            if self.current_char == " ":
                self.pos += 1
                self.current_char = text[self.pos]
                continue
            # if not a whitespace, try to find one of the possible tokens
            """ IS IT A NUMBER? """
            token_value = self.look_for_number()
            """
            if the token is a number, then convert it to an integer,
            create an INTEGER token, and return it
            """
            if token_value is not None:
                return Token(INTEGER, int(token_value))
            """ IS IT AN OPERATION SIGN? """
            token_value = self.look_for_operation()
            """
            if it is an operation sign, return a Token of type SIGN,
            with value the sign character itself. Then return it.
            """
            if token_value is not None:
                return Token(SIGN, token_value)
            """
            if nothing valid was parsed (the read character is neither
            a digit nor an operation sign), raise an error
            """
            self.error()

    """
    scans the text starting from the current self.current_char,
    and looks for a number (that may be composed of more than one
    digit. One the whole number is read, the control is passed back
    to the get_next_token method)
    """
    def look_for_number(self):
        text = self.text
        # string representing the read number.
        # all the digits that are read are added to this string,
        # forming the number.
        # if no digit is found, than this token is not a number,
        # and therefore None is returned.
        number_token = ""
        # read the current_char. If it's a digit, add it to the number
        if self.current_char.isdigit():
            """ FIRST DIGIT """
            number_token += self.current_char
            # then, check if the number is more than 1 digit long:
            """ DIGITS FROM 2nd ONWARDS """
            # while there is a new digit to be read, read it and add it
            # next_char is initially set to the current_char, for simplicity
            if self.pos < len(text) - 1:
                # if the parser has reached the end of the string, there
                # are of course no more digits to be read. That's why we have
                # all this block inside the above 'if'.
                next_char = text[self.pos + 1]
                while(next_char.isdigit()):
                    # add the single digit to the number
                    number_token += next_char
                    """
                    if the next character is still a digit, we remain
                    in the while loop, and the digit is added. Otherwise,
                    the number that has been read so far is returned as
                    a whole token, and the controls returns to get_next_token
                    method, which will analyze this token for other possibilites
                    (if this is a whitespace, every control will fail, and the
                    whitespace will be ignored.)
                    NOTE: since we are in the loop because we know that the next
                    character was a digit. Therefore, in the following line,
                    self.current_char will ALWAYS be equal to a digit.
                    WHY do we do all of this? Because we want to respect the
                    convention that all the 'look_for_*' methods exit leaving
                    self.current_char pointed to the last character of the token
                    that they have found. Not the next one! The duty of advancing
                    self.current_char after all the 'look_for_*' methods are invoked
                    is left to the method get_next_token(). (The new advancement is
                    the line before the while loop in get_next_token).
                    """
                    self.current_char = next_char
                    # then parse the next character
                    self.pos +=1
                    next_char = text[self.pos + 1]
        # return a number if a number was found
        if number_token != "":
            return number_token
        else:
            return None
    """
    analogous to look_for_number(), this method reads the current
    character, trying to understand if this is an operation sign or
    not. If it is, return it as a token. Otherwise, return None.
    """
    def look_for_operation(self):
        # if an operation sign is found, return it, and that
        # will then be taken as value for the Token object
        operation_signs = ['+','-','*','/']
        if self.current_char in operation_signs:
            return self.current_char
        else:
            return None
    """
    use this function to check a token's type. Is it of the type
    you were expecting? if not, raise an error
    """
    def eat(self, token_type):
        """
        compare the current token type with the passed token
        type and if they match, then "eat" the current token
        and assign the next token to the self.current_token,
        otherwise raise an exception
        """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    """
    this method starts reading the expression that the client wrote.
    It reads it, character after character, expecting an expression
    of type INTEGER PLUS INTEGER (therefore, just 3 characters, with
    2 integers and a plus sign between. NO WHITESPACES ANYWHERE! THIS
    IS REALLY STRICT!)
    If the expression is correct, and no error was rised, the interpreter
    finally interprets the expression, returning the sum of the two integers.
    """
    def expr(self):
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

        """
        INTERPRETATION
        at this point INTEGER SIGN INTEGER sequence of tokens has
        been successfully found and the method can just return the
        result of adding two integers, thus effectively interpreting
        client input
        """
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
