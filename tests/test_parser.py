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

    def test_parse_slash_delimited(self):
        """Test parsing slash-delimited card string."""
        card = CCParser("4060680184134946/05/29/423")
        assert card.get_number() == "4060680184134946"
        assert card.get_expiry() == "05/29"
        assert card.get_cvv() == "423"

    def test_parse_compact_expiry(self):
        """Test parsing with compact MMYY expiry format."""
        card = CCParser("4121748175166255 0727 985")
        assert card.get_expiry() == "07/27"
        assert card.get_year() == "2027"

    def test_parse_two_digit_year(self):
        """Test parsing with 2-digit year."""
        card = CCParser("4111111111111111|12|30|123")
        assert card.get_year() == "2030"

    def test_parse_four_digit_year(self):
        """Test parsing with 4-digit year."""
        card = CCParser("4111111111111111|12|2030|123")
        assert card.get_year() == "2030"

    def test_parse_labeled_multiline(self):
        """Test parsing labeled multiline card details."""
        card = CCParser(
            "4085211100141996\n"
            "Holder: Shannon Fiumano-Wagner\n"
            "CVV: 127\n"
            "EXPIRE: 04/28"
        )
        assert card.get_number() == "4085211100141996"
        assert card.get_expiry() == "04/28"
        assert card.get_cvv() == "127"

    def test_parse_labeled_variants(self):
        """Test parsing labeled variants like Exp Date and CVV2."""
        card = CCParser(
            "6225757500752952\n"
            "Exp Date  11/28\n"
            "CVV2  540\n"
            "Holder Name  Yun Xu"
        )
        assert card.get_number() == "6225757500752952"
        assert card.get_expiry() == "11/28"
        assert card.get_cvv() == "540"


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
        """Test is_valid returns False for wrong CVV length by card type."""
        card = CCParser("378282246310005|12|2030|123")  # AMEX needs 4 digits
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
        card = CCParser("378282246310005|12|2030|123")
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

    def test_invalid_cvv_length_raises(self):
        """Test that invalid CVV length raises error at parse time."""
        with pytest.raises(InvalidCVVError):
            CCParser("4111111111111111|12|2030|12")
        with pytest.raises(InvalidCVVError):
            CCParser("4111111111111111|12|2030|12345")

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


