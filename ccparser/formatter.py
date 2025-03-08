def format_card_number(card_number):
    return " ".join(card_number[i:i+4] for i in range(0, len(card_number), 4))

def mask_card_number(card_number):
    return "**** **** **** " + card_number[-4:]