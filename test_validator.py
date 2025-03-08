import pytest
from ccparser.validator import validate_card_number, validate_expiry_date, validate_cvv

def test_validate_card_number():
    assert validate_card_number("4783400008389576") == True
    assert validate_card_number("1234567812345670") == False

def test_validate_expiry_date():
    assert validate_expiry_date("04", "2027") == True
    assert validate_expiry_date("04", "2020") == False

def test_validate_cvv():
    assert validate_cvv("744", "4783400008389576") == True
    assert validate_cvv("1234", "378282246310005") == True
    assert validate_cvv("123", "378282246310005") == False