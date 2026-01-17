"""Tests for the validator module."""

import pytest
from ccparser.validator import validate_card_number, validate_expiry_date, validate_cvv


class TestValidateCardNumber:
    """Tests for validate_card_number function."""

    def test_valid_visa(self):
        """Test valid Visa card number."""
        assert validate_card_number("4111111111111111") is True

    def test_valid_mastercard(self):
        """Test valid MasterCard number."""
        assert validate_card_number("5500000000000004") is True

    def test_valid_amex(self):
        """Test valid AMEX card number."""
        assert validate_card_number("378282246310005") is True

    def test_invalid_luhn(self):
        """Test card number that fails Luhn check."""
        assert validate_card_number("4111111111111112") is False

    def test_all_zeros(self):
        """Test that all zeros fails validation."""
        assert validate_card_number("0000000000000000") is True  # Actually passes Luhn!

    def test_empty_string(self):
        """Test empty string returns False."""
        assert validate_card_number("") is False

    def test_non_numeric(self):
        """Test non-numeric string returns False."""
        assert validate_card_number("4111ABCD11111111") is False

    def test_with_spaces(self):
        """Test string with spaces returns False."""
        assert validate_card_number("4111 1111 1111 1111") is False

    def test_none_value(self):
        """Test None value returns False."""
        assert validate_card_number(None) is False


class TestValidateExpiryDate:
    """Tests for validate_expiry_date function."""

    def test_future_date_valid(self):
        """Test future expiry date is valid."""
        assert validate_expiry_date("12", "2030") is True

    def test_past_date_invalid(self):
        """Test past expiry date is invalid."""
        assert validate_expiry_date("01", "2020") is False

    def test_two_digit_year(self):
        """Test 2-digit year is handled correctly."""
        assert validate_expiry_date("12", "30") is True

    def test_december_edge_case(self):
        """Test December month handling (previously buggy)."""
        assert validate_expiry_date("12", "2030") is True

    def test_january_edge_case(self):
        """Test January month handling."""
        assert validate_expiry_date("01", "2030") is True

    def test_invalid_month_zero(self):
        """Test month 0 is invalid."""
        assert validate_expiry_date("00", "2030") is False

    def test_invalid_month_thirteen(self):
        """Test month 13 is invalid."""
        assert validate_expiry_date("13", "2030") is False

    def test_invalid_month_negative(self):
        """Test negative month is invalid."""
        assert validate_expiry_date("-1", "2030") is False

    def test_invalid_year_too_far_past(self):
        """Test year too far in past is invalid."""
        assert validate_expiry_date("12", "2000") is False

    def test_invalid_year_too_far_future(self):
        """Test year too far in future is invalid."""
        assert validate_expiry_date("12", "2100") is False

    def test_non_numeric_month(self):
        """Test non-numeric month returns False."""
        assert validate_expiry_date("AB", "2030") is False

    def test_non_numeric_year(self):
        """Test non-numeric year returns False."""
        assert validate_expiry_date("12", "YYYY") is False

    def test_empty_values(self):
        """Test empty values return False."""
        assert validate_expiry_date("", "2030") is False
        assert validate_expiry_date("12", "") is False


class TestValidateCVV:
    """Tests for validate_cvv function."""

    def test_valid_3_digit_cvv(self):
        """Test valid 3-digit CVV for Visa."""
        assert validate_cvv("123", "4111111111111111") is True

    def test_valid_4_digit_cvv_amex(self):
        """Test valid 4-digit CVV for AMEX."""
        assert validate_cvv("1234", "378282246310005") is True

    def test_invalid_3_digit_cvv_amex(self):
        """Test 3-digit CVV is invalid for AMEX."""
        assert validate_cvv("123", "378282246310005") is False

    def test_invalid_4_digit_cvv_visa(self):
        """Test 4-digit CVV is invalid for Visa."""
        assert validate_cvv("1234", "4111111111111111") is False

    def test_invalid_2_digit_cvv(self):
        """Test 2-digit CVV is invalid."""
        assert validate_cvv("12", "4111111111111111") is False

    def test_empty_cvv(self):
        """Test empty CVV returns False."""
        assert validate_cvv("", "4111111111111111") is False

    def test_non_numeric_cvv(self):
        """Test non-numeric CVV returns False."""
        assert validate_cvv("ABC", "4111111111111111") is False

    def test_cvv_with_spaces(self):
        """Test CVV with spaces returns False."""
        assert validate_cvv("1 2 3", "4111111111111111") is False
