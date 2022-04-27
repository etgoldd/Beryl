import _lexer
import _parser

def run(file_name, text_param):
    lexer = _lexer.Lexer(text=text_param, file_name=file_name)
    tokens = lexer.make_tokens()
    lexer_throwableHandler = lexer.throwableHandler

    if not lexer_throwableHandler.is_empty():
        return [], lexer_throwableHandler

    parser = _parser.Parser(tokens)
    ast = parser.parse()

    return ast, parser.throwable_handler


while True:
    text = input("Beryl>")

    result, throwableHandler = run("bootstrapper.py", text)

    if not throwableHandler.is_empty():
        print(throwableHandler)
    else:
        print(result)

