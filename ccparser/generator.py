import random

def generate_card_number(card_type: str) -> str:
    """
    Generate a valid credit card number for the specified card type.
    
    Args:
        card_type: The type of credit card to generate (Visa, MasterCard, AMEX, etc.)
        
    Returns:
        A valid credit card number that passes Luhn validation
    """
    card_prefixes = {
        "Visa": ["4"],
        "MasterCard": ["51", "52", "53", "54", "55"],
        "AMEX": ["34", "37"],
        "Discover": ["6011", "644", "645", "646", "647", "648", "649", "65"],
        "JCB": ["3528", "3529", "353", "354", "355", "356", "357", "358"],
        "Diners Club": ["300", "301", "302", "303", "304", "305", "36", "38"],
        "UnionPay": ["62"]
    }
    
    if card_type not in card_prefixes:
        raise ValueError(f"Unsupported card type: {card_type}")
    
    prefix = random.choice(card_prefixes[card_type])
    
    # Set card length based on card type
    if card_type == "AMEX":
        length = 15
    elif card_type == "Diners Club":
        length = 14
    else:
        length = 16
    
    # Generate card number without check digit
    number = prefix
    while len(number) < length - 1:
        number += str(random.randint(0, 9))
    
    # Calculate Luhn check digit
    total = 0
    reversed_digits = number[::-1]
    
    for i, digit in enumerate(reversed_digits):
        digit_value = int(digit)
        if i % 2 == 0:
            digit_value *= 2
            if digit_value > 9:
                digit_value -= 9
        total += digit_value
    
    check_digit = (10 - (total % 10)) % 10
    
    # Append check digit to get the complete card number
    card_number = number + str(check_digit)
    
    return card_number