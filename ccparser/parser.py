import re
from .validator import validate_card_number, validate_expiry_date, validate_cvv
from .formatter import format_card_number, mask_card_number
from .utils import detect_card_type
from .utils import get_card_details

class CCParser:
    def __init__(self, card_string):
        self.card_string = card_string
        self.card_number, self.expiry_month, self.expiry_year, self.cvv = self.parse_card_string(card_string)
    
    def parse_card_string(self, card_string):
        delimiters = r"[|: ]"
        parts = re.split(delimiters, card_string)
        if len(parts) == 3:
            card_number, expiry, cvv = parts
            if '/' in expiry:
                expiry_month, expiry_year = expiry.split('/')
            else:
                raise ValueError("Invalid expiry date format")
        elif len(parts) == 4:
            card_number, expiry_month, expiry_year, cvv = parts
        else:
            raise ValueError("Invalid card string format")
        
        if len(expiry_year) == 2:
            expiry_year = "20" + expiry_year
        
        return card_number, expiry_month, expiry_year, cvv
    
    def get_number(self):
        return self.card_number
    
    def get_formatted_number(self):
        return format_card_number(self.card_number)
    
    def get_expiry(self):
        return f"{self.expiry_month}/{self.expiry_year[2:]}"
    
    def get_year(self):
        return self.expiry_year

    def get_month(self):
        return self.expiry_month
    
    def get_cvv(self):
        return self.cvv
    
    def is_valid(self):
        return (validate_card_number(self.card_number) and
                validate_expiry_date(self.expiry_month, self.expiry_year) and
                validate_cvv(self.cvv, self.card_number))
    
    def get_card_type(self):
        return detect_card_type(self.card_number)
    
    def get_masked_number(self):
        return mask_card_number(self.card_number)
    
    def get_card_details(self):
        return get_card_details(self.card_number)