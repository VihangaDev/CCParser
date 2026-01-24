"""
Credit card parsing module.

This module provides the main CCParser class for parsing, validating,
and extracting credit card information from strings.
"""

import re
import datetime
from typing import Optional

from .validator import validate_card_number, validate_expiry_date, validate_cvv
from .formatter import format_card_number, mask_card_number
from .utils import detect_card_type, get_card_details


class CCParserError(Exception):
    """Base exception for all CCParser errors."""
    pass


class InvalidCardNumberError(CCParserError):
    """Raised when a card number is invalid or malformed."""
    pass


class InvalidExpiryDateError(CCParserError):
    """Raised when an expiry date is invalid or malformed."""
    pass


class InvalidCVVError(CCParserError):
    """Raised when a CVV is invalid or malformed."""
    pass


class CCParser:
    """
    Parse and validate credit card strings.

    The CCParser class extracts card details from various string formats
    and provides methods for validation, formatting, and card type detection.

    Supported formats:
        - 4111111111111111|12/30|123
        - 4111111111111111|12|2030|123
        - 4111111111111111|12|30|123
        - 4111111111111111 12 2030 123
        - 4111111111111111:12:2030:123
        - Labeled/multi-line formats (Exp/CVV labels)

    Attributes:
        card_number: The extracted card number.
        expiry_month: The expiry month (01-12).
        expiry_year: The expiry year (YYYY format).
        cvv: The CVV/CVC code.

    Example:
        >>> card = CCParser("4111111111111111|12|2030|123")
        >>> card.get_number()
        '4111111111111111'
        >>> card.get_card_type()
        'Visa'
        >>> card.is_valid()
        True
    """

    def __init__(self, card_string: str):
        """
        Initialize CCParser with a card string.

        Args:
            card_string: The credit card string to parse.

        Raises:
            InvalidCardNumberError: If the card string format is invalid.
            InvalidExpiryDateError: If the expiry date format is invalid.
        """
        if not card_string or not isinstance(card_string, str):
            raise InvalidCardNumberError("Card string cannot be empty")

        self.card_string = card_string.strip()
        self.card_number, self.expiry_month, self.expiry_year, self.cvv = self._parse_card_string(
            self.card_string,
        )

    def _parse_card_string(self, card_string: str) -> tuple[str, str, str, str]:
        """
        Parse the card string into its components.

        Supports a wide variety of formats including:
        - Single-line delimited: NUMBER|MM|YY|CVV, NUMBER|MM/YY|CVV, etc.
        - Slash/dash/space/colon/pipe as delimiters
        - Combined expiry: NUMBER MMYY CVV or NUMBER MM/YY CVV
        - Multi-line labeled: card number with labeled Exp/CVV fields
        - Reversed dates: YY/MM format (auto-detected)
        - Merged expiry without separator: 0727 meaning 07/27

        Args:
            card_string: The card string to parse.

        Returns:
            A tuple of (card_number, expiry_month, expiry_year, cvv).

        Raises:
            InvalidCardNumberError: If the format is invalid.
            InvalidExpiryDateError: If the expiry date format is invalid.
        """
        card_number = None
        expiry_month = None
        expiry_year = None
        cvv = None

        # Normalize unusual delimiters/wrappers early so all strategies benefit
        card_string = re.sub(r"[;=~#_\(\)\[\]\{\},]+", " ", card_string).strip()

        # Strategy 1: Try multi-line/labeled format parsing
        parsed = self._parse_labeled_format(card_string)
        if parsed:
            card_number, expiry_month, expiry_year, cvv = parsed
        else:
            # Strategy 2: Single-line format parsing
            try:
                card_number, expiry_month, expiry_year, cvv = self._parse_single_line(card_string)
            except (InvalidCardNumberError, InvalidExpiryDateError):
                # Strategy 3: Heuristic extraction (handles any format)
                result = self._extract_heuristic(card_string)
                if result:
                    card_number, expiry_month, expiry_year, cvv = result
                else:
                    raise InvalidCardNumberError(
                        "Could not extract card data. Expected a 13-19 digit card number, "
                        "expiry date, and CVV."
                    )

        # Normalize month/year and validate
        expiry_month, expiry_year = self._normalize_expiry(expiry_month, expiry_year)

        # Validate card number contains only digits
        if not card_number.isdigit():
            raise InvalidCardNumberError("Card number must contain only digits")

        # Validate CVV contains only digits
        if not cvv.isdigit():
            raise InvalidCVVError("CVV must contain only digits")

        # Validate CVV length at parse time
        if len(cvv) not in (3, 4):
            raise InvalidCVVError("CVV must be 3 or 4 digits")

        return card_number, expiry_month, expiry_year, cvv

    def _parse_labeled_format(self, raw: str) -> Optional[tuple[str, str, str, str]]:
        """
        Parse multi-line or labeled card formats.

        Handles formats like:
            4085211100141996
            Holder: Shannon Fiumano-Wagner
            CVV: 127
            EXPIRE: 04/28

            CC #: 4100400037617563
            |Exp: 0329
            |CCV: 475
        """
        # Find card number (13-19 digit sequence that passes Luhn check)
        card_match = None
        for m in re.finditer(r"(?<!\d)(\d{13,19})(?!\d)", raw):
            if self._luhn_check(m.group(1)):
                card_match = m
                break
        if not card_match:
            return None

        # Find CVV (labeled with cvv/cvc/ccv/cvv2/cvc2)
        cvv_match = re.search(
            r"(?:cvv2?|cvc2?|ccv2?|security\s*code)\s*[:\s#|]*\s*(\d{3,4})",
            raw, re.IGNORECASE
        )

        # Find expiry date (labeled with exp/expire/expiry/exp date)
        exp_match = re.search(
            r"(?:exp(?:iry|ire)?(?:\s*date)?|expire[sd]?)\s*[:\s#|]*\s*"
            r"(\d{1,2})\s*[/\-.\s]\s*(\d{2,4})",
            raw, re.IGNORECASE
        )

        # Also try MMYY or MMYYYY merged format after exp label
        if not exp_match:
            exp_match_merged = re.search(
                r"(?:exp(?:iry|ire)?(?:\s*date)?|expire[sd]?)\s*[:\s#|]*\s*"
                r"(\d{4,6})",
                raw, re.IGNORECASE
            )
            if exp_match_merged:
                merged = exp_match_merged.group(1)
                if len(merged) == 4:
                    month_str, year_str = merged[:2], merged[2:]
                elif len(merged) == 6:
                    month_str, year_str = merged[:2], merged[2:]
                else:
                    month_str, year_str = None, None

                if month_str and year_str:
                    if not (card_match and cvv_match):
                        return None
                    return (
                        card_match.group(0),
                        month_str,
                        year_str,
                        cvv_match.group(1),
                    )

        if not (card_match and cvv_match and exp_match):
            return None

        return (
            card_match.group(0),
            exp_match.group(1),
            exp_match.group(2),
            cvv_match.group(1),
        )

    def _parse_single_line(self, card_string: str) -> tuple[str, str, str, str]:
        """
        Parse single-line card formats with various delimiters.

        Handles formats like:
            5466160505270007|09/28|094
            5466160505270007|09-28|094
            5466160505270007|09|28|094
            5466160505270007:09:2028:094
            5466160505270007 09 28 094
            4060680184134946/05/29/423
            4121748175166255 0727 985
            4147202769833490 | 08/30 | 761 |
        """
        # First, extract the card number from the beginning
        card_match = re.match(r"\s*(\d{13,19})", card_string)
        if not card_match:
            raise InvalidCardNumberError(
                "Invalid card string format. Could not find a valid card number (13-19 digits)"
            )

        card_number = card_match.group(1)
        remainder = card_string[card_match.end():].strip()

        # Strip leading delimiters from remainder (including unusual ones)
        remainder = re.sub(r"^[\s|:/\-;=~#_]+", "", remainder)

        # Now parse the remainder for expiry and CVV
        # Try various patterns on the remainder

        # Delimiter character class used across patterns
        # Includes: | : / - ; = ~ # _ and whitespace
        _D = r"[|:\s/\-;=~#_]"
        tail = rf"(?:{_D}.*)?$"

        # Pattern A0: YYYY/MM followed by delimiter and CVV (year-first format)
        # e.g., "2030/12 123" or "2030-12|123"
        match = re.match(
            rf"(\d{{4}})\s*[/\-]\s*(\d{{1,2}})\s*{_D}+\s*(\d{{2,4}})\s*{tail}",
            remainder
        )
        if match:
            year, month, cvv = match.group(1), match.group(2), match.group(3)
            try:
                if 1 <= int(month) <= 12 and 2000 <= int(year) <= 2099:
                    return card_number, month, year, cvv
            except ValueError:
                pass

        # Pattern A: MM/YY or MM/YYYY or MM-YY or MM-YYYY followed by delimiter and CVV
        # e.g., "09/28|094" or "09-2028:094" or "08/30 | 761 |"
        match = re.match(
            rf"(\d{{1,2}})\s*[/\-]\s*(\d{{2,4}})\s*{_D}+\s*(\d{{2,4}})\s*{tail}",
            remainder
        )
        if match:
            return card_number, match.group(1), match.group(2), match.group(3)

        # Pattern B: MMYY or MMYYYY (merged) followed by delimiter and CVV
        # e.g., "0727 985" or "0329|475"
        match = re.match(
            rf"(\d{{4,6}})\s*{_D}+\s*(\d{{2,4}})\s*{tail}",
            remainder
        )
        if match:
            merged = match.group(1)
            cvv = match.group(2)
            if len(merged) in (4, 6):
                return card_number, merged[:2], merged[2:], cvv

        # Pattern C: MM delimiter YY/YYYY delimiter CVV (all separated)
        # e.g., "09|28|094" or "09:2028:094" or "09 28 094"
        match = re.match(
            rf"(\d{{1,2}})\s*{_D}+\s*(\d{{2,4}})\s*{_D}+\s*(\d{{2,4}})\s*{tail}",
            remainder
        )
        if match:
            return card_number, match.group(1), match.group(2), match.group(3)

        # Pattern D: Just slash-separated (card was followed by /MM/YY/CVV)
        # e.g., "05/29/423" or "05-29-423"
        match = re.match(
            rf"(\d{{1,2}})\s*[/\-]\s*(\d{{2,4}})\s*[/\-]\s*(\d{{2,4}})\s*{tail}",
            remainder
        )
        if match:
            return card_number, match.group(1), match.group(2), match.group(3)

        # Pattern E: Non-numeric or too-short CVV (still parse it, let validator reject)
        # e.g., "12|2030|ABC" or "12|2030|12"
        # Only match if remainder is short (< 20 chars) to avoid matching prose text
        if len(remainder) < 20:
            match = re.match(
                rf"(\d{{1,2}})\s*{_D}+\s*(\d{{2,4}})\s*{_D}+\s*(\S+)\s*{tail}",
                remainder
            )
            if match:
                return card_number, match.group(1), match.group(2), match.group(3)

        raise InvalidCardNumberError(
            "Invalid card string format. Expected: NUMBER|MM|YYYY|CVV or NUMBER|MM/YY|CVV"
        )

    def _normalize_expiry(self, expiry_month: str, expiry_year: str) -> tuple[str, str]:
        """
        Normalize and validate expiry month and year.

        Handles:
        - Auto-detection of reversed dates (YY/MM where month > 12)
        - 2-digit to 4-digit year conversion
        - Month padding to 2 digits

        Returns:
            Tuple of (normalized_month, normalized_year).
        """
        try:
            month_int = int(expiry_month)
            year_int = int(expiry_year)
        except ValueError:
            raise InvalidExpiryDateError(
                f"Invalid expiry date: {expiry_month}/{expiry_year}. Must be numeric"
            )

        # Auto-detect reversed date format (YY/MM)
        # If "month" > 12 and "year" <= 12, they're likely swapped
        if month_int > 12 and len(expiry_month) == 2 and year_int <= 12:
            month_int, year_int = year_int, month_int
            expiry_month = str(month_int)
            expiry_year = str(year_int)

        # Validate month
        if month_int < 1 or month_int > 12:
            raise InvalidExpiryDateError(f"Invalid month: {expiry_month}. Must be 01-12")

        expiry_month = f"{month_int:02d}"

        # Normalize year to 4 digits
        if len(expiry_year) <= 2:
            expiry_year = "20" + expiry_year.zfill(2)
        elif len(expiry_year) == 4:
            pass  # Already 4 digits
        else:
            raise InvalidExpiryDateError(f"Invalid year: {expiry_year}. Use YY or YYYY format")

        return expiry_month, expiry_year

    @staticmethod
    def _luhn_check(number: str) -> bool:
        """Fast Luhn checksum validation for candidate filtering."""
        if not number or not number.isdigit():
            return False
        digits = [int(d) for d in number]
        odd = digits[-1::-2]
        even = digits[-2::-2]
        total = sum(odd)
        for d in even:
            d *= 2
            total += d - 9 if d > 9 else d
        return total % 10 == 0

    def _extract_heuristic(self, raw: str) -> Optional[tuple[str, str, str, str]]:
        """
        Heuristic extraction engine that finds card data in any text format.

        Instead of matching fixed patterns, this method finds card components
        by their intrinsic properties:
        - Card number: 13-19 digit sequence passing Luhn checksum
        - Expiry: date-like pattern with month 01-12 and plausible year
        - CVV: 3-4 digit number that isn't the card number or expiry

        Works on any text blob regardless of delimiters, labels, or layout.
        """
        # Normalize unusual delimiters to spaces for uniform parsing
        # Keep / - . : as they have semantic meaning in dates/labels
        normalized = re.sub(r"[;=~#_\(\)\[\]\{\},]+", " ", raw)

        # Step 1: Find card number (Luhn-valid 13-19 digit sequence)
        card_number = self._find_card_number(normalized)
        if not card_number:
            return None

        # Remove card number from text for remaining extraction
        # Replace with placeholder to preserve positions
        remaining = normalized.replace(card_number, " " * len(card_number), 1)
        # Also handle the case where card was found as grouped (with spaces/dashes)
        # by removing the original formatted version from raw
        for fmt in [card_number]:
            # Try removing continuous digits
            remaining = re.sub(re.escape(fmt), " " * len(fmt), remaining, count=1)

        # Step 2: Find expiry date
        expiry_result = self._find_expiry(remaining)
        if not expiry_result:
            return None
        expiry_month, expiry_year, expiry_text = expiry_result

        # Remove expiry text from remaining
        remaining = remaining.replace(expiry_text, " " * len(expiry_text), 1)

        # Step 3: Find CVV
        cvv = self._find_cvv(remaining, card_number)
        if not cvv:
            return None

        return card_number, expiry_month, expiry_year, cvv

    def _find_card_number(self, raw: str) -> Optional[str]:
        """
        Find a valid card number in arbitrary text.

        Looks for 13-19 digit sequences (allowing spaces/dashes between groups)
        and validates with Luhn checksum.
        """
        # First try: find formatted card numbers (digit groups separated by spaces/dashes)
        # e.g., "4111 1111 1111 1111" or "4111-1111-1111-1111" or "3782 822463 10005"
        # Require groups of 4+ digits separated by single space or dash
        grouped_pattern = re.finditer(
            r"(?<!\d)(\d{4,6}(?:[\s\-]\d{4,6}){2,4})(?!\d)",
            raw
        )
        for match in grouped_pattern:
            digits = re.sub(r"[\s\-]", "", match.group(1))
            if 13 <= len(digits) <= 19 and self._luhn_check(digits):
                return digits

        # Second try: find raw continuous digit sequences
        digit_sequences = re.finditer(r"(?<!\d)(\d{13,19})(?!\d)", raw)
        for match in digit_sequences:
            if self._luhn_check(match.group(1)):
                return match.group(1)

        # Third try: handle merged card+expiry+cvv (no separators at all)
        # e.g., "411111111111111112/30/123" or "411111111111111112301234"
        # Find long digit sequences and try to extract a Luhn-valid card number from the start
        long_sequences = re.finditer(r"(?<!\d)(\d{16,})(?!\d)", raw)
        for match in long_sequences:
            seq = match.group(1)
            # Try card lengths from 19 down to 13
            for length in range(min(19, len(seq)), 12, -1):
                candidate = seq[:length]
                if self._luhn_check(candidate):
                    return candidate

        return None

    def _find_expiry(self, text: str) -> Optional[tuple[str, str, str]]:
        """
        Find an expiry date in text. Returns (month, year, matched_text) or None.

        Searches for date patterns in priority order:
        1. Labeled dates (Exp: MM/YY, Valid thru: MM/YY, etc.)
        2. Separated dates (MM/YY, MM-YY, MM.YY)
        3. Merged dates (MMYY, MMYYYY)
        4. Bare digit pairs that form valid month+year
        """
        current_year = datetime.datetime.now().year % 100  # 2-digit current year

        # Priority 1: Labeled expiry (most reliable)
        label_patterns = [
            # "Exp: 04/28", "EXPIRE: 04/28", "Exp Date 11/28", "Valid thru 04/28"
            r"(?:exp(?:iry|ire)?(?:\s*date)?|expire[sd]?|valid(?:\s*thru)?|good\s*thru)"
            r"\s*[:\s#|/\-]*\s*"
            r"(\d{1,2})\s*[/\-.\s]\s*(\d{2,4})",
        ]
        for pattern in label_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                month, year = match.group(1), match.group(2)
                if self._is_valid_expiry(month, year, current_year):
                    return month, year, match.group(0)

        # Priority 1b: Labeled merged expiry ("Exp: 0329", "Exp 0428")
        merged_label = re.search(
            r"(?:exp(?:iry|ire)?(?:\s*date)?|expire[sd]?|valid(?:\s*thru)?)"
            r"\s*[:\s#|]*\s*"
            r"(\d{4,6})",
            text, re.IGNORECASE
        )
        if merged_label:
            merged = merged_label.group(1)
            month, year = merged[:2], merged[2:]
            if self._is_valid_expiry(month, year, current_year):
                return month, year, merged_label.group(0)

        # Priority 2: Separated date patterns (MM/YY, MM-YY, MM.YY, YYYY/MM)
        sep_matches = re.finditer(
            r"(?<!\d)(\d{1,4})\s*[/\-.]\s*(\d{1,4})(?!\d)",
            text
        )
        for match in sep_matches:
            a, b = match.group(1), match.group(2)
            # Try MM/YY or MM/YYYY (standard order)
            if self._is_valid_expiry(a, b, current_year):
                return a, b, match.group(0)
            # Try YYYY/MM or YY/MM (reversed order)
            if self._is_valid_expiry(b, a, current_year):
                return b, a, match.group(0)

        # Priority 3: Merged MMYY or MMYYYY (4 or 6 digit sequences that aren't card/cvv)
        merged_matches = re.finditer(r"(?<!\d)(\d{4,6})(?!\d)", text)
        for match in merged_matches:
            merged = match.group(1)
            if len(merged) in (4, 6):
                month, year = merged[:2], merged[2:]
                if self._is_valid_expiry(month, year, current_year):
                    return month, year, match.group(0)

        # Priority 4: Two separate small numbers that form valid month+year
        # e.g., "09 28" or "12\n2030"
        pair_matches = re.finditer(
            r"(?<!\d)(\d{1,2})\s+(\d{2,4})(?!\d)",
            text
        )
        for match in pair_matches:
            month, year = match.group(1), match.group(2)
            if self._is_valid_expiry(month, year, current_year):
                return month, year, match.group(0)
            # Try reversed
            if len(month) == 2 and int(month) > 12 and self._is_valid_expiry(year, month, current_year):
                return year, month, match.group(0)

        # Priority 5: Digit blob containing merged expiry+CVV (e.g., "1230123" = MMYY + CVV)
        # Try to split 7-10 digit sequences as MMYYYY(6) + CVV(3-4) or MMYY(4) + CVV(3-4)
        blob_matches = re.finditer(r"(?<!\d)(\d{7,10})(?!\d)", text)
        for match in blob_matches:
            blob = match.group(1)
            # Try MMYYYY + CVV first (more specific, 6 + 3 or 6 + 4)
            if len(blob) >= 9:
                month, year = blob[:2], blob[2:6]
                if self._is_valid_expiry(month, year, current_year):
                    return month, year, blob[:6]
            # Fall back to MMYY + CVV (4 + 3 or 4 + 4)
            if len(blob) >= 7:
                month, year = blob[:2], blob[2:4]
                if self._is_valid_expiry(month, year, current_year):
                    return month, year, blob[:4]

        return None

    def _is_valid_expiry(self, month_str: str, year_str: str, current_year_2d: int) -> bool:
        """Check if month/year form a plausible expiry date."""
        try:
            month = int(month_str)
            year = int(year_str)
        except (ValueError, TypeError):
            return False

        if month < 1 or month > 12:
            return False

        # Normalize year for comparison
        if len(year_str) == 2:
            # 2-digit year: interpret as 20xx and check if within reasonable range
            full_year = 2000 + year
            current_full = 2000 + current_year_2d
            return (current_full - 2) <= full_year <= (current_full + 20)
        elif len(year_str) == 4:
            current_full = 2000 + current_year_2d
            return (current_full - 2) <= year <= (current_full + 20)

        return False

    def _find_cvv(self, text: str, card_number: str) -> Optional[str]:
        """
        Find CVV in remaining text after card number and expiry are removed.

        Priority:
        1. Labeled CVV (CVV: 123, CVC: 1234, etc.)
        2. 3-digit numbers (most common CVV length)
        3. 4-digit numbers (AMEX)
        """
        # Priority 1: Labeled CVV
        cvv_labeled = re.search(
            r"(?:cvv2?|cvc2?|ccv2?|cid|security\s*code|sec(?:urity)?\s*#?)"
            r"\s*[:\s#|]*\s*(\d{3,4})",
            text, re.IGNORECASE
        )
        if cvv_labeled:
            return cvv_labeled.group(1)

        # Priority 2 & 3: Find all 3-4 digit numbers, prefer 3-digit
        all_numbers = re.findall(r"(?<!\d)(\d{3,4})(?!\d)", text)

        # Filter out numbers that are substrings of the card number
        candidates = [n for n in all_numbers if n not in card_number]

        # Prefer 3-digit candidates
        three_digit = [n for n in candidates if len(n) == 3]
        if three_digit:
            return three_digit[0]

        four_digit = [n for n in candidates if len(n) == 4]
        if four_digit:
            return four_digit[0]

        # Last resort: any 3-4 digit number
        if candidates:
            return candidates[0]

        return None

    def get_number(self) -> str:
        """
        Get the raw card number.

        Returns:
            The unformatted card number string.
        """
        return self.card_number

    def get_formatted_number(self) -> str:
        """
        Get the formatted card number with spaces.

        Returns:
            The card number formatted with spaces (e.g., '4111 1111 1111 1111').
        """
        return format_card_number(self.card_number)

    def get_expiry(self) -> str:
        """
        Get the expiry date in MM/YY format.

        Returns:
            The expiry date string (e.g., '12/30').
        """
        return f"{self.expiry_month}/{self.expiry_year[2:]}"

    def get_expiry_full(self) -> str:
        """
        Get the expiry date in MM/YYYY format.

        Returns:
            The full expiry date string (e.g., '12/2030').
        """
        return f"{self.expiry_month}/{self.expiry_year}"

    def get_year(self) -> str:
        """
        Get the expiry year.

        Returns:
            The 4-digit expiry year (e.g., '2030').
        """
        return self.expiry_year

    def get_month(self) -> str:
        """
        Get the expiry month.

        Returns:
            The 2-digit expiry month (e.g., '12').
        """
        return self.expiry_month

    def get_cvv(self) -> str:
        """
        Get the CVV code.

        Returns:
            The CVV/CVC code string.
        """
        return self.cvv

    def is_valid(self) -> bool:
        """
        Check if the card data is valid.

        Validates the card number (Luhn check), expiry date (not expired),
        and CVV length (3 or 4 digits depending on card type).

        Returns:
            True if all validations pass, False otherwise.

        Note:
            This method returns False instead of raising exceptions for
            validation failures. Use validate() if you need detailed
            error information.
        """
        try:
            if not validate_card_number(self.card_number):
                return False
            if not validate_expiry_date(self.expiry_month, self.expiry_year):
                return False
            if not validate_cvv(self.cvv, self.card_number):
                return False
            return True
        except Exception:
            return False

    def validate(self) -> None:
        """
        Validate the card data and raise exceptions on failure.

        Raises:
            InvalidCardNumberError: If the card number fails Luhn validation.
            InvalidExpiryDateError: If the card has expired.
            InvalidCVVError: If the CVV length is incorrect for the card type.
        """
        if not validate_card_number(self.card_number):
            raise InvalidCardNumberError("Card number failed Luhn validation")
        if not validate_expiry_date(self.expiry_month, self.expiry_year):
            raise InvalidExpiryDateError("Card has expired or expiry date is invalid")
        if not validate_cvv(self.cvv, self.card_number):
            raise InvalidCVVError(
                f"Invalid CVV length. Expected {'4' if detect_card_type(self.card_number) == 'AMEX' else '3'} digits"
            )

    def get_card_type(self) -> str:
        """
        Detect and return the card type.

        Returns:
            The card type name (e.g., 'Visa', 'MasterCard', 'AMEX'),
            or 'Unknown' if not recognized.
        """
        return detect_card_type(self.card_number)

    def get_masked_number(self) -> str:
        """
        Get the masked card number.

        Returns:
            The card number with most digits masked
            (e.g., '**** **** **** 1111').
        """
        return mask_card_number(self.card_number)

    def get_card_details(self) -> Optional[dict]:
        """
        Fetch detailed card information from BIN lookup.

        This method requires the 'requests' library. Install with:
        pip install ccparser[api]

        Returns:
            A dictionary with card details (bank, country, etc.),
            or None if lookup fails.

        Raises:
            ImportError: If 'requests' is not installed.
        """
        return get_card_details(self.card_number)

    def to_dict(self) -> dict:
        """
        Convert card data to a dictionary.

        Returns:
            A dictionary containing all card information.
        """
        return {
            'number': self.card_number,
            'formatted_number': self.get_formatted_number(),
            'masked_number': self.get_masked_number(),
            'expiry': self.get_expiry(),
            'expiry_month': self.expiry_month,
            'expiry_year': self.expiry_year,
            'cvv': self.cvv,
            'card_type': self.get_card_type(),
            'is_valid': self.is_valid()
        }

    def __repr__(self) -> str:
        """Return a string representation of the CCParser object."""
        return f"CCParser(type={self.get_card_type()}, masked={self.get_masked_number()})"

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"{self.get_card_type()} {self.get_masked_number()} (exp: {self.get_expiry()})"
