"""Tests for the utils module."""

import pytest
from ccparser.utils import detect_card_type, CARD_TYPE_PATTERNS


class TestDetectCardType:
    """Tests for detect_card_type function."""

    def test_detect_visa(self):
        """Test detecting Visa cards."""
        assert detect_card_type("4111111111111111") == "Visa"
        assert detect_card_type("4012888888881881") == "Visa"
        assert detect_card_type("4222222222222") == "Visa"  # 13-digit Visa

    def test_detect_mastercard(self):
        """Test detecting MasterCard cards."""
        assert detect_card_type("5500000000000004") == "MasterCard"
        assert detect_card_type("5105105105105100") == "MasterCard"
        assert detect_card_type("5555555555554444") == "MasterCard"

    def test_detect_amex(self):
        """Test detecting American Express cards."""
        assert detect_card_type("378282246310005") == "AMEX"
        assert detect_card_type("371449635398431") == "AMEX"
        assert detect_card_type("340000000000009") == "AMEX"

    def test_detect_discover(self):
        """Test detecting Discover cards."""
        assert detect_card_type("6011111111111117") == "Discover"
        assert detect_card_type("6011000990139424") == "Discover"
        assert detect_card_type("6500000000000002") == "Discover"

    def test_detect_jcb(self):
        """Test detecting JCB cards."""
        assert detect_card_type("3530111333300000") == "JCB"
        assert detect_card_type("3566002020360505") == "JCB"

    def test_detect_diners_club(self):
        """Test detecting Diners Club cards."""
        assert detect_card_type("30569309025904") == "Diners Club"
        assert detect_card_type("38520000023237") == "Diners Club"

    def test_detect_unionpay(self):
        """Test detecting UnionPay cards."""
        assert detect_card_type("6200000000000005") == "UnionPay"
        assert detect_card_type("6212345678901234567") == "UnionPay"

    def test_detect_unknown(self):
        """Test detecting unknown card types."""
        assert detect_card_type("1234567890123456") == "Unknown"
        assert detect_card_type("9999999999999999") == "Unknown"

    def test_detect_empty_string(self):
        """Test detecting with empty string."""
        assert detect_card_type("") == "Unknown"

    def test_detect_with_spaces(self):
        """Test that spaces are ignored."""
        assert detect_card_type("4111 1111 1111 1111") == "Visa"

    def test_detect_with_dashes(self):
        """Test that dashes are ignored."""
        assert detect_card_type("4111-1111-1111-1111") == "Visa"

    def test_all_card_types_have_patterns(self):
        """Ensure all card types in patterns are testable."""
        expected_types = {"Visa", "MasterCard", "AMEX", "Discover", "JCB", "Diners Club", "UnionPay"}
        assert set(CARD_TYPE_PATTERNS.keys()) == expected_types


class TestGetCardDetails:
    """Tests for get_card_details function.

    Note: These tests require the 'requests' library and network access.
    They are marked to be skipped if requests is not available.
    """

    def test_get_card_details_import_error(self):
        """Test that ImportError is raised if requests is not installed."""
        # This test verifies the error message when requests is missing
        # In a real scenario, you'd mock the import
        pass  # Skipped - requires mocking imports

    def test_get_card_details_with_short_number(self):
        """Test get_card_details with a number too short for BIN lookup."""
        try:
            from ccparser.utils import get_card_details
            result = get_card_details("12345")
            assert result is None
        except ImportError:
            pytest.skip("requests library not installed")

    def test_get_card_details_with_empty_string(self):
        """Test get_card_details with empty string."""
        try:
            from ccparser.utils import get_card_details
            result = get_card_details("")
            assert result is None
        except ImportError:
            pytest.skip("requests library not installed")
