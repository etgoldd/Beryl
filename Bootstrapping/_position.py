

class Position:
    def __init__(self, index, line, column, file_name, file_text):
        self.index = index
        self.line = line
        self.column = column
        self.file_name = file_name
        self.file_text = file_text

    def advance(self, current_char=None):
        self.index += 1
        self.column += 1

        if current_char == '\n':
            self.column = 0
            self.line += 1

    def go_back(self):
        self.index -= 1
        self.column -= 1

    def copy(self):
        return Position(index=self.index,
                        line=self.line,
                        column=self.column,
                        file_name=self.file_name,
                        file_text=self.file_text)
