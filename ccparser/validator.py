import datetime
from .utils import detect_card_type

def validate_card_number(card_number: str) -> bool:
    def luhn_checksum(card_number: str) -> int:
        def digits_of(n: str) -> list[int]:
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10
    
    return luhn_checksum(card_number) == 0

def validate_expiry_date(month: str, year: str) -> bool:
    now = datetime.datetime.now()
    expiry_date = datetime.datetime(int(year), int(month), 1)
    last_day_of_month = (expiry_date.replace(month=expiry_date.month % 12 + 1, day=1) - datetime.timedelta(days=1)).day
    expiry_date = expiry_date.replace(day=last_day_of_month)
    return expiry_date >= now.replace(day=1)

def validate_cvv(cvv: str, card_number: str) -> bool:
    card_type = detect_card_type(card_number)
    if card_type == "AMEX":
        return len(cvv) == 4
    return len(cvv) == 3