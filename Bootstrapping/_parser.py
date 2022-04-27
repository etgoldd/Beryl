import _throw
import _lexer


class ValueNode:

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'


class NumNode(ValueNode):

    def __init__(self, token):
        super().__init__(token)


class BinOpNode:  # Binary Operator Node

    def __init__(self, left, token, right):
        self.token = token
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({self.left} {self.token} {self.right})'

# 1 + 2 * 3 + 4 + 5 * 6
# expr(expr(expr(trm(fctr(1)) trm(fctr(2) fctr(3))) trm(fctr(4))) trm(fctr(5) fctr(6))))


class Parser:

    def __init__(self, tokens):
        self.token_index = 0
        self.tokens = tokens
        self.throwable_handler = _throw.ThrowableHandler()
        self.current_token: _lexer.Token = tokens[self.token_index]

    def parse(self):
        expression = self.expression()
        if not self.throwable_handler.is_empty() and self.current_token.type != _lexer.TT_EOF:

        return self.expression()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]

    def factor(self):
        tok = self.current_token

        if tok.type in (_lexer.TT_INT, _lexer.TT_FLOAT):
            self.advance()
            return NumNode(tok)
        else:
            self.advance()
            self.throwable_handler.add(_throw.SyntaxError_(illegal_statement=f'{tok.value}',
                                                           detail=f"Expected int or float, got {tok.type} instead",
                                                           position=tok.pos_start))
            return NumNode(tok)

    def term(self):
        return self.bin_op((_lexer.TT_MUL, _lexer.TT_DIV), self.factor)

    def expression(self):
        return self.bin_op((_lexer.TT_PLUS, _lexer.TT_MINUS), self.term)

    def bin_op(self, op_tokens, method):
        left = method()

        while self.current_token in op_tokens:
            op_token = self.current_token
            right = method()
            self.advance()
            left = BinOpNode(left=left, token=op_token, right=right)

        return left

