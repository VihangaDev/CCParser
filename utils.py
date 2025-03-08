import re

def detect_card_type(card_number):
    card_types = {
        "Visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
        "MasterCard": r"^5[1-5][0-9]{14}$",
        "AMEX": r"^3[47][0-9]{13}$",
        "Discover": r"^6(?:011|5[0-9]{2})[0-9]{12}$"
    }
    for card_type, pattern in card_types.items():
        if re.match(pattern, card_number):
            return card_type
    return "Unknown"