# The MIT License (MIT).
#
# Copyright (c) 2024-2025 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
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

# flake8: noqa: WPS433

import ast
from typing import Callable

try:
    from typing import TypeAlias  # type: ignore [attr-defined, unused-ignore]
except ImportError:
    from typing_extensions import TypeAlias  # noqa: WPS440

import pytest

from flake8_no_private_methods.plugin import Plugin

_PLUGIN_RUN_T: TypeAlias = Callable[
    [str], list[tuple[int, int, str]],
]


@pytest.fixture
def plugin_run() -> _PLUGIN_RUN_T:
    """Fixture for easy run plugin."""
    def _plugin_run(code: str) -> list[tuple[int, int, str]]:  # noqa: WPS430
        """Plugin run result."""
        plugin = Plugin(ast.parse(code))
        res = []
        for viol in plugin.run():
            res.append((
                viol[0],
                viol[1],
                viol[2],
            ))
        return res
    return _plugin_run


@pytest.mark.parametrize('definition', [
    'def move(self, to_x: int, to_y: int):',
    'async def move(self, to_x: int, to_y: int):',
])
def test_valid(definition: str, plugin_run: _PLUGIN_RUN_T) -> None:
    """Test valid case."""
    got = plugin_run('\n'.join([
        'class Animal(object):',
        '',
        '    {0}'.format(definition),
        '        # Some logic for change coordinates',
        '        pass',
    ]))

    assert not got


@pytest.mark.parametrize('method_name', [
    'def _move',
    'def __move',
    'async def _move',
    'async def __move',
])
def test_invalid(method_name: str, plugin_run: _PLUGIN_RUN_T) -> None:
    """Test valid case."""
    got = plugin_run('\n'.join([
        'class Animal(object):',
        '',
        '    {0}(self, to_x: int, to_y: int):'.format(method_name),
        '        # Some logic for change coordinates',
        '        pass',
        '',
    ]))

    assert got == [
        (
            3,
            4,
            'NPM100 private methods forbidden',
        ),
    ]


@pytest.mark.parametrize('dunder_method', [
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
])
def test_dunder_methods(plugin_run: _PLUGIN_RUN_T, dunder_method: str) -> None:
    """Test valid case."""
    got = plugin_run('\n'.join([
        'class Animal(object):',
        '',
        '    def {0}(self):'.format(dunder_method),
        '        # Some logic for change coordinates',
        '        pass',
    ]))

    assert not got