# flake8-no-private-methods

[![test](https://github.com/blablatdinov/flake8-no-private-methods/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/blablatdinov/flake8-no-private-methods/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/flake8-no-private-methods.svg)](https://pypi.org/project/flake8-no-private-methods/)

`flake8-no-private-methods` is a Flake8 plugin designed to enforce a coding standard where every method in a class must have the @override decorator. This ensures that all public methods implement their counterparts from an interface, promoting better design practices, easier mocking in unit tests, and simpler extension via decoration.

[Seven Virtues of a Good Object. Part 2](https://www.yegor256.com/2014/11/20/seven-virtues-of-good-object.html#2-he-works-by-contracts)

## Installation

You can install flake8-no-private-methods via pip:

```bash
pip install flake8-no-private-methods
```

## Usage

To use flake8-no-private-methods, simply include it in your Flake8 configuration. You can run Flake8 as usual, and the plugin will check for the presence of the @override decorator on each method.

```bash
flake8 your_code_directory
```

## Example

### Input code

```python
class MyClass:
    def _run(self):
        pass
```

Running flake8 will produce the following error:

```
your_file.py:2:4: NPM100 private methods forbidden
```

### Expected code

```python
class MyClass:
    def run(self):
        pass
```

## Rationale

Using private methods in Python can reduce the modularity and testability of your code. By enforcing the prohibition of private methods (methods with names starting with `_` or `__`), `flake8-no-private-methods` encourages developers to use public methods and cleaner, more modular designs.

## License

[MIT](https://github.com/blablatdinov/flake8-no-private-methods/blob/master/LICENSE)

## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [864a62ecb432655249d071e263ac51f053448659](https://github.com/wemake-services/wemake-python-package/tree/864a62ecb432655249d071e263ac51f053448659). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/864a62ecb432655249d071e263ac51f053448659...master) since then.
