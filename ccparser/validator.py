"""
Validation functions for credit card data.

This module provides validation functions for card numbers (using Luhn algorithm),
expiry dates, and CVV codes.
"""

import datetime
from typing import Optional
from .utils import detect_card_type


def validate_card_number(card_number: str) -> bool:
    """
    Validate a credit card number using the Luhn algorithm.

    Args:
        card_number: The credit card number to validate (digits only).

    Returns:
        True if the card number passes Luhn validation, False otherwise.

    Example:
        >>> validate_card_number("4111111111111111")
        True
        >>> validate_card_number("1234567890123456")
        False
    """
    if not card_number or not card_number.isdigit():
        return False

    def luhn_checksum(number: str) -> int:
        def digits_of(n: str) -> list[int]:
            return [int(d) for d in str(n)]
        digits = digits_of(number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    return luhn_checksum(card_number) == 0


def validate_expiry_date(month: str, year: str) -> bool:
    """
    Validate that a credit card expiry date is not in the past.

    The card is considered valid through the last day of the expiry month.

    Args:
        month: The expiry month (1-12 or 01-12).
        year: The expiry year (YYYY or YY format).

    Returns:
        True if the expiry date is valid and not expired, False otherwise.

    Example:
        >>> validate_expiry_date("12", "2030")
        True
        >>> validate_expiry_date("01", "2020")
        False
    """
    try:
        month_int = int(month)
        year_int = int(year)

        # Handle 2-digit year format
        if year_int < 100:
            year_int += 2000

        # Validate month range
        if month_int < 1 or month_int > 12:
            return False

        # Validate year is reasonable (not too far in past or future)
        current_year = datetime.datetime.now().year
        if year_int < current_year - 10 or year_int > current_year + 20:
            return False

        # Create expiry date (first day of expiry month)
        expiry_date = datetime.datetime(year_int, month_int, 1)

        # Calculate the last day of the expiry month
        if month_int == 12:
            # December: last day is the 31st
            last_day = 31
        else:
            # Get the first day of next month and subtract one day
            next_month = datetime.datetime(year_int, month_int + 1, 1)
            last_day = (next_month - datetime.timedelta(days=1)).day

        expiry_date = expiry_date.replace(day=last_day)

        # Compare with current date (ignoring time, just date)
        now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return expiry_date >= now

    except (ValueError, TypeError):
        return False


def validate_cvv(cvv: str, card_number: str) -> bool:
    """
    Validate a CVV (Card Verification Value) code.

    AMEX cards require a 4-digit CVV, while other cards require 3 digits.

    Args:
        cvv: The CVV code to validate.
        card_number: The associated card number (used to determine card type).

    Returns:
        True if the CVV is valid for the card type, False otherwise.

    Example:
        >>> validate_cvv("123", "4111111111111111")  # Visa
        True
        >>> validate_cvv("1234", "378282246310005")  # AMEX
        True
        >>> validate_cvv("123", "378282246310005")  # AMEX with 3-digit CVV
        False
    """
    if not cvv or not cvv.isdigit():
        return False

    card_type = detect_card_type(card_number)
    if card_type == "AMEX":
        return len(cvv) == 4
    return len(cvv) == 3
