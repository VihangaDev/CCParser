# CCParser

![PyPI](https://img.shields.io/pypi/v/ccparser)
![License](https://img.shields.io/github/license/VihangaDev/CCParser)
![Build Status](https://img.shields.io/github/actions/workflow/status/VihangaDev/CCParser/ci.yml)

CCParser is a powerful Python library designed for credit card parsing, validation, and formatting. It provides a comprehensive set of features to handle various credit card operations with ease.

## Features

- **Card Number Extraction**: Extracts card number, expiry month, expiry year, and CVV from a given string.
- **Standard Formatting**: Formats the card number into a standard display format: `xxxx xxxx xxxx xxxx`.
- **Luhn Algorithm Validation**: Uses the Luhn algorithm to check if a card number is valid.
- **Expiry Date and CVV Validation**: Validates expiry dates and CVV length based on card type.
- **Card Provider Detection**: Detects card providers such as Visa, MasterCard, AMEX, Discover, etc.
- **Masked Format Option**: Option to return a masked format: `**** **** **** 5379`.
- **Multiple Delimiters**: Accepts multiple delimiters like `|`, `:`, and spaces.
- **Flexible Expiry Year Handling**: Handles expiry years in YYYY or YY format.
- **Easy-to-Use API**: Provides an easy-to-use Python API.
- **CLI Tool**: Can be used as a CLI tool for quick parsing.
- **Unit Tests**: Includes pytest unit tests for all functions.
- **Markdown Documentation**: Provides comprehensive Markdown documentation (`README.md`).
- **PyPI Ready**: Structured for publishing on PyPI.
- **Easy Installation**: Includes `setup.py` or `pyproject.toml` for easy installation.
- **CI/CD Testing**: Uses GitHub Actions for CI/CD testing.
- **Get Expiry Year**: Retrieves the expiry year of the card.
- **Get Expiry Month**: Retrieves the expiry month of the card.
- **Get Card Details**: Fetches detailed information about the card from an external API.

## Supported Card Types

CCParser supports the following card types and formats:

- **Visa**: `^4[0-9]{12}(?:[0-9]{3})?$`
- **MasterCard**: `^5[1-5][0-9]{14}$`
- **American Express (AMEX)**: `^3[47][0-9]{13}$`
- **Discover**: `^6(?:011|5[0-9]{2})[0-9]{12}$`
- **JCB**: `^(?:2131|1800|35\d{3})\d{11}$`
- **Diners Club**: `^3(?:0[0-5]|[68][0-9])[0-9]{11}$`
- **UnionPay**: `^62[0-9]{14,17}$`

## Installation

Install CCParser using pip:

```bash
pip install ccparser
```

## Example Usage

Here's a quick example of how to use CCParser in your Python code:

```python
from ccparser import CCParser

card = CCParser("4111111111111111|12|2030|123")
print(card.get_number())  # 4111111111111111
print(card.get_formatted_number())  # 4111 1111 1111 1111
print(card.get_expiry())  # 12/30
print(card.get_cvv())  # 123
print(card.is_valid())  # True
print(card.get_card_type())  # Visa
print(card.get_masked_number())  # **** **** **** 1111
print(card.get_year())  # 2030
print(card.get_month())  # 12
print(card.get_card_details())  # Detailed card information
```

## CLI Usage

CCParser can also be used as a command-line tool:

```bash
ccparser "4111111111111111|12|2030|123"
```

## Running Tests

Run the unit tests using pytest:

```bash
pytest
```

## Building Package

Build the package using the following command:

```bash
python setup.py sdist bdist_wheel
```

## Publishing to PyPI

Publish the package to PyPI using Twine:

```bash
twine upload dist/*
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## Acknowledgements

- [Luhn Algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm)
- [Regular Expressions](https://docs.python.org/3/library/re.html)

## Contact

For any inquiries or issues, please contact [Vihanga Indusara](mailto:vihangadev@gmail.com).