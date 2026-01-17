"""
Credit card parsing module.

This module provides the main CCParser class for parsing, validating,
and extracting credit card information from strings.
"""

import re
from typing import Optional

from .validator import validate_card_number, validate_expiry_date, validate_cvv
from .formatter import format_card_number, mask_card_number
from .utils import detect_card_type, get_card_details


class CCParserError(Exception):
    """Base exception for all CCParser errors."""
    pass


class InvalidCardNumberError(CCParserError):
    """Raised when a card number is invalid or malformed."""
    pass


class InvalidExpiryDateError(CCParserError):
    """Raised when an expiry date is invalid or malformed."""
    pass


class InvalidCVVError(CCParserError):
    """Raised when a CVV is invalid or malformed."""
    pass


class CCParser:
    """
    Parse and validate credit card strings.

    The CCParser class extracts card details from various string formats
    and provides methods for validation, formatting, and card type detection.

    Supported formats:
        - 4111111111111111|12/30|123
        - 4111111111111111|12|2030|123
        - 4111111111111111|12|30|123
        - 4111111111111111 12 2030 123
        - 4111111111111111:12:2030:123

    Attributes:
        card_number: The extracted card number.
        expiry_month: The expiry month (01-12).
        expiry_year: The expiry year (YYYY format).
        cvv: The CVV/CVC code.

    Example:
        >>> card = CCParser("4111111111111111|12|2030|123")
        >>> card.get_number()
        '4111111111111111'
        >>> card.get_card_type()
        'Visa'
        >>> card.is_valid()
        True
    """

    def __init__(self, card_string: str):
        """
        Initialize CCParser with a card string.

        Args:
            card_string: The credit card string to parse.

        Raises:
            InvalidCardNumberError: If the card string format is invalid.
            InvalidExpiryDateError: If the expiry date format is invalid.
        """
        if not card_string or not isinstance(card_string, str):
            raise InvalidCardNumberError("Card string cannot be empty")

        self.card_string = card_string.strip()
        self.card_number, self.expiry_month, self.expiry_year, self.cvv = self._parse_card_string(self.card_string)

    def _parse_card_string(self, card_string: str) -> tuple[str, str, str, str]:
        """
        Parse the card string into its components.

        Args:
            card_string: The card string to parse.

        Returns:
            A tuple of (card_number, expiry_month, expiry_year, cvv).

        Raises:
            InvalidCardNumberError: If the format is invalid.
            InvalidExpiryDateError: If the expiry date format is invalid.
        """
        delimiters = r"[|: ]+"
        parts = [p for p in re.split(delimiters, card_string) if p]

        if len(parts) == 3:
            card_number, expiry, cvv = parts
            if '/' in expiry:
                expiry_parts = expiry.split('/')
            elif '-' in expiry:
                expiry_parts = expiry.split('-')
            else:
                raise InvalidExpiryDateError("Invalid expiry date format. Use MM/YY or MM/YYYY")

            if len(expiry_parts) != 2:
                raise InvalidExpiryDateError("Invalid expiry date format. Use MM/YY or MM/YYYY")

            expiry_month, expiry_year = expiry_parts

        elif len(parts) == 4:
            card_number, expiry_month, expiry_year, cvv = parts
        else:
            raise InvalidCardNumberError(
                "Invalid card string format. Expected: NUMBER|MM|YYYY|CVV or NUMBER|MM/YY|CVV"
            )

        # Validate and normalize month
        try:
            month_int = int(expiry_month)
            if month_int < 1 or month_int > 12:
                raise InvalidExpiryDateError(f"Invalid month: {expiry_month}. Must be 01-12")
            expiry_month = f"{month_int:02d}"
        except ValueError:
            raise InvalidExpiryDateError(f"Invalid month: {expiry_month}. Must be numeric")

        # Normalize year to 4 digits
        if len(expiry_year) == 2:
            expiry_year = "20" + expiry_year
        elif len(expiry_year) != 4:
            raise InvalidExpiryDateError(f"Invalid year: {expiry_year}. Use YY or YYYY format")

        # Validate card number contains only digits
        if not card_number.isdigit():
            raise InvalidCardNumberError("Card number must contain only digits")

        # Validate CVV contains only digits
        if not cvv.isdigit():
            raise InvalidCVVError("CVV must contain only digits")

        return card_number, expiry_month, expiry_year, cvv

    def get_number(self) -> str:
        """
        Get the raw card number.

        Returns:
            The unformatted card number string.
        """
        return self.card_number

    def get_formatted_number(self) -> str:
        """
        Get the formatted card number with spaces.

        Returns:
            The card number formatted with spaces (e.g., '4111 1111 1111 1111').
        """
        return format_card_number(self.card_number)

    def get_expiry(self) -> str:
        """
        Get the expiry date in MM/YY format.

        Returns:
            The expiry date string (e.g., '12/30').
        """
        return f"{self.expiry_month}/{self.expiry_year[2:]}"

    def get_expiry_full(self) -> str:
        """
        Get the expiry date in MM/YYYY format.

        Returns:
            The full expiry date string (e.g., '12/2030').
        """
        return f"{self.expiry_month}/{self.expiry_year}"

    def get_year(self) -> str:
        """
        Get the expiry year.

        Returns:
            The 4-digit expiry year (e.g., '2030').
        """
        return self.expiry_year

    def get_month(self) -> str:
        """
        Get the expiry month.

        Returns:
            The 2-digit expiry month (e.g., '12').
        """
        return self.expiry_month

    def get_cvv(self) -> str:
        """
        Get the CVV code.

        Returns:
            The CVV/CVC code string.
        """
        return self.cvv

    def is_valid(self) -> bool:
        """
        Check if the card data is valid.

        Validates the card number (Luhn check), expiry date (not expired),
        and CVV length (3 or 4 digits depending on card type).

        Returns:
            True if all validations pass, False otherwise.

        Note:
            This method returns False instead of raising exceptions for
            validation failures. Use validate() if you need detailed
            error information.
        """
        try:
            if not validate_card_number(self.card_number):
                return False
            if not validate_expiry_date(self.expiry_month, self.expiry_year):
                return False
            if not validate_cvv(self.cvv, self.card_number):
                return False
            return True
        except Exception:
            return False

    def validate(self) -> None:
        """
        Validate the card data and raise exceptions on failure.

        Raises:
            InvalidCardNumberError: If the card number fails Luhn validation.
            InvalidExpiryDateError: If the card has expired.
            InvalidCVVError: If the CVV length is incorrect for the card type.
        """
        if not validate_card_number(self.card_number):
            raise InvalidCardNumberError("Card number failed Luhn validation")
        if not validate_expiry_date(self.expiry_month, self.expiry_year):
            raise InvalidExpiryDateError("Card has expired or expiry date is invalid")
        if not validate_cvv(self.cvv, self.card_number):
            raise InvalidCVVError(
                f"Invalid CVV length. Expected {'4' if detect_card_type(self.card_number) == 'AMEX' else '3'} digits"
            )

    def get_card_type(self) -> str:
        """
        Detect and return the card type.

        Returns:
            The card type name (e.g., 'Visa', 'MasterCard', 'AMEX'),
            or 'Unknown' if not recognized.
        """
        return detect_card_type(self.card_number)

    def get_masked_number(self) -> str:
        """
        Get the masked card number.

        Returns:
            The card number with most digits masked
            (e.g., '**** **** **** 1111').
        """
        return mask_card_number(self.card_number)

    def get_card_details(self) -> Optional[dict]:
        """
        Fetch detailed card information from BIN lookup.

        This method requires the 'requests' library. Install with:
        pip install ccparser[api]

        Returns:
            A dictionary with card details (bank, country, etc.),
            or None if lookup fails.

        Raises:
            ImportError: If 'requests' is not installed.
        """
        return get_card_details(self.card_number)

    def to_dict(self) -> dict:
        """
        Convert card data to a dictionary.

        Returns:
            A dictionary containing all card information.
        """
        return {
            'number': self.card_number,
            'formatted_number': self.get_formatted_number(),
            'masked_number': self.get_masked_number(),
            'expiry': self.get_expiry(),
            'expiry_month': self.expiry_month,
            'expiry_year': self.expiry_year,
            'cvv': self.cvv,
            'card_type': self.get_card_type(),
            'is_valid': self.is_valid()
        }

    def __repr__(self) -> str:
        """Return a string representation of the CCParser object."""
        return f"CCParser(type={self.get_card_type()}, masked={self.get_masked_number()})"

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"{self.get_card_type()} {self.get_masked_number()} (exp: {self.get_expiry()})"
