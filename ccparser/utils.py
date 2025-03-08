import re
import requests

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

def get_card_details(card_number):
    bin_number = card_number[:6]
    url = f'https://lookup.binlist.net/{bin_number}'
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        card_details = {
            'bank': data.get('bank', {}).get('name', 'Unknown'),
            'name': data.get('name', 'Unknown'),
            'brand': data.get('brand', 'Unknown'),
            'country': data.get('country', {}).get('name', 'Unknown'),
            'emoji': data.get('country', {}).get('emoji', ''),
            'scheme': data.get('scheme', 'Unknown'),
            'type': data.get('type', 'Unknown'),
            'currency': data.get('country', {}).get('currency', 'Unknown'),
            'bin': 'Credit' if data.get('type') == 'credit' else 'Debit'
        }
        return card_details
    else:
        return None