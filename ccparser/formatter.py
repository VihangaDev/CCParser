"""
Formatting functions for credit card numbers.

This module provides functions to format and mask credit card numbers
for display purposes.
"""


def format_card_number(card_number: str, separator: str = " ") -> str:
    """
    Format a credit card number into groups of 4 digits.

    For AMEX cards (15 digits), formats as 4-6-5 pattern.
    For other cards, formats as 4-4-4-4 pattern.

    Args:
        card_number: The credit card number (digits only).
        separator: The separator to use between groups (default: space).

    Returns:
        The formatted card number string.

    Example:
        >>> format_card_number("4111111111111111")
        '4111 1111 1111 1111'
        >>> format_card_number("378282246310005")
        '3782 822463 10005'
    """
    if not card_number:
        return ""

    # Clean any existing formatting
    clean_number = "".join(c for c in card_number if c.isdigit())

    # AMEX format: 4-6-5
    if len(clean_number) == 15:
        return f"{clean_number[:4]}{separator}{clean_number[4:10]}{separator}{clean_number[10:]}"

    # Diners Club format: 4-6-4
    if len(clean_number) == 14:
        return f"{clean_number[:4]}{separator}{clean_number[4:10]}{separator}{clean_number[10:]}"

    # Standard format: groups of 4
    return separator.join(clean_number[i:i+4] for i in range(0, len(clean_number), 4))


def mask_card_number(card_number: str, visible_digits: int = 4) -> str:
    """
    Mask a credit card number, showing only the last few digits.

    Supports different card lengths:
    - 16 digits (Visa, MasterCard, etc.): **** **** **** 1234
    - 15 digits (AMEX): **** ****** *2345
    - 14 digits (Diners Club): **** ****** 1234

    Args:
        card_number: The credit card number to mask.
        visible_digits: Number of digits to show at the end (default: 4).

    Returns:
        The masked card number string.

    Example:
        >>> mask_card_number("4111111111111111")
        '**** **** **** 1111'
        >>> mask_card_number("378282246310005")
        '**** ****** *0005'
    """
    if not card_number:
        return ""

    # Clean any existing formatting
    clean_number = "".join(c for c in card_number if c.isdigit())
    length = len(clean_number)

    if length < visible_digits:
        return clean_number

    # Get the visible portion
    visible_part = clean_number[-visible_digits:]

    # AMEX format: 4-6-5 with last 4 visible (1 masked in last group)
    if length == 15:
        return f"**** ****** *{visible_part}"

    # Diners Club format: 4-6-4 with last 4 visible
    if length == 14:
        return f"**** ****** {visible_part}"

    # Standard 16-digit format
    if length == 16:
        return f"**** **** **** {visible_part}"

    # Generic fallback for other lengths
    masked_length = length - visible_digits
    masked_groups = []
    remaining_masked = masked_length

    for i in range(0, length, 4):
        group_size = min(4, length - i)
        if remaining_masked >= group_size:
            masked_groups.append("*" * group_size)
            remaining_masked -= group_size
        elif remaining_masked > 0:
            masked_groups.append("*" * remaining_masked + clean_number[i + remaining_masked:i + group_size])
            remaining_masked = 0
        else:
            masked_groups.append(clean_number[i:i + group_size])

    return " ".join(masked_groups)
