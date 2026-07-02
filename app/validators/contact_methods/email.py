from pydantic import validate_email as _validate_email

from app.exceptions.validation import EmailValidationError


def validate_email(email: str) -> str:
    try:
        return _validate_email(email)[1]
    except Exception:
        raise EmailValidationError(email)
