import _position


class Throwable:

    def __init__(self, position,  throwable_name: str, details: str = ""):
        self.pos: _position.Position = position
        self.throwable_name = throwable_name
        self.details = details
        self.fatal = False  # TODO do something with this, or delete it

    def __repr__(self):
        string_rep = ""
        if self.fatal:
            string_rep += "Fatal: "
        string_rep += f"{self.throwable_name}: {self.details}"
        string_rep += f"\n \t In {self.pos.file_name}, line {self.pos.line}"
        return string_rep


class IllegalCharException(Throwable):
    def __init__(self, char, position):
        super().__init__(throwable_name='IllegalCharException',
                         details=f"Unrecognized character: '{char}'",
                         position=position)


class SyntaxError_(Throwable):
    def __init__(self, detail, position, illegal_statement=""):
        super().__init__(throwable_name='SyntaxError',
                         details=f"{detail}: {illegal_statement}",
                         position=position)


class ThrowableHandler:

    def __init__(self):
        self.throws: list[Throwable] = []

    def __repr__(self):
        str_rep = ''
        for throw in self.throws:
            str_rep += f'{throw.__repr__()} \n \n'
        return str_rep

    def add(self, throwable):
        self.throws.append(throwable)

    def is_empty(self):
        return len(self.throws) == 0
