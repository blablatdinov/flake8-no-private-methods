# flake8-no-private-methods

[![test](https://github.com/blablatdinov/flake8-no-private-methods/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/blablatdinov/flake8-no-private-methods/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/flake8-no-private-methods.svg)](https://pypi.org/project/flake8-no-private-methods/)

`flake8-no-private-methods` is a Flake8 plugin that prohibits the use of private methods in Python code. The plugin is based on the object-oriented programming principle: **each private method is a candidate for a new class**.

[Each Private Static Method Is a Candidate for a New Class](https://www.yegor256.com/2017/02/07/private-method-is-new-class.html)

## Installation

Install flake8-no-private-methods via pip:

```bash
pip install flake8-no-private-methods
```

## Usage

To use flake8-no-private-methods, simply include it in your Flake8 configuration. Run Flake8 as usual, and the plugin will check for the presence of private methods in your code.

```bash
flake8 your_code_directory
```

## Example

### Problematic code

```python
class Token:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
    
    def encoded(self):
        return "key=" + self._encode(self.key) + "&secret=" + self._encode(self.secret)
    
    def _encode(self, text):  # Private method - violation!
        return URLEncoder.encode(text, "UTF-8")
```

Running flake8 will produce the following error:

```
your_file.py:8:4: NPM100 private methods forbidden
```

### Correct code

Instead of a private method, create a separate class:

```python
class Encoded:
    def __init__(self, raw):
        self.raw = raw
    
    def __str__(self):
        return URLEncoder.encode(self.raw, "UTF-8")

class Token:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
    
    def encoded(self):
        return "key=" + str(Encoded(self.key)) + "&secret=" + str(Encoded(self.secret))
```

## Rationale

Private methods in Python reduce code modularity, testability, and reusability. The main problems with private methods:

- **Not reusable**: private methods cannot be used in other classes
- **Not testable**: it's difficult to create unit tests for private methods
- **Violate single responsibility principle**: a class takes on too many responsibilities

The `flake8-no-private-methods` plugin encourages developers to create separate classes instead of private methods, which leads to:

- **Better modularity**: each class has a single responsibility
- **Improved testability**: each class can be tested independently
- **Enhanced reusability**: functionality can be used in different places
- **Cleaner design**: code becomes more object-oriented

As Yegor Bugayenko said: *"Each private method is a candidate for a new class"*.

## License

[MIT](https://github.com/blablatdinov/flake8-no-private-methods/blob/master/LICENSE)

## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [864a62ecb432655249d071e263ac51f053448659](https://github.com/wemake-services/wemake-python-package/tree/864a62ecb432655249d071e263ac51f053448659). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/864a62ecb432655249d071e263ac51f053448659...master) since then.

The plugin idea is based on [Yegor Bugayenko's article](https://www.yegor256.com/2017/02/07/private-method-is-new-class.html) about how each private method is a candidate for a new class.
