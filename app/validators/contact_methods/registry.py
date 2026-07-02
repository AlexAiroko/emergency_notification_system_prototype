from app.models.contact_method import ChannelType
from app.validators.contact_methods.email import validate_email
from app.validators.contact_methods.telegram import validate_telegram_id
from app.validators.contact_methods.phone import validate_phone


class ContactMethodValidatorRegistry:
    _validators = {
        ChannelType.EMAIL: validate_email,
        ChannelType.TELEGRAM: validate_telegram_id,
        ChannelType.SMS: validate_phone,
    }

    @classmethod
    def validate(cls, channel: ChannelType, value: str) -> str:
        validator = cls._validators.get(channel)

        if not validator:
            raise ValueError(f"No validator for channel: {channel}")

        return validator(value)
