import phonenumbers

from app.exceptions.validation import PhoneValidationError


def validate_phone(phone_number: str) -> str:
    parsed = phonenumbers.parse(phone_number, None)

    if not phonenumbers.is_valid_number(parsed):
        raise PhoneValidationError(phone_number)

    return phonenumbers.format_number(
        parsed,
        phonenumbers.PhoneNumberFormat.E164,
    )

