"""
Utility functions for credit card operations.

This module provides helper functions for detecting card types and
fetching BIN (Bank Identification Number) information.
"""

import re
from typing import Optional

# Card type patterns for detection
# Order matters: more specific patterns must come before broader ones.
# Longer/more-specific prefixes are checked first to avoid false matches.
CARD_TYPE_PATTERNS = {
    # === Most specific first (6+ digit prefixes) ===

    # Elo: Brazilian card, very specific prefixes, 16 digits
    "Elo": r"^(?:401178|401179|438935|457631|457632|431274|451416|457393|504175|506699|506[7-9][0-9]{2}|509[0-9]{3}|636368|636297|636369|627780)[0-9]{10}$",

    # Verve: Nigerian/African payment network, 506099-506198, 650002-650027, 16 or 19 digits
    "Verve": r"^(?:506(?:099|1[0-9]{2})|650(?:00[2-9]|0[12][0-9]|027))[0-9]{10,13}$",

    # LankaPay: Sri Lankan payment network, starts with 357111, 16 digits
    # Must come before JCB (which matches 35xx)
    "LankaPay": r"^357111[0-9]{10}$",

    # === 4-digit prefixes ===

    # Dankort: Danish payment network, 5019, 16 digits
    "Dankort": r"^5019[0-9]{12}$",

    # Humo: Uzbekistan payment network, starts with 9860, 16 digits
    "Humo": r"^9860[0-9]{12}$",

    # UzCard: Uzbekistan payment network, starts with 8600, 16 digits
    "UzCard": r"^8600[0-9]{12}$",

    # Troy: Turkish payment network, 9792 prefix, 16 digits
    "Troy": r"^9792[0-9]{12}$",

    # Mir: Russian payment system, starts with 2200-2204, 16-19 digits
    "Mir": r"^220[0-4][0-9]{12,15}$",

    # Visa Electron: specific 4-digit prefixes, must come before generic Visa
    "Visa Electron": r"^(?:4026|417500|4405|4508|4844|4913|4917)[0-9]{10,13}$",

    # Maestro: various prefixes, 12-19 digits
    "Maestro": r"^(?:5018|5020|5038|5893|6304|6759|6761|6762|6763)[0-9]{8,15}$",

    # === 3-digit and 2-digit prefixes ===

    # AMEX: starts with 34 or 37, 15 digits
    "AMEX": r"^3[47][0-9]{13}$",

    # Diners Club Carte Blanche/International: 300-305, 36, 38, 14-19 digits
    "Diners Club": r"^3(?:0[0-5]|[68][0-9])[0-9]{11,14}$",

    # JCB: 2131, 1800 (15 digits) or 3528-3589 (16-19 digits)
    # Must come before UATP (which matches all 1xxx)
    "JCB": r"^(?:2131|1800|35[2-8][0-9])[0-9]{11,15}$",

    # UATP: airline card, starts with 1, 15 digits
    # Must come after JCB (1800 is JCB, not UATP)
    "UATP": r"^1[0-9]{14}$",

    # MasterCard: 51-55 (legacy) and 2221-2720 (2-series, added 2017), 16 digits
    "MasterCard": r"^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$",

    # Discover: 6011, 622126-622925 (co-brand), 644-649, 65, 16-19 digits
    # Must come before UnionPay (622xxx sub-range overlaps with UnionPay's 62)
    "Discover": r"^(?:6011[0-9]{12,15}|64[4-9][0-9]{13,16}|65[0-9]{14,17}|622(?:1(?:2[6-9]|[3-9][0-9])|[2-8][0-9]{2}|9(?:[01][0-9]|2[0-5]))[0-9]{10,13})$",

    # InstaPayment: 637-639, 16 digits
    "InstaPayment": r"^63[7-9][0-9]{13}$",

    # InterPayment: starts with 636, 16-19 digits
    "InterPayment": r"^636[0-9]{13,16}$",

    # UnionPay: starts with 62 or 81, 16-19 digits
    # Must come after Discover (622126-622925 is Discover co-brand, not UnionPay)
    "UnionPay": r"^(?:62|81)[0-9]{14,17}$",

    # Visa: starts with 4, 13, 16, or 19 digits (broadest 4-prefix, must be after Visa Electron/Elo)
    "Visa": r"^4[0-9]{12}(?:[0-9]{3})?(?:[0-9]{3})?$",
}


def detect_card_type(card_number: str) -> str:
    """
    Detect the card type based on the card number pattern.

    Supports detection of Visa, MasterCard, AMEX, Discover, JCB,
    Diners Club, UnionPay, and additional regional networks.

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
        'User-Agent': 'CCParser/2.0 (https://github.com/VihangaDev/CCParser)',
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
