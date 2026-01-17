"""
Credit card number generator for testing purposes.

This module provides functionality to generate valid test credit card numbers
that pass Luhn validation. These are for testing purposes only and should
never be used for actual transactions.
"""

import random
from typing import List, Optional

# Card type prefixes and their corresponding IIN ranges
CARD_PREFIXES = {
    "Visa": ["4"],
    "MasterCard": ["51", "52", "53", "54", "55"],
    "AMEX": ["34", "37"],
    "Discover": ["6011", "644", "645", "646", "647", "648", "649", "65"],
    "JCB": ["3528", "3529", "353", "354", "355", "356", "357", "358"],
    "Diners Club": ["300", "301", "302", "303", "304", "305", "36", "38"],
    "UnionPay": ["62"]
}

# Card lengths by type
CARD_LENGTHS = {
    "Visa": 16,
    "MasterCard": 16,
    "AMEX": 15,
    "Discover": 16,
    "JCB": 16,
    "Diners Club": 14,
    "UnionPay": 16
}


def generate_card_number(card_type: str, seed: Optional[int] = None) -> str:
    """
    Generate a valid test credit card number for the specified card type.

    The generated number passes Luhn validation and matches the IIN (Issuer
    Identification Number) pattern for the specified card type.

    **WARNING:** These are test numbers only. They are not connected to any
    real account and should never be used for actual transactions.

    Args:
        card_type: The type of credit card to generate.
            Supported types: Visa, MasterCard, AMEX, Discover, JCB,
            Diners Club, UnionPay.
        seed: Optional random seed for reproducible generation.

    Returns:
        A valid credit card number string that passes Luhn validation.

    Raises:
        ValueError: If the card type is not supported.

    Example:
        >>> generate_card_number("Visa")
        '4532015112830366'
        >>> generate_card_number("AMEX")
        '378282246310005'
    """
    if card_type not in CARD_PREFIXES:
        supported = ", ".join(sorted(CARD_PREFIXES.keys()))
        raise ValueError(f"Unsupported card type: '{card_type}'. Supported types: {supported}")

    if seed is not None:
        random.seed(seed)

    prefix = random.choice(CARD_PREFIXES[card_type])
    length = CARD_LENGTHS[card_type]

    # Generate card number without check digit
    number = prefix
    while len(number) < length - 1:
        number += str(random.randint(0, 9))

    # Calculate Luhn check digit
    check_digit = _calculate_luhn_check_digit(number)

    return number + str(check_digit)


def _calculate_luhn_check_digit(number: str) -> int:
    """
    Calculate the Luhn check digit for a partial card number.

    Args:
        number: The card number without the check digit.

    Returns:
        The check digit (0-9) that makes the number pass Luhn validation.
    """
    total = 0
    reversed_digits = number[::-1]

    for i, digit in enumerate(reversed_digits):
        digit_value = int(digit)
        if i % 2 == 0:
            digit_value *= 2
            if digit_value > 9:
                digit_value -= 9
        total += digit_value

    return (10 - (total % 10)) % 10


def get_supported_card_types() -> List[str]:
    """
    Get a list of supported card types for generation.

    Returns:
        A sorted list of supported card type names.

    Example:
        >>> get_supported_card_types()
        ['AMEX', 'Diners Club', 'Discover', 'JCB', 'MasterCard', 'UnionPay', 'Visa']
    """
    return sorted(CARD_PREFIXES.keys())
