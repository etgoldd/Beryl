import _throw
import _position
import time

"""
TOKENS
"""

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = "LPAREN"
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'

# Some tokens are very simple to find, no need to have an ugly if/else chain for them
SIMPLE_TOKEN_DICT = {'+': 'PLUS',
                     '-': 'MINUS',
                     '*': 'MUL',
                     '/': 'DIV',
                     '(': 'LPAREN',
                     ')': 'RPAREN'}


class Token:

    def __init__(self, type_, value=None, pos_start: _position.Position = None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'


"""
LEXER
"""

DIGITS = '0123456789'


class Lexer:

    def __init__(self, file_name, text):
        self.text = text
        self.pos = _position.Position(index=-1, line=0, column=-1, file_name=file_name, file_text=text)
        self.current_char = None
        self.throwableHandler = _throw.ThrowableHandler()

        self.line_len = len(text)
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < self.line_len else None

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            simple_token_type = SIMPLE_TOKEN_DICT.get(self.current_char)

            if self.current_char in ' \t':
                pass  # Not a placeholder, spaces and tabs are very common, better to check for them first
            elif simple_token_type is not None:
                tokens.append(Token(simple_token_type, pos_start=self.pos.copy()))
            elif self.current_char in DIGITS:
                token = self.make_number_token()
                tokens.append(token)

                if not self.throwableHandler.is_empty():
                    return []
            else:
                self.throwableHandler.add(_throw.IllegalCharException(char=self.current_char,
                                                                      position=self.pos.copy()))
                return []

            self.advance()
        tokens.append(Token(TT_EOF, pos_start=self.pos.copy()))
        return tokens

    def make_number_token(self):
        num_str = ''
        dot_count = 0
        digits_dot = DIGITS + '.'
        start_pos = self.pos

        while self.current_char is not None and self.current_char in digits_dot:
            if self.current_char == '.':
                dot_count += 1
            num_str += self.current_char
            self.advance()

        self.pos.go_back()

        if dot_count == 0:
            return Token(TT_INT, value=int(num_str), pos_start=start_pos.copy())
        elif dot_count == 1:
            return Token(TT_FLOAT, value=float(num_str), pos_start=start_pos.copy())
        else:
            self.throwableHandler.add(_throw.SyntaxError_(illegal_statement=num_str,
                                                          detail="\t Unexpected dot",
                                                          position=self.pos.copy()))
            return

