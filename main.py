import unittest
from lark import Lark


def interactive():
    """Interactive mode. Creates a REPL in the terminal."""
    # Set up parser
    parser = Lark.open("c_grammar.lark")
    print("Welcome to interactive mode. Type Ctrl+C to quit.")

    while True:
        try:
            user_input = input(">")
        except KeyboardInterrupt:
            break

        # Run
        try:
            tree = parser.parse(user_input)
        except Exception as e:
            print(e)

        else:
            # Print result
            print(tree.pretty())


class ParserTests(unittest.TestCase):
    """
    Run test.c file.
    Run this test with `python -m unittest main.py`
    """

    def setUp(self):
        self.parser = Lark.open("c_grammar.lark")

    def test_file(self):
        with open("test.c", "r") as f:
            lines = f.read()
        tree = self.parser.parse(lines)
        print(tree.pretty())


if __name__ == "__main__":
    # unittest.main()  # Run unit test cases
    interactive()
