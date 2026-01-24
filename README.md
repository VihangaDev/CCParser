# CCParser - Powerful Credit Card Parsing & Validation Library

![PyPI](https://img.shields.io/pypi/v/ccparser)  
![License](https://img.shields.io/github/license/VihangaDev/CCParser)  
![Build Status](https://img.shields.io/github/actions/workflow/status/VihangaDev/CCParser/ci.yml)  

CCParser is a robust and efficient Python library designed for seamless credit card parsing, validation, and formatting. It can extract card details from clean, delimited strings and messy real-world text while keeping a simple, consistent API.

---

## Features

- Smart extraction of card number, expiry date, and CVV from many formats
- Heuristic parser for messy input (labels, mixed delimiters, extra text)
- Parse-time CVV length validation (3 or 4 digits)
- Luhn validation and expiry validation helpers
- CVV validation with card-type awareness
- Card type detection across 20 major networks
- Formatting and masking helpers
- CLI for quick parsing and validation

---

## Disclaimer

This library is intended for educational and legitimate purposes only.

CCParser is designed to assist developers in:

- Building payment processing systems
- Testing and validating payment integrations
- Educational purposes and learning about payment card industry standards
- Fraud detection and prevention systems

Prohibited uses include:

- Unauthorized access to financial systems or data
- Credit card fraud, carding, or any form of financial crime
- Harvesting, storing, or processing stolen card information
- Any activity that violates applicable laws or regulations

By using this library, you agree to comply with all applicable laws, including but not limited to PCI-DSS standards, and take full responsibility for your use of this software. The author(s) are not responsible for any misuse or illegal activities conducted with this tool.

If you suspect fraudulent activity, please report it to your local authorities.

---

## Supported Card Types

CCParser recognizes and validates card networks including:

- AMEX
- Dankort
- Diners Club
- Discover
- Elo
- Humo
- InstaPayment
- InterPayment
- JCB
- LankaPay
- Maestro
- MasterCard
- Mir
- Troy
- UATP
- UnionPay
- UzCard
- Verve
- Visa
- Visa Electron

---

## Installation

```bash
pip install ccparser
```

---

## Usage Examples

### Supported Formats

CCParser supports a wide range of inputs, including:

```
4111111111111111|12/30|123
4111111111111111|12|2030|123
4111111111111111|12|30|123
4111111111111111 12 2030 123
4111111111111111 12 30 123
4111111111111111:12:2030:123
4111111111111111 2030/12 123
4111111111111111;12-30;123
4111 1111 1111 1111 12/30 123

CC #: 4111111111111111
Exp: 03/29
CVV: 123
```

### Python API

```python
from ccparser import CCParser

card = CCParser("4111111111111111|12|2030|123")
print(card.get_number())           # 4111111111111111
print(card.get_formatted_number()) # 4111 1111 1111 1111
print(card.get_expiry())           # 12/30
print(card.get_cvv())              # 123
print(card.is_valid())             # True
print(card.get_card_type())        # Visa
print(card.get_masked_number())    # **** **** **** 1111
print(card.get_year())             # 2030
print(card.get_month())            # 12
```

### Card Number Generation

```python
from ccparser.generator import generate_card_number

print(generate_card_number("Visa"))
print(generate_card_number("MasterCard"))
```

### CLI

```bash
ccparser "4111111111111111|12|2030|123"
ccparser --masked "4111111111111111|12|2030|123"
ccparser --json "4111111111111111|12|2030|123"
```

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Contributing

Contributions are welcome! Please review our CONTRIBUTING.md guidelines before submitting a pull request.

---

## Acknowledgements

- Luhn Algorithm
- Python regular expressions

---

## Contact

For any inquiries or issues, feel free to reach out:

Vihanga Indusara - vihangadev@gmail.com

---

CCParser - Simplifying credit card parsing, one line at a time.
