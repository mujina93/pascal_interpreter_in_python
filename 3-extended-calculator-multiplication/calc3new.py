"""
Interpreter for arithmetic expressions. (i.e. calculator)
This version can handle expressions like:
* INTEGER SIGN INTEGER (with whitespaces in between)
* arbitrary chains of additions/subtractions (with whitespaces)
* arbitrary chains of multiplications/divisions (with whitespaces)
"""


class Character:
    pass


EOF = Character()


# Types of tokens
import types
token_types_names = ['INTEGER','ALG_SUM_SIGN','ALG_MUL_SIGN','EOF']
token_types = types.SimpleNamespace(**{k: k for k in token_types_names})
# token_types can be accessed like a namespace or an object or an enum.
# e.g. token_types.INTEGER is the type of the INTEGER token


class Token:
    """
    a.k.a. Terminal (= leaf in ast)
    """
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
                return Token(token_types.INTEGER, self.parse_integer_token_value())
            elif self.current_char in self.alg_sum_signs:
                return Token(token_types.ALG_SUM_SIGN, self.parse_alg_sum_sign_token_value())
            elif self.current_char in self.alg_mul_signs:
                return Token(token_types.ALG_MUL_SIGN, self.parse_alg_mul_sign_token_value())
            else:
                self.lexing_error()
        return Token(token_types.EOF, None)

    def skip_whitespace(self):
        while self.current_char is not EOF and self.current_char.isspace():
            self.advance()

    def parse_integer_token_value(self):
        number = ""
        while self.current_char is not EOF and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        if number == "": self.lexing_error()
        return int(number)

    def parse_alg_sum_sign_token_value(self):
        sign = self.current_char
        self.advance()
        return sign

    def parse_alg_mul_sign_token_value(self):
        sign = self.current_char
        self.advance()
        return sign

    def __iter__(self):
        """
        Iterator interface.
        Usage:
            for token in Lexer(text):
                print(token) # Does NOT output EOF token at the end
        :return:
        """
        while True:
            token = self.get_next_token()
            if token.type == token_types.EOF:
                return
            else:
                yield token


class NonTerminal:
    """
    General node in ast
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

    # TODO implement this as a generic node with arbitrary amount of children



class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        # self.current_token = self.lexer.get_next_token() # get 1st in init
        self.tokens = [token for token in self.lexer]

    def parsing_error(self, msg):
        if not msg:
            raise Exception(
                f"Error parsing input.\n"
                f"Token {self.current_token}\n")
                # TODO add some context
        else:
            raise Exception(msg)

    def advance_parser(self, token_type):
        """
        # TODO probably this function is not needed
        Advance parser
        :return:
        """
        if self.current_token is None:
            self.parsing_error(f"Parsing error. self.current_token is still uninitialized.")

        ## Check token type
        if self.current_token.type == token_type:
            ## Advances token to next
            self.current_token = self.lexer.get_next_token()
        else:
            self.parsing_error()

    def parse_expression(self):
        """
        Parse expression of type sexpr ("sum expression")
        with:
            sexpr : mexpr (alg_sum_sign mexpr)*
            alg_sum_sign: + | -
            mexpr : term (alg_mul_sign term)*
            alg_mul_sign: * | /
            term: integer : nonzerodigit (digit)*
        :return:
        """
        ast = self.parse_sexpr(self.tokens)
        return ast

    def parse_sexpr(self, tokens):
       """
       Parse sexpr:
            sexpr : mexpr (alg_sum_sign mexpr)*
       :param tokens:
       :return:
       """


class Interpreter:
    pass


def test_lexer():
    with open('sample.txt', 'r') as f:
        text = f.read()
    print("Sample is")
    print(text)
    l = Lexer(text)
    print("Lexing:")
    while True:
        token = l.get_next_token()
        print(token)
        if token.type == token_types.EOF: break

def test_lexer_iter():
    with open('sample.txt', 'r') as f:
        text = f.read()
    print("Sample is")
    print(text)
    l = Lexer(text)
    print("Lexing:")
    for token in l:
        print(token)

if __name__ == '__main__':
    # test_lexer()
    test_lexer_iter()
    # # REPL
    # while True:
    #     try:
    #         text = input('calc> ')
    #     except EOFError:
    #         break
    #     if not text: continue
    #     lexer = Lexer(text)
    #     parser = Parser(lexer)
    #     result = Interpreter(parser)
    #     print(result)