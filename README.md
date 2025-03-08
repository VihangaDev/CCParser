# CCParser - Powerful Credit Card Parsing & Validation Library

![PyPI](https://img.shields.io/pypi/v/ccparser)  
![License](https://img.shields.io/github/license/VihangaDev/CCParser)  
![Build Status](https://img.shields.io/github/actions/workflow/status/VihangaDev/CCParser/ci.yml)  

CCParser is a robust and efficient Python library designed for seamless credit card parsing, validation, and formatting. Whether you're extracting card details, validating numbers, or formatting them for display, CCParser makes the process effortless with its powerful features and intuitive API.

---

## 🚀 Features

- **🔍 Smart Extraction:** Extracts card number, expiry date (month/year), and CVV from a string.
- **📏 Standardized Formatting:** Converts card numbers into `xxxx xxxx xxxx xxxx` format.
- **✅ Luhn Validation:** Ensures card validity using the industry-standard Luhn algorithm.
- **🗓️ Expiry & CVV Checks:** Validates expiry date and CVV length based on card type.
- **💳 Card Type Detection:** Identifies major card providers (Visa, MasterCard, AMEX, etc.).
- **🔒 Masked Output Option:** Returns a masked format (`**** **** **** 5379`).
- **🔗 Multiple Delimiters:** Supports delimiters like `|`, `:`, and spaces.
- **📆 Flexible Expiry Handling:** Accepts expiry years in both `YYYY` and `YY` formats.
- **⚡ Easy-to-Use API:** Well-structured API for seamless integration.
- **🖥️ Command-Line Support:** Provides a CLI tool for quick parsing.
- **📖 Well-Documented:** Extensive Markdown documentation (`README.md`).
- **📦 PyPI Ready:** Structured for easy PyPI distribution.
- **🛠️ CI/CD Integration:** Uses GitHub Actions for automated testing.
<<<<<<< HEAD
=======
- **🆕 Card Number Generation:** Generate valid card numbers for testing purposes.
- **🆕 Additional Card Types:** Supports JCB, Diners Club, and UnionPay.
>>>>>>> 43067d2 (feat: Add support for additional card types, card number generation, and flexible expiry date formatting)

---

## 💳 Supported Card Types

CCParser recognizes and validates multiple card providers:

- **Visa:** `^4[0-9]{12}(?:[0-9]{3})?$`
- **MasterCard:** `^5[1-5][0-9]{14}$`
- **American Express (AMEX):** `^3[47][0-9]{13}$`
- **Discover:** `^6(?:011|5[0-9]{2})[0-9]{12}$`
- **JCB:** `^(?:2131|1800|35\d{3})\d{11}$`
- **Diners Club:** `^3(?:0[0-5]|[68][0-9])[0-9]{11}$`
- **UnionPay:** `^62[0-9]{14,17}$`

---

## 📥 Installation

Install CCParser using pip:

```bash
pip install ccparser
```

---

## 📝 Usage Examples

### Supported Card Formats

CCParser supports various card formats with different delimiters and expiry formats:

```
4111111111111111|12/30|123
4111111111111111|12|2030|123
4111111111111111|12|30|123
4111111111111111 12 2030 123
4111111111111111 12 30 123
4111111111111111:12:2030:123
4111111111111111:12:30:123
```

### Python API

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

<<<<<<< HEAD
### CLI Tool

=======
### Card Number Generation

```python
from ccparser.generator import generate_card_number

print(generate_card_number("Visa"))  # Generates a valid Visa card number
print(generate_card_number("MasterCard"))  # Generates a valid MasterCard number
```

### CLI Tool

>>>>>>> 43067d2 (feat: Add support for additional card types, card number generation, and flexible expiry date formatting)
CCParser can also be used via the command line:

```bash
ccparser "4111111111111111|12|2030|123"
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please review our [CONTRIBUTING](CONTRIBUTING.md) guidelines before submitting a pull request.

---

## 📚 Acknowledgements

- [Luhn Algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm)
- [Regular Expressions](https://docs.python.org/3/library/re.html)

---

## 📧 Contact

For any inquiries or issues, feel free to reach out:

📩 **Vihanga Indusara** - [vihangadev@gmail.com](mailto:vihangadev@gmail.com)

---

<<<<<<< HEAD
CCParser – Simplifying credit card parsing, one line at a time! 🚀
=======
CCParser – Simplifying credit card parsing, one line at a time! 🚀
>>>>>>> 43067d2 (feat: Add support for additional card types, card number generation, and flexible expiry date formatting)
