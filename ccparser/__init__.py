"""
CCParser - Credit Card Parsing & Validation Library.

A robust Python library for parsing, validating, and formatting credit card data.

Example:
    >>> from ccparser import CCParser
    >>> card = CCParser("4111111111111111|12|2030|123")
    >>> card.get_card_type()
    'Visa'
    >>> card.is_valid()
    True
"""

from .parser import (
    CCParser,
    CCParserError,
    InvalidCardNumberError,
    InvalidExpiryDateError,
    InvalidCVVError,
)
from .generator import generate_card_number
from .validator import validate_card_number, validate_expiry_date, validate_cvv
from .formatter import format_card_number, mask_card_number
from .utils import detect_card_type, get_card_details

__version__ = "1.0.0"
__author__ = "Vihanga Indusara"
__email__ = "vihangadev@gmail.com"

__all__ = [
    # Main class
    "CCParser",
    # Exceptions
    "CCParserError",
    "InvalidCardNumberError",
    "InvalidExpiryDateError",
    "InvalidCVVError",
    # Generator
    "generate_card_number",
    # Validators
    "validate_card_number",
    "validate_expiry_date",
    "validate_cvv",
    # Formatters
    "format_card_number",
    "mask_card_number",
    # Utilities
    "detect_card_type",
    "get_card_details",
]
