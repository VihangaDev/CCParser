import re
from .validator import validate_card_number, validate_expiry_date, validate_cvv
from .formatter import format_card_number, mask_card_number
from .utils import detect_card_type, get_card_details

class InvalidCardNumberError(Exception):
    pass

class InvalidExpiryDateError(Exception):
    pass

class InvalidCVVError(Exception):
    pass

class CCParser:
    def __init__(self, card_string: str):
        self.card_string = card_string
        self.card_number, self.expiry_month, self.expiry_year, self.cvv = self.parse_card_string(card_string)
    
    def parse_card_string(self, card_string: str) -> tuple[str, str, str, str]:
        delimiters = r"[|: ]"
        parts = re.split(delimiters, card_string)
        if len(parts) == 3:
            card_number, expiry, cvv = parts
            if '/' in expiry:
                expiry_month, expiry_year = expiry.split('/')
            elif '-' in expiry:
                expiry_month, expiry_year = expiry.split('-')
            else:
                raise InvalidExpiryDateError("Invalid expiry date format")
        elif len(parts) == 4:
            card_number, expiry_month, expiry_year, cvv = parts
        else:
            raise InvalidCardNumberError("Invalid card string format")
        
        if len(expiry_year) == 2:
            expiry_year = "20" + expiry_year
        
        return card_number, expiry_month, expiry_year, cvv
    
    def get_number(self) -> str:
        return self.card_number
    
    def get_formatted_number(self) -> str:
        return format_card_number(self.card_number)
    
    def get_expiry(self) -> str:
        return f"{self.expiry_month}/{self.expiry_year[2:]}"
    
    def get_year(self) -> str:
        return self.expiry_year

    def get_month(self) -> str:
        return self.expiry_month
    
    def get_cvv(self) -> str:
        return self.cvv
    
    def is_valid(self) -> bool:
        if not validate_card_number(self.card_number):
            raise InvalidCardNumberError("Invalid card number")
        if not validate_expiry_date(self.expiry_month, self.expiry_year):
            raise InvalidExpiryDateError("Invalid expiry date")
        if not validate_cvv(self.cvv, self.card_number):
            raise InvalidCVVError("Invalid CVV")
        return True
    
    def get_card_type(self) -> str:
        return detect_card_type(self.card_number)
    
    def get_masked_number(self) -> str:
        return mask_card_number(self.card_number)
    
    def get_card_details(self) -> dict:
        return get_card_details(self.card_number)