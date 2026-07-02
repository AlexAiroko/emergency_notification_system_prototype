from app.exceptions.validation import TelegramValidationError


def validate_telegram_id(telegram_id: str) -> str:
    telegram_id = telegram_id.strip()

    if telegram_id.isdigit():
        return telegram_id

    raise TelegramValidationError(telegram_id)
