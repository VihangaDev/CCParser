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
    "MasterCard": ["51", "52", "53", "54", "55", "2221", "2222", "2223",
                   "23", "24", "25", "26", "270", "271", "2720"],
    "AMEX": ["34", "37"],
    "Discover": ["6011", "644", "645", "646", "647", "648", "649", "65",
                 "622126", "622127", "622128", "622129", "62213",
                 "6222", "6223", "6224", "6225", "6226", "6227", "6228",
                 "62290", "62291", "622920", "622921", "622922",
                 "622923", "622924", "622925"],
    "JCB": ["3528", "3529", "353", "354", "355", "356", "357", "358"],
    "Diners Club": ["300", "301", "302", "303", "304", "305", "36", "38"],
    # Use 81 to avoid Discover's 622126-622925 overlap
    "UnionPay": ["81"],
    "Maestro": ["5018", "5020", "5038", "5893", "6304", "6759",
                "6761", "6762", "6763"],
    "Visa Electron": ["4026", "417500", "4405", "4508", "4844", "4913", "4917"],
    "Mir": ["2200", "2201", "2202", "2203", "2204"],
    "Elo": ["401178", "401179", "438935", "457631", "457632", "431274",
            "451416", "457393", "504175", "506699", "5067", "5068",
            "5069", "509", "636368", "636297", "636369", "627780"],
    "Troy": ["9792"],
    "Dankort": ["5019"],
    "UATP": ["1"],
    "Humo": ["9860"],
    "UzCard": ["8600"],
    "Verve": ["506099", "506100", "506101", "650002", "650003", "650004"],
    "InstaPayment": ["637", "638", "639"],
    "InterPayment": ["636"],
    "LankaPay": ["357111"],
    "RuPay": [],  # RuPay overlaps with many networks, use detect_card_type instead
}

# Card lengths by type
CARD_LENGTHS = {
    "Visa": 16,
    "MasterCard": 16,
    "AMEX": 15,
    "Discover": 16,
    "JCB": 16,
    "Diners Club": 14,
    "UnionPay": 16,
    "Maestro": 16,
    "Visa Electron": 16,
    "Mir": 16,
    "Elo": 16,
    "Troy": 16,
    "Dankort": 16,
    "UATP": 15,
    "Humo": 16,
    "UzCard": 16,
    "Verve": 16,
    "InstaPayment": 16,
    "InterPayment": 16,
    "LankaPay": 16,
    "RuPay": 16,
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
