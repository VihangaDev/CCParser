# Changelog

All notable changes to CCParser will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-17

### Added

- **Disclaimer section** in README for legal compliance
- **Base exception class** `CCParserError` for better exception handling
- **New `validate()` method** that raises exceptions with detailed error messages
- **New `to_dict()` method** for easy serialization of card data
- **New `get_expiry_full()` method** returning MM/YYYY format
- **New `get_supported_card_types()` function** in generator module
- **`__repr__` and `__str__` methods** for CCParser class
- **Optional `seed` parameter** for reproducible card generation
- **CLI enhancements**:
  - `--masked` flag to show masked card number
  - `--json` flag for JSON output format
  - `--quiet` flag for silent validation (exit codes only)
  - `--version` flag to show version
  - Proper exit codes (0 for valid, 1 for invalid)
- **Comprehensive test suite** with 100+ test cases
- **Type hints** throughout the codebase
- **Docstrings** for all public functions and classes
- **pyproject.toml** with full project configuration

### Changed

- **`is_valid()` now returns `False`** instead of raising exceptions for validation failures
- **`requests` is now an optional dependency** - install with `pip install ccparser[api]`
- **Improved expiry date validation** - fixed December edge case bug
- **Improved month validation** - validates range 1-12
- **Improved card number formatting** - supports AMEX (4-6-5) and Diners Club (4-6-4) patterns
- **Improved masking** - supports all card lengths correctly
- **Improved error messages** - more descriptive and helpful
- **Updated CI/CD workflows** - now tests Python 3.10, 3.11, 3.12, 3.13
- **Minimum Python version** raised to 3.10 (for modern type hint syntax)

### Fixed

- **December expiry date bug** - month 12 was incorrectly validated
- **AMEX card formatting** - now uses correct 4-6-5 format
- **Diners Club card masking** - now shows correct masked format
- **Network error handling** - `get_card_details()` now handles timeouts and connection errors
- **Input validation** - rejects non-numeric card numbers and CVVs during parsing

### Removed

- **Redundant `python-package.yml` workflow** - consolidated into `publish.yml`

## [0.5.0] - Previous Release

### Added

- Support for additional card types: JCB, Diners Club, UnionPay
- Card number generation for testing purposes
- Flexible expiry date formatting (YY and YYYY)

### Fixed

- UTF-8 encoding issues

## [0.4.0] - Earlier Release

### Added

- Initial public release
- Credit card parsing from various string formats
- Luhn validation
- Card type detection (Visa, MasterCard, AMEX, Discover)
- CVV validation
- Card number formatting and masking
- CLI tool
- BIN lookup via external API
