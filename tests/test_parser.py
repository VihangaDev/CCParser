import pytest
from ccparser import CCParser

def test_parser():
    card = CCParser("4111111111111111|12|2030|123")
    assert card.get_number() == "4111111111111111"
    assert card.get_formatted_number() == "4111 1111 1111 1111"
    assert card.get_expiry() == "12/30"
    assert card.get_cvv() == "123"
    assert card.is_valid() == True
    assert card.get_card_type() == "Visa"
    assert card.get_masked_number() == "**** **** **** 1111"