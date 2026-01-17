"""
Utility functions for credit card operations.

This module provides helper functions for detecting card types and
fetching BIN (Bank Identification Number) information.
"""

import re
from typing import Optional

# Card type patterns for detection
CARD_TYPE_PATTERNS = {
    "Visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
    "MasterCard": r"^5[1-5][0-9]{14}$",
    "AMEX": r"^3[47][0-9]{13}$",
    "Discover": r"^6(?:011|4[4-9][0-9]|5[0-9]{2})[0-9]{12}$",
    "JCB": r"^(?:2131|1800|35\d{3})\d{11}$",
    "Diners Club": r"^3(?:0[0-5]|[68][0-9])[0-9]{11}$",
    "UnionPay": r"^62[0-9]{14,17}$"
}


def detect_card_type(card_number: str) -> str:
    """
    Detect the card type based on the card number pattern.

    Supports detection of: Visa, MasterCard, AMEX, Discover, JCB,
    Diners Club, and UnionPay.

    Args:
        card_number: The credit card number (digits only).

    Returns:
        The detected card type name, or "Unknown" if not recognized.

    Example:
        >>> detect_card_type("4111111111111111")
        'Visa'
        >>> detect_card_type("5500000000000004")
        'MasterCard'
        >>> detect_card_type("378282246310005")
        'AMEX'
    """
    if not card_number:
        return "Unknown"

    # Clean any non-digit characters
    clean_number = "".join(c for c in card_number if c.isdigit())

    for card_type, pattern in CARD_TYPE_PATTERNS.items():
        if re.match(pattern, clean_number):
            return card_type

    return "Unknown"


def get_card_details(card_number: str, timeout: int = 10) -> Optional[dict]:
    """
    Fetch detailed card information from BIN lookup service.

    This function requires the 'requests' library and makes an external
    API call to binlist.net. Install with: pip install ccparser[api]

    Args:
        card_number: The credit card number (at least 6 digits for BIN).
        timeout: Request timeout in seconds (default: 10).

    Returns:
        A dictionary containing card details, or None if lookup fails.
        Dictionary keys: bank, name, brand, country, emoji, scheme,
        type, currency, bin.

    Raises:
        ImportError: If 'requests' library is not installed.

    Example:
        >>> details = get_card_details("4111111111111111")
        >>> details['scheme']
        'visa'
    """
    try:
        import requests
    except ImportError:
        raise ImportError(
            "The 'requests' library is required for get_card_details(). "
            "Install it with: pip install ccparser[api]"
        )

    if not card_number or len(card_number) < 6:
        return None

    # Clean the card number and extract BIN
    clean_number = "".join(c for c in card_number if c.isdigit())
    bin_number = clean_number[:6]

    url = f'https://lookup.binlist.net/{bin_number}'
    headers = {
        'User-Agent': 'CCParser/1.0 (https://github.com/VihangaDev/CCParser)',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)

        if response.status_code == 200:
            data = response.json()
            card_details = {
                'bank': data.get('bank', {}).get('name', 'Unknown') if data.get('bank') else 'Unknown',
                'name': data.get('name', 'Unknown'),
                'brand': data.get('brand', 'Unknown'),
                'country': data.get('country', {}).get('name', 'Unknown') if data.get('country') else 'Unknown',
                'emoji': data.get('country', {}).get('emoji', '') if data.get('country') else '',
                'scheme': data.get('scheme', 'Unknown'),
                'type': data.get('type', 'Unknown'),
                'currency': data.get('country', {}).get('currency', 'Unknown') if data.get('country') else 'Unknown',
                'bin': 'Credit' if data.get('type') == 'credit' else 'Debit'
            }
            return card_details
        elif response.status_code == 404:
            # BIN not found in database
            return None
        elif response.status_code == 429:
            # Rate limited
            return None
        else:
            return None

    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.RequestException:
        return None
    except (ValueError, KeyError):
        # JSON parsing error or missing keys
        return None
