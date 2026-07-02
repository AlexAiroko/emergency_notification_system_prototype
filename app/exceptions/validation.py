from app.exceptions.base import ValidationError


class EmailValidationError(ValidationError):
    code = "email_validation"
    
    def __init__(self, email: str):
        super().__init__(f"Incorrect email: '{email}'")


class TelegramValidationError(ValidationError):
    code = "telegram_validation"
    
    def __init__(self, telegram_id: str):
        super().__init__(f"Incorrect telegram id: '{telegram_id}'")


class PhoneValidationError(ValidationError):
    code = "phone_validation"
    
    def __init__(self, phone_number: str):
        super().__init__(f"Incorrect phone number: '{phone_number}'")
