import pytest
from ccparser.generator import generate_card_number
from ccparser.validator import validate_card_number

def test_generate_card_number():
    card_types = ["Visa", "MasterCard", "AMEX", "Discover", "JCB", "Diners Club", "UnionPay"]
    for card_type in card_types:
        card_number = generate_card_number(card_type)
        assert validate_card_number(card_number) == True