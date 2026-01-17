"""Tests for the parser module."""

import pytest
from ccparser import (
    CCParser,
    CCParserError,
    InvalidCardNumberError,
    InvalidExpiryDateError,
    InvalidCVVError,
)


class TestCCParserBasic:
    """Basic parsing tests."""

    def test_parse_pipe_delimited(self):
        """Test parsing pipe-delimited card string."""
        card = CCParser("4111111111111111|12|2030|123")
        assert card.get_number() == "4111111111111111"
        assert card.get_formatted_number() == "4111 1111 1111 1111"
        assert card.get_expiry() == "12/30"
        assert card.get_cvv() == "123"
        assert card.is_valid()
        assert card.get_card_type() == "Visa"
        assert card.get_masked_number() == "**** **** **** 1111"

    def test_parse_space_delimited(self):
        """Test parsing space-delimited card string."""
        card = CCParser("4111111111111111 12 2030 123")
        assert card.get_number() == "4111111111111111"
        assert card.get_expiry() == "12/30"

    def test_parse_colon_delimited(self):
        """Test parsing colon-delimited card string."""
        card = CCParser("4111111111111111:12:2030:123")
        assert card.get_number() == "4111111111111111"

    def test_parse_slash_expiry(self):
        """Test parsing with MM/YY expiry format."""
        card = CCParser("4111111111111111|12/30|123")
        assert card.get_expiry() == "12/30"
        assert card.get_year() == "2030"

    def test_parse_dash_expiry(self):
        """Test parsing with MM-YY expiry format."""
        card = CCParser("4111111111111111|12-30|123")
        assert card.get_expiry() == "12/30"

    def test_parse_two_digit_year(self):
        """Test parsing with 2-digit year."""
        card = CCParser("4111111111111111|12|30|123")
        assert card.get_year() == "2030"

    def test_parse_four_digit_year(self):
        """Test parsing with 4-digit year."""
        card = CCParser("4111111111111111|12|2030|123")
        assert card.get_year() == "2030"


class TestCCParserCardTypes:
    """Tests for different card types."""

    def test_mastercard(self):
        """Test MasterCard parsing."""
        card = CCParser("5500000000000004|12|2030|123")
        assert card.get_card_type() == "MasterCard"
        assert card.is_valid()

    def test_amex(self):
        """Test American Express parsing."""
        card = CCParser("378282246310005|12|2030|1234")
        assert card.get_card_type() == "AMEX"
        assert card.get_formatted_number() == "3782 822463 10005"
        assert card.get_masked_number() == "**** ****** *0005"
        assert card.is_valid()

    def test_discover(self):
        """Test Discover card parsing."""
        card = CCParser("6011111111111117|12|2030|123")
        assert card.get_card_type() == "Discover"
        assert card.is_valid()

    def test_diners_club(self):
        """Test Diners Club card parsing."""
        card = CCParser("30569309025904|12|2030|123")
        assert card.get_card_type() == "Diners Club"
        assert card.get_formatted_number() == "3056 930902 5904"


class TestCCParserValidation:
    """Tests for validation functionality."""

    def test_is_valid_returns_bool(self):
        """Test that is_valid returns boolean, not raises."""
        card = CCParser("4111111111111111|12|2030|123")
        result = card.is_valid()
        assert isinstance(result, bool)
        assert result is True

    def test_is_valid_invalid_luhn(self):
        """Test is_valid returns False for invalid Luhn."""
        card = CCParser("4111111111111112|12|2030|123")
        assert card.is_valid() is False

    def test_is_valid_expired_card(self):
        """Test is_valid returns False for expired card."""
        card = CCParser("4111111111111111|01|2020|123")
        assert card.is_valid() is False

    def test_is_valid_wrong_cvv_length(self):
        """Test is_valid returns False for wrong CVV length."""
        card = CCParser("4111111111111111|12|2030|12")  # Too short
        assert card.is_valid() is False

    def test_validate_raises_on_invalid_luhn(self):
        """Test that validate() raises for invalid Luhn."""
        card = CCParser("4111111111111112|12|2030|123")
        with pytest.raises(InvalidCardNumberError):
            card.validate()

    def test_validate_raises_on_expired(self):
        """Test that validate() raises for expired card."""
        card = CCParser("4111111111111111|01|2020|123")
        with pytest.raises(InvalidExpiryDateError):
            card.validate()

    def test_validate_raises_on_wrong_cvv(self):
        """Test that validate() raises for wrong CVV."""
        card = CCParser("4111111111111111|12|2030|12")
        with pytest.raises(InvalidCVVError):
            card.validate()


