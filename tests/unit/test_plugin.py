# SPDX-FileCopyrightText: Copyright (c) 2024-2026 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
# SPDX-License-Identifier: MIT

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
    '__abs__',
    '__add__',
    '__aenter__',
    '__aexit__',
    '__aiter__',
    '__and__',
    '__anext__',
    '__annotate__',
    '__annotations__',
    '__await__',
    '__base__',
    '__bases__',
    '__bool__',
    '__buffer__',
    '__builtins__',
    '__bytes__',
    '__cached__',
    '__call__',
    '__ceil__',
    '__class__',
    '__class_getitem__',
    '__classcell__',
    '__closure__',
    '__code__',
    '__complex__',
    '__contains__',
    '__defaults__',
    '__del__',
    '__delattr__',
    '__delete__',
    '__delitem__',
    '__dict__',
    '__dir__',
    '__divmod__',
    '__doc__',
    '__enter__',
    '__eq__',
    '__exit__',
    '__file__',
    '__firstlineno__',
    '__float__',
    '__floor__',
    '__floordiv__',
    '__format__',
    '__fspath__',
    '__func__',
    '__future__',
    '__ge__',
    '__get__',
    '__getattr__',
    '__getattribute__',
    '__getitem__',
    '__globals__',
    '__gt__',
    '__hash__',
    '__iadd__',
    '__iand__',
    '__ifloordiv__',
    '__ilshift__',
    '__imatmul__',
    '__imod__',
    '__import__',
    '__imul__',
    '__index__',
    '__init__',
    '__init_subclass__',
    '__instancecheck__',
    '__int__',
    '__invert__',
    '__ior__',
    '__ipow__',
    '__irshift__',
    '__isub__',
    '__iter__',
    '__itruediv__',
    '__ixor__',
    '__kwdefaults__',
    '__le__',
    '__len__',
    '__length_hint__',
    '__loader__',
    '__lshift__',
    '__lt__',
    '__main__',
    '__match_args__',
    '__matmul__',
    '__missing__',
    '__mod__',
    '__module__',
    '__mro__',
    '__mro_entries__',
    '__mul__',
    '__name__',
    '__ne__',
    '__neg__',
    '__new__',
    '__next__',
    '__objclass__',
    '__or__',
    '__package__',
    '__path__',
    '__pos__',
    '__pow__',
    '__prepare__',
    '__qualname__',
    '__radd__',
    '__rand__',
    '__rdivmod__',
    '__release_buffer__',
    '__repr__',
    '__reversed__',
    '__rfloordiv__',
    '__rlshift__',
    '__rmatmul__',
    '__rmod__',
    '__rmul__',
    '__ror__',
    '__round__',
    '__rpow__',
    '__rrshift__',
    '__rshift__',
    '__rsub__',
    '__rtruediv__',
    '__rxor__',
    '__self__',
    '__set__',
    '__set_name__',
    '__setattr__',
    '__setitem__',
    '__slots__',
    '__spec__',
    '__static_attributes__',
    '__str__',
    '__sub__',
    '__subclasscheck__',
    '__subclasses__',
    '__traceback__',
    '__truediv__',
    '__trunc__',
    '__type_params__',
    '__weakref__',
    '__xor__',
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
