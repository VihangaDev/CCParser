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
        assert detect_card_type("4111111111111111000") == "Visa"  # 19-digit Visa

    def test_detect_visa_electron(self):
        """Test detecting Visa Electron cards."""
        assert detect_card_type("4026000000000001") == "Visa Electron"
        assert detect_card_type("4175000000000001") == "Visa Electron"
        assert detect_card_type("4508000000000001") == "Visa Electron"
        assert detect_card_type("4844000000000001") == "Visa Electron"
        assert detect_card_type("4913000000000001") == "Visa Electron"
        assert detect_card_type("4917000000000001") == "Visa Electron"

    def test_detect_mastercard(self):
        """Test detecting MasterCard cards."""
        # Legacy 51-55 range
        assert detect_card_type("5500000000000004") == "MasterCard"
        assert detect_card_type("5105105105105100") == "MasterCard"
        assert detect_card_type("5555555555554444") == "MasterCard"
        # 2-series range (2221-2720)
        assert detect_card_type("2221000000000009") == "MasterCard"
        assert detect_card_type("2223000000000007") == "MasterCard"
        assert detect_card_type("2300000000000003") == "MasterCard"
        assert detect_card_type("2500000000000001") == "MasterCard"
        assert detect_card_type("2720000000000005") == "MasterCard"

    def test_detect_mastercard_2series_boundaries(self):
        """Test MasterCard 2-series boundary values."""
        # Just below range - should NOT match MasterCard
        assert detect_card_type("2220000000000000") != "MasterCard"
        # Just above range - should NOT match MasterCard
        assert detect_card_type("2721000000000000") != "MasterCard"

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
        # 644-649 range
        assert detect_card_type("6440000000000000") == "Discover"
        assert detect_card_type("6490000000000000") == "Discover"
        # 622126-622925 co-brand range
        assert detect_card_type("6221260000000000") == "Discover"
        assert detect_card_type("6229250000000000") == "Discover"

    def test_detect_jcb(self):
        """Test detecting JCB cards."""
        assert detect_card_type("3530111333300000") == "JCB"
        assert detect_card_type("3566002020360505") == "JCB"
        # 15-digit JCB
        assert detect_card_type("213100000000000") == "JCB"
        assert detect_card_type("180000000000000") == "JCB"

    def test_detect_diners_club(self):
        """Test detecting Diners Club cards."""
        assert detect_card_type("30569309025904") == "Diners Club"
        assert detect_card_type("38520000023237") == "Diners Club"
        assert detect_card_type("36000000000000") == "Diners Club"

    def test_detect_unionpay(self):
        """Test detecting UnionPay cards."""
        assert detect_card_type("6200000000000005") == "UnionPay"
        assert detect_card_type("6212345678901234567") == "UnionPay"
        # 81 prefix
        assert detect_card_type("8100000000000000") == "UnionPay"
        assert detect_card_type("8100000000000000000") == "UnionPay"  # 19 digits

    def test_detect_maestro(self):
        """Test detecting Maestro cards."""
        assert detect_card_type("5018000000000000") == "Maestro"
        assert detect_card_type("5020000000000000") == "Maestro"
        assert detect_card_type("5038000000000000") == "Maestro"
        assert detect_card_type("5893000000000000") == "Maestro"
        assert detect_card_type("6304000000000000") == "Maestro"
        assert detect_card_type("6759000000000000") == "Maestro"
        assert detect_card_type("6761000000000000") == "Maestro"
        assert detect_card_type("6762000000000000") == "Maestro"
        assert detect_card_type("6763000000000000") == "Maestro"
        # 12-digit Maestro
        assert detect_card_type("501800000000") == "Maestro"
        # 19-digit Maestro
        assert detect_card_type("5018000000000000000") == "Maestro"

    def test_detect_mir(self):
        """Test detecting Mir cards."""
        assert detect_card_type("2200000000000000") == "Mir"
        assert detect_card_type("2201000000000000") == "Mir"
        assert detect_card_type("2202000000000000") == "Mir"
        assert detect_card_type("2203000000000000") == "Mir"
        assert detect_card_type("2204000000000000") == "Mir"
        # 19-digit Mir
        assert detect_card_type("2200000000000000000") == "Mir"

    def test_detect_elo(self):
        """Test detecting Elo cards."""
        assert detect_card_type("4011780000000000") == "Elo"
        assert detect_card_type("4011790000000000") == "Elo"
        assert detect_card_type("4389350000000000") == "Elo"
        assert detect_card_type("5041750000000000") == "Elo"
        assert detect_card_type("5066990000000000") == "Elo"
        assert detect_card_type("5067000000000000") == "Elo"
        assert detect_card_type("6363680000000000") == "Elo"
        assert detect_card_type("6362970000000000") == "Elo"
        assert detect_card_type("6277800000000000") == "Elo"

    def test_detect_troy(self):
        """Test detecting Troy cards."""
        assert detect_card_type("9792000000000000") == "Troy"

    def test_detect_dankort(self):
        """Test detecting Dankort cards."""
        assert detect_card_type("5019000000000000") == "Dankort"

    def test_detect_uatp(self):
        """Test detecting UATP cards."""
        assert detect_card_type("100000000000000") == "UATP"
        assert detect_card_type("199999999999999") == "UATP"

    def test_detect_humo(self):
        """Test detecting Humo cards."""
        assert detect_card_type("9860000000000000") == "Humo"

    def test_detect_uzcard(self):
        """Test detecting UzCard cards."""
        assert detect_card_type("8600000000000000") == "UzCard"

    def test_detect_verve(self):
        """Test detecting Verve cards."""
        assert detect_card_type("5060990000000000") == "Verve"
        assert detect_card_type("5061000000000000") == "Verve"
        assert detect_card_type("6500020000000000") == "Verve"
        # 19-digit Verve
        assert detect_card_type("5060990000000000000") == "Verve"

    def test_detect_instapayment(self):
        """Test detecting InstaPayment cards."""
        assert detect_card_type("6370000000000000") == "InstaPayment"
        assert detect_card_type("6380000000000000") == "InstaPayment"
        assert detect_card_type("6390000000000000") == "InstaPayment"

    def test_detect_interpayment(self):
        """Test detecting InterPayment cards."""
        assert detect_card_type("6360000000000000") == "InterPayment"

    def test_detect_lankapay(self):
        """Test detecting LankaPay cards."""
        assert detect_card_type("3571110000000000") == "LankaPay"

    def test_detect_unknown(self):
        """Test detecting unknown card types."""
        assert detect_card_type("0000000000000000") == "Unknown"
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

    def test_all_expected_card_types_have_patterns(self):
        """Ensure all expected card types are covered."""
        expected_types = {
            "Visa", "Visa Electron", "MasterCard", "AMEX", "Discover",
            "JCB", "Diners Club", "UnionPay", "Maestro", "Mir",
            "Elo", "Troy", "Dankort", "UATP", "Humo", "UzCard",
            "Verve", "InstaPayment", "InterPayment", "LankaPay",
        }
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
