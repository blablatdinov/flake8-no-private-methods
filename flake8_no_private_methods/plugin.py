# The MIT License (MIT).
#
# Copyright (c) 2024 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

# flake8: noqa: WPS232

import ast
from collections.abc import Generator
from typing import Union, final


def node_problems(
    node: Union[ast.FunctionDef, ast.AsyncFunctionDef],
    dunder_methods: set[str],
) -> list[tuple[int, int]]:
    problems = []
    if node.name.startswith('_') and node.name not in dunder_methods:
        problems.append((node.lineno, node.col_offset))
    return problems


@final
class ClassVisitor(ast.NodeVisitor):
    """Class visitor for checking that all methods has override decorator."""

    def __init__(self) -> None:
        """Ctor."""
        self.problems: list[tuple[int, int]] = []
        self._dunder_methods = {
            '__init__',
            '__new__',
            '__del__',
            '__repr__',
            '__str__',
            '__bytes__',
            '__format__',
            '__lt__',
            '__le__',
            '__eq__',
            '__ne__',
            '__gt__',
            '__ge__',
            '__hash__',
            '__bool__',
            '__getattr__',
            '__getattribute__',
            '__setattr__',
            '__delattr__',
            '__dir__',
            '__get__',
            '__set__',
            '__delete__',
            '__init_subclass__',
            '__set_name__',
            '__instancecheck__',
            '__subclasscheck__',
            '__class_getitem__',
            '__call__',
            '__len__',
            '__length_hint__',
            '__getitem__',
            '__setitem__',
            '__delitem__',
            '__missing__',
            '__iter__',
            '__reversed__',
            '__contains__',
            '__add__',
            '__radd__',
            '__iadd__',
            '__sub__',
            '__mul__',
            '__matmul__',
            '__truediv__',
            '__floordiv__',
            '__mod__',
            '__divmod__',
            '__pow__',
            '__lshift__',
            '__rshift__',
            '__and__',
            '__xor__',
            '__or__',
            '__neg__',
            '__pos__',
            '__abs__',
            '__invert__',
            '__complex__',
            '__int__',
            '__float__',
            '__index__',
            '__round__',
            '__trunc__',
            '__floor__',
            '__ceil__',
            '__enter__',
            '__exit__',
            '__await__',
            '__aiter__',
            '__anext__',
            '__aenter__',
            '__aexit__',
        }

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit by classes."""
        self.problems.extend(node_problems(node, self._dunder_methods))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.problems.extend(node_problems(node, self._dunder_methods))
        self.generic_visit(node)


@final
class Plugin:
    """Flake8 plugin."""

    def __init__(self, tree: ast.AST) -> None:
        """Ctor."""
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type], None, None]:
        """Entry."""
        visitor = ClassVisitor()
        visitor.visit(self._tree)
        for line in visitor.problems:  # noqa: WPS526
            yield (line[0], line[1], 'NPM100 private methods forbidden', type(self))