class TestCCParserErrors:
    """Tests for error handling."""

    def test_empty_string_raises(self):
        """Test that empty string raises error."""
        with pytest.raises(InvalidCardNumberError):
            CCParser("")

    def test_none_raises(self):
        """Test that None raises error."""
        with pytest.raises(InvalidCardNumberError):
            CCParser(None)

    def test_invalid_format_raises(self):
        """Test that invalid format raises error."""
        with pytest.raises(InvalidCardNumberError):
            CCParser("4111111111111111")

    def test_invalid_month_raises(self):
        """Test that invalid month raises error."""
        with pytest.raises(InvalidExpiryDateError):
            CCParser("4111111111111111|13|2030|123")

    def test_zero_month_raises(self):
        """Test that month 0 raises error."""
        with pytest.raises(InvalidExpiryDateError):
            CCParser("4111111111111111|00|2030|123")

    def test_non_numeric_card_raises(self):
        """Test that non-numeric card number raises error."""
        with pytest.raises(InvalidCardNumberError):
            CCParser("4111ABCD11111111|12|2030|123")

    def test_non_numeric_cvv_raises(self):
        """Test that non-numeric CVV raises error."""
        with pytest.raises(InvalidCVVError):
            CCParser("4111111111111111|12|2030|ABC")

    def test_base_exception_hierarchy(self):
        """Test that all exceptions inherit from CCParserError."""
        assert issubclass(InvalidCardNumberError, CCParserError)
        assert issubclass(InvalidExpiryDateError, CCParserError)
        assert issubclass(InvalidCVVError, CCParserError)


class TestCCParserMethods:
    """Tests for additional CCParser methods."""

    def test_get_expiry_full(self):
        """Test get_expiry_full method."""
        card = CCParser("4111111111111111|12|2030|123")
        assert card.get_expiry_full() == "12/2030"

    def test_to_dict(self):
        """Test to_dict method."""
        card = CCParser("4111111111111111|12|2030|123")
        result = card.to_dict()
        assert result['number'] == "4111111111111111"
        assert result['formatted_number'] == "4111 1111 1111 1111"
        assert result['masked_number'] == "**** **** **** 1111"
        assert result['expiry'] == "12/30"
        assert result['expiry_month'] == "12"
        assert result['expiry_year'] == "2030"
        assert result['cvv'] == "123"
        assert result['card_type'] == "Visa"
        assert result['is_valid'] is True

    def test_repr(self):
        """Test __repr__ method."""
        card = CCParser("4111111111111111|12|2030|123")
        repr_str = repr(card)
        assert "CCParser" in repr_str
        assert "Visa" in repr_str

    def test_str(self):
        """Test __str__ method."""
        card = CCParser("4111111111111111|12|2030|123")
        str_str = str(card)
        assert "Visa" in str_str
        assert "12/30" in str_str

    def test_month_normalization(self):
        """Test that single-digit months are normalized."""
        card = CCParser("4111111111111111|1|2030|123")
        assert card.get_month() == "01"

    def test_whitespace_handling(self):
        """Test that whitespace is stripped."""
        card = CCParser("  4111111111111111|12|2030|123  ")
        assert card.get_number() == "4111111111111111"
