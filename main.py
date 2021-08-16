import operator
import unittest
from typing import Dict, List

from lark import Lark, Transformer
from lark.lexer import Token


def interactive():
    """Interactive mode. Creates a REPL in the terminal."""
    # Set up parser
    parser = Lark.open("c_grammar.lark")
    transformer = TreeToC()

    print("Welcome to interactive mode. Type Ctrl+C to quit.")

    while True:
        try:
            user_input = input(">")
        except KeyboardInterrupt:
            break

        # Run
        try:
            tree = parser.parse(user_input)
            transformer.transform(tree)
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


class Variable:
    def __init__(self, type_, data) -> None:
        self.type = type_
        self.value = data

    def __str__(self) -> str:
        return f"var<{self.type}> = {self.value}"

    def __repr__(self) -> str:
        return f"Variable({self.type}, {self.value})"


#####################################
NULL = 0  # Constant
variables: Dict[str, Variable] = {}


class TreeToC(Transformer):
    def var_assign(self, s: List[Token]) -> None:
        print(">>> var_assign", s)
        var_name, assign_op, value, *_ = s
        # Update var_name with new value.
        if var_name in variables:
            variables[var_name].value = value
        else:
            print(f'Error: "{var_name}" undeclared.')

    def var_decl(self, s: List[Token]):
        print(">>> var_decl:", s)
        var_type, var_name, *_ = s
        if var_name in variables:
            print(f'Error: "{var_name}" previously declared.')
            return
        variables[var_name.value] = Variable(var_type.value, NULL)
        print(">>> New variables:", variables)
        return var_name

    def var_compound_decl_assign(self, s):
        print(">>> combo:", s)
        self.var_assign(s)

    def expression(self, s):
        print(">>> expression:", s)

        if len(s) == 1:
            (s,) = s  # Unpack s

            # Evaluate expression
            value = s.value
            if s.type == "SIGNED_INT":
                value = int(value)
            elif s.type == "SIGNED_NUMBER":
                value = float(value)

            return value  # To parent

        else:
            assert len(s) == 3
            lhs, op, rhs = s
            # lhs and rhs should be evaluated
            ops = {
                "+": operator.add,
                "-": operator.sub,
                "*": operator.mul,
                "/": operator.truediv,  # TODO find way to make c-style div
                "%": operator.mod,
                "==": operator.eq,
                "!=": operator.ne,
                "<": operator.lt,
                "<=": operator.le,
                ">=": operator.ge,
                ">": operator.gt,
                "|": operator.or_,  # Bitwise operator
                "&": operator.and_,
                "^": operator.xor,
                "<<": operator.lshift,
                ">>": operator.rshift,
                "&&": operator.and_,  # TODO not sure if correct
                "||": operator.or_,
            }
            result = ops[op.value](lhs, rhs)
            print("result:", result)
            return result


if __name__ == "__main__":
    # unittest.main()  # Run unit test cases
    interactive()
