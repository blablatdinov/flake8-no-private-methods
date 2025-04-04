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

# flake8: noqa: S . Not a production code

import os
import subprocess
from collections.abc import Generator
from pathlib import Path
from shutil import copy2

import pytest
from _pytest.legacypath import TempdirFactory


@pytest.fixture(scope='module')
def current_dir() -> Path:
    return Path().absolute()


@pytest.fixture(scope='module')
def _test_dir(tmpdir_factory: TempdirFactory, current_dir: str) -> Generator[None, None, None]:
    tmp_path = tmpdir_factory.mktemp('test')
    copy2(Path('tests/fixtures/file.py.txt'), tmp_path / 'file.py')
    os.chdir(tmp_path)
    subprocess.run(['python', '-m', 'venv', 'venv'], check=True)
    subprocess.run(['venv/bin/pip', 'install', 'pip', '-U'], check=True)
    subprocess.run(['venv/bin/pip', 'install', str(current_dir)], check=True)
    yield
    os.chdir(current_dir)


@pytest.mark.usefixtures('_test_dir')
@pytest.mark.parametrize('version', [
    ('flake8==5.0.0',),
    ('flake8', '-U'),
])
def test_dependency_versions(version: tuple[str]) -> None:
    """Test script with different dependency versions."""
    subprocess.run(['venv/bin/pip', 'install', *version], check=True)
    got = subprocess.run(
        ['venv/bin/flake8', 'file.py', '--max-line-length=120'],
        stdout=subprocess.PIPE,
        check=False,
    )

    assert got.stdout.decode('utf-8').strip().splitlines() == [
       'file.py:29:5: NPM100 private methods forbidden',
       'file.py:33:5: NPM100 private methods forbidden',
    ]
    assert got.returncode == 1


@pytest.mark.usefixtures('_test_dir')
def test() -> None:
    """Test script."""
    got = subprocess.run(
        ['venv/bin/flake8', 'file.py', '--max-line-length=120'],
        stdout=subprocess.PIPE,
        check=False,
    )

    assert got.returncode == 1
    assert got.stdout.decode('utf-8').strip().splitlines() == [
       'file.py:29:5: NPM100 private methods forbidden',
       'file.py:33:5: NPM100 private methods forbidden',
    ]
