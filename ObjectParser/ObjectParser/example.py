from .parser import Parser

class Some:
    p: str = "World!"
    i: int = 0

def test():
    some: Some = Parser.load("test.yml", Some)
    print(some.p)