import pytest
from ccparser import CCParser

def test_parser():
    card = CCParser("4783400008389576|04|2027|744")
    assert card.get_number() == "4783400008389576"
    assert card.get_formatted_number() == "4783 4000 0838 9576"
    assert card.get_expiry() == "04/27"
    assert card.get_cvv() == "744"
    assert card.is_valid() == True
    assert card.get_card_type() == "Visa"
    assert card.get_masked_number() == "**** **** **** 9576"