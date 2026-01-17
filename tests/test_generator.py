"""Tests for the generator module."""

import pytest
from ccparser.generator import generate_card_number, get_supported_card_types
from ccparser.validator import validate_card_number
from ccparser.utils import detect_card_type


class TestGenerateCardNumber:
    """Tests for generate_card_number function."""

    def test_generate_all_card_types(self):
        """Test generating valid card numbers for all supported types."""
        card_types = ["Visa", "MasterCard", "AMEX", "Discover", "JCB", "Diners Club", "UnionPay"]
        for card_type in card_types:
            card_number = generate_card_number(card_type)
            assert validate_card_number(card_number) is True
            assert detect_card_type(card_number) == card_type

    def test_generate_visa(self):
        """Test generating Visa card."""
        card_number = generate_card_number("Visa")
        assert len(card_number) == 16
        assert card_number.startswith("4")
        assert validate_card_number(card_number) is True

    def test_generate_mastercard(self):
        """Test generating MasterCard."""
        card_number = generate_card_number("MasterCard")
        assert len(card_number) == 16
        assert card_number[0:2] in ["51", "52", "53", "54", "55"]
        assert validate_card_number(card_number) is True

    def test_generate_amex(self):
        """Test generating AMEX card."""
        card_number = generate_card_number("AMEX")
        assert len(card_number) == 15
        assert card_number[0:2] in ["34", "37"]
        assert validate_card_number(card_number) is True

    def test_generate_diners_club(self):
        """Test generating Diners Club card."""
        card_number = generate_card_number("Diners Club")
        assert len(card_number) == 14
        assert validate_card_number(card_number) is True

    def test_generate_discover(self):
        """Test generating Discover card."""
        card_number = generate_card_number("Discover")
        assert len(card_number) == 16
        assert validate_card_number(card_number) is True

    def test_generate_jcb(self):
        """Test generating JCB card."""
        card_number = generate_card_number("JCB")
        assert len(card_number) == 16
        assert validate_card_number(card_number) is True

    def test_generate_unionpay(self):
        """Test generating UnionPay card."""
        card_number = generate_card_number("UnionPay")
        assert len(card_number) == 16
        assert card_number.startswith("62")
        assert validate_card_number(card_number) is True

    def test_unsupported_card_type_raises(self):
        """Test that unsupported card type raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            generate_card_number("InvalidType")
        assert "Unsupported card type" in str(exc_info.value)
        assert "InvalidType" in str(exc_info.value)

    def test_reproducible_with_seed(self):
        """Test that same seed produces same card number."""
        card1 = generate_card_number("Visa", seed=42)
        card2 = generate_card_number("Visa", seed=42)
        assert card1 == card2

    def test_different_seeds_produce_different_cards(self):
        """Test that different seeds produce different card numbers."""
        card1 = generate_card_number("Visa", seed=42)
        card2 = generate_card_number("Visa", seed=43)
        assert card1 != card2

    def test_multiple_generations_are_different(self):
        """Test that multiple generations without seed are different."""
        cards = [generate_card_number("Visa") for _ in range(10)]
        # All cards should be unique (extremely unlikely to have duplicates)
        assert len(set(cards)) == len(cards)


class TestGetSupportedCardTypes:
    """Tests for get_supported_card_types function."""

    def test_returns_list(self):
        """Test that function returns a list."""
        result = get_supported_card_types()
        assert isinstance(result, list)

    def test_contains_expected_types(self):
        """Test that all expected card types are included."""
        result = get_supported_card_types()
        expected = ["AMEX", "Diners Club", "Discover", "JCB", "MasterCard", "UnionPay", "Visa"]
        assert result == expected

    def test_list_is_sorted(self):
        """Test that the list is sorted alphabetically."""
        result = get_supported_card_types()
        assert result == sorted(result)
