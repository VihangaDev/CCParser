import random

def generate_card_number(card_type: str) -> str:
    card_prefixes = {
        "Visa": "4",
        "MasterCard": "5",
        "AMEX": "3",
        "Discover": "6",
        "JCB": "35",
        "Diners Club": "3",
        "UnionPay": "62"
    }
    
    if card_type not in card_prefixes:
        raise ValueError("Unsupported card type")
    
    prefix = card_prefixes[card_type]
    length = 16 if card_type != "AMEX" else 15
    card_number = [int(d) for d in prefix]
    
    while len(card_number) < (length - 1):
        card_number.append(random.randint(0, 9))
    
    def luhn_checksum(card_number: list[int]) -> int:
        def digits_of(n: str) -> list[int]:
            return [int(d) for d in str(n)]
        digits = digits_of("".join(map(str, card_number)))
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10
    
    checksum = luhn_checksum(card_number)
    card_number.append((10 - checksum) % 10)
    
    return "".join(map(str, card_number))