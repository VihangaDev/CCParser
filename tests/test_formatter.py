"""Tests for the formatter module."""

import pytest
from ccparser.formatter import format_card_number, mask_card_number


class TestFormatCardNumber:
    """Tests for format_card_number function."""

    def test_format_visa_16_digit(self):
        """Test formatting a standard 16-digit Visa card."""
        result = format_card_number("4111111111111111")
        assert result == "4111 1111 1111 1111"

    def test_format_mastercard_16_digit(self):
        """Test formatting a standard 16-digit MasterCard."""
        result = format_card_number("5500000000000004")
        assert result == "5500 0000 0000 0004"

    def test_format_amex_15_digit(self):
        """Test formatting a 15-digit AMEX card (4-6-5 pattern)."""
        result = format_card_number("378282246310005")
        assert result == "3782 822463 10005"

    def test_format_diners_14_digit(self):
        """Test formatting a 14-digit Diners Club card (4-6-4 pattern)."""
        result = format_card_number("30569309025904")
        assert result == "3056 930902 5904"

    def test_format_with_custom_separator(self):
        """Test formatting with a custom separator."""
        result = format_card_number("4111111111111111", separator="-")
        assert result == "4111-1111-1111-1111"

    def test_format_empty_string(self):
        """Test formatting an empty string."""
        result = format_card_number("")
        assert result == ""

    def test_format_already_formatted(self):
        """Test formatting a card number that already has spaces."""
        result = format_card_number("4111 1111 1111 1111")
        assert result == "4111 1111 1111 1111"

    def test_format_with_non_digits(self):
        """Test that non-digit characters are stripped."""
        result = format_card_number("4111-1111-1111-1111")
        assert result == "4111 1111 1111 1111"


class TestMaskCardNumber:
    """Tests for mask_card_number function."""

    def test_mask_visa_16_digit(self):
        """Test masking a standard 16-digit Visa card."""
        result = mask_card_number("4111111111111111")
        assert result == "**** **** **** 1111"

    def test_mask_mastercard_16_digit(self):
        """Test masking a standard 16-digit MasterCard."""
        result = mask_card_number("5500000000000004")
        assert result == "**** **** **** 0004"

    def test_mask_amex_15_digit(self):
        """Test masking a 15-digit AMEX card."""
        result = mask_card_number("378282246310005")
        assert result == "**** ****** *0005"

    def test_mask_diners_14_digit(self):
        """Test masking a 14-digit Diners Club card."""
        result = mask_card_number("30569309025904")
        assert result == "**** ****** 5904"

    def test_mask_empty_string(self):
        """Test masking an empty string."""
        result = mask_card_number("")
        assert result == ""

    def test_mask_short_number(self):
        """Test masking a number shorter than visible digits."""
        result = mask_card_number("123")
        assert result == "123"

    def test_mask_with_spaces(self):
        """Test masking a card number that has spaces."""
        result = mask_card_number("4111 1111 1111 1111")
        assert result == "**** **** **** 1111"

    def test_mask_custom_visible_digits(self):
        """Test masking with custom number of visible digits on non-standard length."""
        # Test with a 12-digit number to use generic fallback
        result = mask_card_number("411111111111", visible_digits=4)
        assert result == "**** **** 1111"
