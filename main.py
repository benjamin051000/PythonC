import unittest
from lark import Lark

class ParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = Lark.open('c_grammar.lark')

    def test_file(self):
        with open('test.c', 'r') as f:
            lines = f.read()
        tree = self.parser.parse(lines)
        print(tree.pretty())

if __name__ == '__main__':
    unittest.main()
