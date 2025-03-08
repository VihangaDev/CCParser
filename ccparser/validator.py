import datetime
from .utils import detect_card_type

def validate_card_number(card_number):
    def luhn_checksum(card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        print(f"Card Number: {card_number}, Checksum: {checksum}")  # Debug print
        return checksum % 10
    
    return luhn_checksum(card_number) == 0

def validate_expiry_date(month, year):
    now = datetime.datetime.now()
    expiry_date = datetime.datetime(int(year), int(month), 1)
    return expiry_date > now

def validate_cvv(cvv, card_number):
    card_type = detect_card_type(card_number)
    if card_type == "AMEX":
        return len(cvv) == 4
    return len(cvv) == 3