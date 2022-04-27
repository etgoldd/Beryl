import _lexer


def run(file_name, text_param):
    lexer = _lexer.Lexer(text=text_param, file_name=file_name)
    tokens, throwable_ = lexer.make_tokens()

    return tokens, throwable_

while True:
    text = input("Beryl>")

    result, throwable = run("bootstrapper.py", text)

    if throwable:
        print(throwable)
    else:
        print(result)