class TestCCParserFormats:
    """Tests for comprehensive format support."""

    # --- Pipe-delimited formats ---

    def test_pipe_mm_slash_yy_cvv(self):
        """Test: NUMBER|MM/YY|CVV"""
        card = CCParser("5466160505270007|09/28|094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_pipe_mm_dash_yy_cvv(self):
        """Test: NUMBER|MM-YY|CVV"""
        card = CCParser("5466160505270007|09-28|094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_pipe_mm_slash_yyyy_cvv(self):
        """Test: NUMBER|MM/YYYY|CVV"""
        card = CCParser("5466160505270007|09/2028|094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_pipe_mm_dash_yyyy_cvv(self):
        """Test: NUMBER|MM-YYYY|CVV"""
        card = CCParser("5466160505270007|09-2028|094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_pipe_mm_yy_cvv(self):
        """Test: NUMBER|MM|YY|CVV"""
        card = CCParser("5466160505270007|09|28|094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_pipe_mm_yyyy_cvv(self):
        """Test: NUMBER|MM|YYYY|CVV"""
        card = CCParser("5466160505270007|09|2028|094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    # --- Colon-delimited formats ---

    def test_colon_mm_slash_yy_cvv(self):
        """Test: NUMBER:MM/YY:CVV"""
        card = CCParser("5466160505270007:09/28:094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_colon_mm_dash_yy_cvv(self):
        """Test: NUMBER:MM-YY:CVV"""
        card = CCParser("5466160505270007:09-28:094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_colon_mm_slash_yyyy_cvv(self):
        """Test: NUMBER:MM/YYYY:CVV"""
        card = CCParser("5466160505270007:09/2028:094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_colon_mm_dash_yyyy_cvv(self):
        """Test: NUMBER:MM-YYYY:CVV"""
        card = CCParser("5466160505270007:09-2028:094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_colon_mm_yy_cvv(self):
        """Test: NUMBER:MM:YY:CVV"""
        card = CCParser("5466160505270007:09:28:094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_colon_mm_yyyy_cvv(self):
        """Test: NUMBER:MM:YYYY:CVV"""
        card = CCParser("5466160505270007:09:2028:094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    # --- Space-delimited formats ---

    def test_space_mm_slash_yy_cvv(self):
        """Test: NUMBER MM/YY CVV"""
        card = CCParser("5466160505270007 09/28 094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_space_mm_dash_yy_cvv(self):
        """Test: NUMBER MM-YY CVV"""
        card = CCParser("5466160505270007 09-28 094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_space_mm_slash_yyyy_cvv(self):
        """Test: NUMBER MM/YYYY CVV"""
        card = CCParser("5466160505270007 09/2028 094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_space_mm_dash_yyyy_cvv(self):
        """Test: NUMBER MM-YYYY CVV"""
        card = CCParser("5466160505270007 09-2028 094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_space_mm_yy_cvv(self):
        """Test: NUMBER MM YY CVV"""
        card = CCParser("5466160505270007 09 28 094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    def test_space_mm_yyyy_cvv(self):
        """Test: NUMBER MM YYYY CVV"""
        card = CCParser("5466160505270007 09 2028 094")
        assert card.get_number() == "5466160505270007"
        assert card.get_month() == "09"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "094"

    # --- Slash as delimiter (all slashes) ---

    def test_all_slash_delimited(self):
        """Test: NUMBER/MM/YY/CVV"""
        card = CCParser("4060680184134946/05/29/423")
        assert card.get_number() == "4060680184134946"
        assert card.get_month() == "05"
        assert card.get_year() == "2029"
        assert card.get_cvv() == "423"

    # --- Merged expiry format ---

    def test_merged_expiry_mmyy(self):
        """Test: NUMBER MMYY CVV"""
        card = CCParser("4121748175166255 0727 985")
        assert card.get_number() == "4121748175166255"
        assert card.get_month() == "07"
        assert card.get_year() == "2027"
        assert card.get_cvv() == "985"

    # --- Pipe with spaces around ---

    def test_pipe_with_spaces(self):
        """Test: NUMBER | MM/YY | CVV |"""
        card = CCParser("4147202769833490 | 08/30 | 761 |")
        assert card.get_number() == "4147202769833490"
        assert card.get_month() == "08"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "761"

    # --- Multi-line labeled formats ---

    def test_multiline_holder_cvv_expire(self):
        """Test multi-line with Holder/CVV/EXPIRE labels."""
        card_str = "4085211100141996\nHolder: Shannon Fiumano-Wagner\nCVV: 127\nEXPIRE: 04/28"
        card = CCParser(card_str)
        assert card.get_number() == "4085211100141996"
        assert card.get_month() == "04"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "127"

    def test_multiline_exp_date_cvv2(self):
        """Test multi-line with Exp Date/CVV2 labels."""
        card_str = "6225757500752952\nExp Date  11/28\nCVV2  540\nHolder Name  Yun Xu"
        card = CCParser(card_str)
        assert card.get_number() == "6225757500752952"
        assert card.get_month() == "11"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "540"

    def test_multiline_single_digit_month(self):
        """Test multi-line with single digit month (5/32)."""
        card_str = "6225750684795863\nExp Date  5/32\nCVV2  488\nHolder Name  N/A"
        card = CCParser(card_str)
        assert card.get_number() == "6225750684795863"
        assert card.get_month() == "05"
        assert card.get_year() == "2032"
        assert card.get_cvv() == "488"

    def test_multiline_cc_hash_exp_ccv(self):
        """Test multi-line with CC #:/Exp:/CCV: labels."""
        card_str = "CC #: 4100400037617563\n|Exp: 0329\n|CCV: 475\nName: Robert Madai"
        card = CCParser(card_str)
        assert card.get_number() == "4100400037617563"
        assert card.get_month() == "03"
        assert card.get_year() == "2029"
        assert card.get_cvv() == "475"

    def test_multiline_exp_cvc_on_separate_lines(self):
        """Test multi-line with Exp and CVC on lines after labels."""
        card_str = "5453131621011463\nExp\n11/27\nCVC\n663"
        card = CCParser(card_str)
        assert card.get_number() == "5453131621011463"
        assert card.get_month() == "11"
        assert card.get_year() == "2027"
        assert card.get_cvv() == "663"

    # --- Reversed date format (YY/MM) ---

    def test_reversed_date_yy_mm(self):
        """Test reversed date format where YY/MM is auto-detected."""
        card_str = "5264711004726313\nEXP\n27/11\nNAME\nMelissa Taylor\nCVV\n983"
        card = CCParser(card_str)
        assert card.get_number() == "5264711004726313"
        assert card.get_month() == "11"
        assert card.get_year() == "2027"
        assert card.get_cvv() == "983"


class TestCCParserHeuristic:
    """Tests for the heuristic extraction engine.

    These test formats that no fixed pattern parser could handle —
    the heuristic engine finds card data by properties (Luhn check,
    date validation, CVV length) rather than format matching.
    """

    # --- Card number with spaces/dashes (formatted cards) ---

    def test_card_with_spaces_in_number(self):
        """Test card number formatted with spaces between groups."""
        card = CCParser("4111 1111 1111 1111 12/30 123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_card_with_dashes_in_number(self):
        """Test card number formatted with dashes."""
        card = CCParser("4111-1111-1111-1111 12/30 123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    # --- Unusual delimiters ---

    def test_tab_delimited(self):
        """Test tab-separated format."""
        card = CCParser("4111111111111111\t12/30\t123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_dot_separated_expiry(self):
        """Test dot as expiry separator."""
        card = CCParser("4111111111111111 12.30 123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_multiple_spaces(self):
        """Test multiple spaces as delimiters."""
        card = CCParser("4111111111111111    12/30    123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    # --- Text blob with card data embedded ---

    def test_card_in_sentence(self):
        """Test card data mixed with surrounding text."""
        card_str = "Card: 4111111111111111 Expires: 12/30 Security Code: 123"
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_card_with_name_and_address(self):
        """Test card data mixed with name and address."""
        card_str = (
            "Name: John Smith\n"
            "4111111111111111\n"
            "Exp: 03/28\n"
            "CVV: 456\n"
            "Address: 123 Main St"
        )
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "03"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "456"

    def test_card_with_phone_number_nearby(self):
        """Test that phone numbers don't confuse the parser."""
        card_str = (
            "Phone: 555-123-4567\n"
            "CC: 4111111111111111\n"
            "Exp: 06/29\n"
            "CVV: 789"
        )
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "06"
        assert card.get_year() == "2029"
        assert card.get_cvv() == "789"

    # --- Various label styles ---

    def test_valid_thru_label(self):
        """Test 'Valid thru' as expiry label."""
        card_str = "4111111111111111\nValid thru: 05/29\nCVV: 321"
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "05"
        assert card.get_year() == "2029"
        assert card.get_cvv() == "321"

    def test_good_thru_label(self):
        """Test 'Good thru' as expiry label."""
        card_str = "4111111111111111\nGood Thru 08/30\nSecurity Code 555"
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "08"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "555"

    def test_cid_label(self):
        """Test 'CID' as CVV label (AMEX style)."""
        card_str = "378282246310005\nExp 12/28\nCID 1234"
        card = CCParser(card_str)
        assert card.get_number() == "378282246310005"
        assert card.get_month() == "12"
        assert card.get_year() == "2028"
        assert card.get_cvv() == "1234"

    # --- No explicit labels ---

    def test_just_numbers_with_newlines(self):
        """Test card data as just numbers on separate lines."""
        card_str = "4111111111111111\n12/30\n123"
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_numbers_with_mixed_separators(self):
        """Test unusual mixed separator format."""
        card_str = "4111111111111111;12-30;123"
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    # --- Edge cases ---

    def test_amex_with_4digit_cvv(self):
        """Test AMEX card with 4-digit CVV extraction."""
        card_str = "378282246310005 09/29 1234"
        card = CCParser(card_str)
        assert card.get_number() == "378282246310005"
        assert card.get_month() == "09"
        assert card.get_year() == "2029"
        assert card.get_cvv() == "1234"

    def test_card_number_not_at_start(self):
        """Test card number appearing in the middle of text."""
        card_str = "My card is 4111111111111111 exp 10/30 cvv 456"
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "10"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "456"

    def test_full_year_in_expiry(self):
        """Test 4-digit year in heuristic mode."""
        card_str = "Number: 4111111111111111\nExpiry: 03/2029\nCVV: 741"
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "03"
        assert card.get_year() == "2029"
        assert card.get_cvv() == "741"

    def test_minimal_text_no_labels(self):
        """Test absolute minimal format - just numbers."""
        card_str = "4111111111111111 1230 123"
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_extra_whitespace_everywhere(self):
        """Test with excessive whitespace."""
        card_str = "  4111111111111111   \n\n  Exp:  12 / 30  \n\n  CVV:  123  "
        card = CCParser(card_str)
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    # --- Unusual delimiter tests ---

    def test_semicolon_delimiter(self):
        """Test semicolons as delimiters."""
        card = CCParser("4111111111111111;12;30;123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_equals_delimiter(self):
        """Test equals signs as delimiters."""
        card = CCParser("4111111111111111=12=30=123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_underscore_delimiter(self):
        """Test underscores as delimiters."""
        card = CCParser("4111111111111111_12_30_123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_hash_delimiter(self):
        """Test hash signs as delimiters."""
        card = CCParser("4111111111111111#12#30#123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_tilde_delimiter(self):
        """Test tildes as delimiters."""
        card = CCParser("4111111111111111~12~30~123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    # --- Year-first date format ---

    def test_yyyy_mm_format(self):
        """Test YYYY/MM date format."""
        card = CCParser("4111111111111111 2030/12 123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_yyyy_dash_mm_format(self):
        """Test YYYY-MM date format."""
        card = CCParser("4111111111111111 2030-12 123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    # --- Parenthesized/wrapped values ---

    def test_parenthesized_cvv(self):
        """Test CVV wrapped in parentheses."""
        card = CCParser("4111111111111111 12/30 (123)")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_bracketed_cvv(self):
        """Test CVV wrapped in square brackets."""
        card = CCParser("4111111111111111 12/30 [123]")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    # --- Trailing text ---

    def test_trailing_name_after_cvv(self):
        """Test trailing text (name) after CVV."""
        card = CCParser("4111111111111111|12|30|123 - John Doe")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    # --- Card number without separator before expiry ---

    def test_merged_card_and_expiry(self):
        """Test card number directly followed by expiry with slash."""
        card = CCParser("411111111111111112/30/123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_comma_delimiter(self):
        """Test commas as delimiters (CSV format)."""
        card = CCParser("4111111111111111,12,30,123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_non_luhn_number_skipped(self):
        """Test that non-Luhn digit sequences are skipped in favor of valid ones."""
        card = CCParser("Phone: 1234567890123456 CC: 4111111111111111 exp 12/30 cvv 123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_prose_with_punctuation(self):
        """Test card data embedded in prose with commas and periods."""
        card = CCParser("Charge card 4111111111111111, exp 12/30, CVV 123.")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_merged_expiry_cvv_mmyy(self):
        """Test merged MMYY+CVV with no separator between them."""
        card = CCParser("4111111111111111 1230123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_merged_expiry_cvv_mmyyyy(self):
        """Test merged MMYYYY+CVV with no separator between them."""
        card = CCParser("4111111111111111 122030123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

    def test_prose_with_labeled_cvv_and_noise(self):
        """Test prose with non-CVV numbers before the actual labeled CVV."""
        card = CCParser("4111111111111111 12/30 Rate: 4.5 Code: 789 CVV: 123")
        assert card.get_number() == "4111111111111111"
        assert card.get_month() == "12"
        assert card.get_year() == "2030"
        assert card.get_cvv() == "123"

