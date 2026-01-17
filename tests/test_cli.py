"""Tests for the CLI module."""

import json
import subprocess
import sys


class TestCLI:
    """Tests for the ccparser CLI."""

    def test_basic_parsing(self):
        """Test basic card parsing output."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "4111111111111111|12|2030|123"],
            capture_output=True,
            text=True
        )
        assert "Card Number: 4111 1111 1111 1111" in result.stdout
        assert "Expiry Date: 12/30" in result.stdout
        assert "CVV: 123" in result.stdout
        assert "Card Type: Visa" in result.stdout
        assert "Valid: True" in result.stdout

    def test_masked_output(self):
        """Test masked card number output."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "--masked", "4111111111111111|12|2030|123"],
            capture_output=True,
            text=True
        )
        assert "**** **** **** 1111" in result.stdout
        assert "4111 1111 1111 1111" not in result.stdout

    def test_json_output(self):
        """Test JSON format output."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "--json", "4111111111111111|12|2030|123"],
            capture_output=True,
            text=True
        )
        output = json.loads(result.stdout)
        assert output['number'] == "4111111111111111"
        assert output['card_type'] == "Visa"
        assert output['is_valid'] is True

    def test_quiet_mode_valid(self):
        """Test quiet mode with valid card returns 0."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "--quiet", "4111111111111111|12|2030|123"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert result.stdout == ""

    def test_quiet_mode_invalid(self):
        """Test quiet mode with invalid card returns 1."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "--quiet", "4111111111111112|12|2030|123"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

    def test_invalid_card_error(self):
        """Test error message for invalid card format."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "invalid"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
        assert "Error" in result.stderr

    def test_version_flag(self):
        """Test --version flag."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "--version"],
            capture_output=True,
            text=True
        )
        assert "ccparser" in result.stdout.lower()

    def test_help_flag(self):
        """Test --help flag."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "--help"],
            capture_output=True,
            text=True
        )
        assert "usage" in result.stdout.lower()
        assert "--masked" in result.stdout
        assert "--json" in result.stdout

    def test_exit_code_valid_card(self):
        """Test exit code is 0 for valid card."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "4111111111111111|12|2030|123"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_exit_code_invalid_luhn(self):
        """Test exit code is 1 for invalid Luhn."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "4111111111111112|12|2030|123"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

    def test_amex_card(self):
        """Test AMEX card parsing."""
        result = subprocess.run(
            [sys.executable, "-m", "ccparser.cli", "378282246310005|12|2030|1234"],
            capture_output=True,
            text=True
        )
        assert "Card Type: AMEX" in result.stdout
        assert "3782 822463 10005" in result.stdout
