# CCParser

CCParser is a Python library for credit card parsing, validation, and formatting.

## Features

- Extracts card number, expiry month, expiry year, and CVV.
- Formats the card number into a standard display format: `xxxx xxxx xxxx xxxx`.
- Uses the Luhn algorithm to check if a card number is valid.
- Validates expiry dates and CVV length based on card type.
- Detects card providers: Visa, MasterCard, AMEX, Discover, etc.
- Option to return a masked format: `**** **** **** 5379`.
- Accepts multiple delimiters like `|`, `:`, and spaces.
- Handles expiry years in YYYY or YY format.
- Provides an easy-to-use Python API.
- Can be used as a CLI tool for quick parsing.
- Includes pytest unit tests for all functions.
- Provides Markdown documentation (`README.md`).
- Structured for publishing on PyPI.
- Includes `setup.py` or `pyproject.toml` for easy installation.
- Uses GitHub Actions for CI/CD testing.

## Installation

```bash
pip install ccparser
```

## Example Usage

```python
from ccparser import CCParser

card = CCParser("4783400008389576|04|2027|744")
print(card.get_number())  # 4783400008389576
print(card.get_formatted_number())  # 4783 4000 0838 9576
print(card.get_expiry())  # 04/27
print(card.get_cvv())  # 744
print(card.is_valid())  # True
print(card.get_card_type())  # Visa
```

## Running Tests

```bash
pytest
```

## Building Package

```bash
python setup.py sdist bdist_wheel
```

## Publishing to PyPI

```bash
twine upload dist/*
```