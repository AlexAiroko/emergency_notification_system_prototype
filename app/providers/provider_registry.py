from app.models.contact_method import ChannelType
from app.providers.base import BaseProvider
from app.providers.email import EmailProvider
from app.providers.telegram import TelegramProvider
from app.core.config import settings


class ProviderRegistry:
    def __init__(self):
        # A list of available providers.
        # To add a new channel (e.g., WhatsApp),
        # add an object for this channel to this dictionary.
        self.providers = {
            "email": EmailProvider(),
            "telegram": TelegramProvider(settings.TELEGRAM_BOT_TOKEN),
        }

    def get(self, channel: ChannelType) -> BaseProvider:
        """
        Returns a provider by channel name.
        """
        provider = self.providers.get(channel.value)

        if provider is None:
            raise ValueError(f"Unsupported channel: {channel}")

        return provider
