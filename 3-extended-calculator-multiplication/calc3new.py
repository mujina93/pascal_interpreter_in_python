"""
Interpreter for arithmetic expressions. (i.e. calculator)
This version can handle expressions like:
* INTEGER SIGN INTEGER (with whitespaces in between)
* arbitrary chains of additions/subtractions (with whitespaces)
* arbitrary chains of multiplications/divisions (with whitespaces)
"""

# Types of tokens
import types
token_types_names = ['INTEGER','ALG_SUM_SIGN','ALG_MUL_SIGN','EOF']
token_types = types.SimpleNamespace(**{k:k for k in token_types_names})
# token_types can be accessed like a namespace or an object or an enum.
# e.g. token_types.INTEGER is the type of the INTEGER token

class Character:
    pass
EOF = Character()

class Token:
    def __init__(self, type, value):
        # token type e.g. token_types.INTEGER
        self.type = type
        # token value: 0, 1, ..., 9, '+',..., '/', None
        self.value = value

    def iseof(self):
        return self.type == token_types.EOF

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'


class Lexer:
    alg_sum_signs = ['+','-']
    alg_mul_signs = ['*','/']

    def __init__(self, text):
        self.text = text
        self.last_idx = len(self.text) - 1
        self.pos = 0
        self.current_char = self.text[self.pos]

    def lexing_error(self):
        raise Exception(f"Error lexing input. Position {self.pos}.\n"
                        f"Character {self.current_char} in context:\n"
                        f"{self.text[min(self.pos-10,0):max(self.pos+10,self.last_idx)]}")

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos <= self.last_idx else EOF

    def get_next_token(self):
        while self.current_char is not EOF:
            if self.current_char.isspace():
                self.skip_whitespace()
            elif self.current_char.isdigit():
                return Token(token_types.INTEGER, self.parse_integer())
            elif self.current_char in self.alg_sum_signs:
                return Token(token_types.ALG_SUM_SIGN, self.parse_alg_sum_sign_atom())
            elif self.current_char in self.alg_mul_signs:
                return Token(token_types.ALG_MUL_SIGN, self.parse_alg_mul_sign_atom())
            else:
                self.lexing_error()
        return Token(token_types.EOF, None)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def parse_integer_atom(self):

    def parse_alg_sum_sign_atom(self):

    def parse_alg_mul_sign_atom(self):


class Parser:
    def eat_token(self):

    def parse_expression(self):


class Interpreter:
    pass

if __name__ == '__main__':
    # REPL
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text: continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        result = Interpreter(parser)
        print(result)