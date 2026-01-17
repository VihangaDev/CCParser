"""
Command-line interface for CCParser.

Usage:
    ccparser "4111111111111111|12|2030|123"
    ccparser --masked "4111111111111111|12|2030|123"
    ccparser --json "4111111111111111|12|2030|123"
"""

import argparse
import json
import sys

from . import __version__
from .parser import CCParser, CCParserError


def main() -> int:
    """
    Main entry point for the CCParser CLI.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        prog="ccparser",
        description="Parse, validate, and format credit card strings.",
        epilog="Example: ccparser '4111111111111111|12|2030|123'"
    )

    parser.add_argument(
        "card_string",
        help="Credit card string to parse (format: NUMBER|MM|YYYY|CVV or NUMBER|MM/YY|CVV)"
    )

    parser.add_argument(
        "-m", "--masked",
        action="store_true",
        help="Show masked card number instead of full number"
    )

    parser.add_argument(
        "-j", "--json",
        action="store_true",
        dest="json_output",
        help="Output in JSON format"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Only show validation result (exit code 0 if valid, 1 if invalid)"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    try:
        card = CCParser(args.card_string)

        # Quiet mode - just validate and exit
        if args.quiet:
            return 0 if card.is_valid() else 1

        # JSON output
        if args.json_output:
            output = card.to_dict()
            if args.masked:
                output['number'] = output['masked_number']
            print(json.dumps(output, indent=2))
            return 0

        # Standard output
        if args.masked:
            print(f"Card Number: {card.get_masked_number()}")
        else:
            print(f"Card Number: {card.get_formatted_number()}")

        print(f"Expiry Date: {card.get_expiry()}")
        print(f"CVV: {card.get_cvv()}")
        print(f"Card Type: {card.get_card_type()}")
        print(f"Valid: {card.is_valid()}")

        return 0 if card.is_valid() else 1

    except CCParserError as e:
        if args.quiet:
            return 1
        if args.json_output:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        if args.quiet:
            return 1
        if args.json_output:
            print(json.dumps({"error": f"Unexpected error: {e}"}), indent=2)
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
