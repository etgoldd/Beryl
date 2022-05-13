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


class UnaryOpNode:
    def __init__(self, token, node: ValueNode):
        self.token = token
        self.node = node

    def __repr__(self):
        return f'({self.token}->{self.node})'


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
        if self.throwable_handler.is_empty() and self.current_token.type != _lexer.TT_EOF:
            self.throwable_handler.add(_throw.SyntaxError_(illegal_statement=f'',
                                                           detail=f'Expected an operator, got {expression.token.type} instead',
                                                           position=expression.token.pos_start.copy()))
        return expression

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]

    def recede(self):
        self.token_index -= 1
        if self.token_index > 0:
            self.current_token = self.tokens[self.token_index]

    def factor(self):
        token = self.current_token
        self.advance()

        # Skipping over excess plus signs
        if token.type == _lexer.TT_PLUS:
            while self.current_token.type == _lexer.TT_PLUS:
                self.advance()
            return self.factor()

        if token.type == _lexer.TT_MINUS:
            if self.current_token.type == _lexer.TT_MINUS:
                self.advance()
                return self.factor()  # skip two minuses
            return UnaryOpNode(token=token, node=self.factor())
        elif token.type == _lexer.TT_LPAREN:
            expr = self.expression()
            if self.current_token.type == _lexer.TT_RPAREN:
                self.advance()
                return expr
            else:
                self.throwable_handler.add(_throw.SyntaxError_(illegal_statement=f'',
                                                               detail="Expected ')'",
                                                               position=token.pos_start.copy()))
        elif token.type in (_lexer.TT_INT, _lexer.TT_FLOAT):
            return NumNode(token)
        else:
            self.throwable_handler.add(_throw.SyntaxError_(illegal_statement=f'',
                                                           detail=f"Expected int or float, got {token.type} instead",
                                                           position=token.pos_start.copy()))
            return NumNode(token)

    def term(self):
        return self.bin_op((_lexer.TT_MUL, _lexer.TT_DIV), self.factor)

    def expression(self):
        return self.bin_op((_lexer.TT_PLUS, _lexer.TT_MINUS), self.term)

    def bin_op(self, op_tokens, method):
        left = method()

        while self.current_token.type in op_tokens:
            op_token = self.current_token
            self.advance()
            right = method()
            left = BinOpNode(left=left, token=op_token, right=right)

        return left
