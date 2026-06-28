from abc import ABC, abstractmethod


class ProviderError(Exception):
    """Error sending through an external provider."""
    pass


class BaseProvider(ABC):
    @abstractmethod
    def send(
        self,
        to: str,
        body: str,
        subject: str | None = None,
    ) -> str | None:
        """
        Sends a message.

        Args:
            to: Recipient's address (email, phone, chat_id, etc.)
            body: Message text.
            subject: Email subject (used, for example, for email).

        Returns:
            The ID of the message from the external provider,
            if it is available.

        Raises:
            ProviderError: if the sending failed.
        """
        raise NotImplementedError
