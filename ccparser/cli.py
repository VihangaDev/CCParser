import argparse
from .parser import CCParser, InvalidCardNumberError, InvalidExpiryDateError, InvalidCVVError

def main():
    parser = argparse.ArgumentParser(description="CCParser CLI tool")
    parser.add_argument("card_string", help="Credit card string to parse")
    args = parser.parse_args()
    
    try:
        card = CCParser(args.card_string)
        print(f"Card Number: {card.get_formatted_number()}")
        print(f"Expiry Date: {card.get_expiry()}")
        print(f"CVV: {card.get_cvv()}")
        print(f"Card Type: {card.get_card_type()}")
        print(f"Valid: {card.is_valid()}")
    except (InvalidCardNumberError, InvalidExpiryDateError, InvalidCVVError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()