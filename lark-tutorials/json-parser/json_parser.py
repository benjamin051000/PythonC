"""
    json_parser.py

    Loosely follows tutorial from
    https://lark-parser.readthedocs.io/en/latest/json_tutorial.html,
    with added comments.
"""
from lark import Lark, Transformer

with open("./grammar.lark", "r") as f:
    grammar = f.read()

# The tree transformer has functions with names that match
# Grammar rules defined in the grammar file.
# These functions convert the data from the lexer
# Into useable data/proper types in Python.
class TreeToJSON(Transformer):
    def string(self, s):
        # s is list of one element. Unpack it.
        (s,) = s  # Shorthand for s = s[0]
        return s.strip('"')

    def number(self, n):
        (n,) = n
        return float(n)

    # Shorthand for def list(self, l): return list(l)
    list = list
    pair = tuple
    dict = dict

    # Shorthand for def null(self, _): return None
    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False

# Create parser
json_parser = Lark(grammar, start="value", parser="lalr", transformer=TreeToJSON())

# Test text (could be read from a file or stdin)
text = '{"key": ["item0", "item1", 3.14, true], "a": null}'

# Parse the text.
json_obj = json_parser.parse(text)

print(json_obj)

# Some tests to prove the parser actually generated Python objects.
assert type(json_obj) == dict
assert type(json_obj['key']) == list
print('All tests passed.')
