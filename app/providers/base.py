from abc import ABC, abstractmethod


class ProviderError(Exception):
    """Ошибка отправки через внешний провайдер."""
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
        Отправляет сообщение.

        Args:
            to: Адрес получателя (email, телефон, chat_id и т.д.)
            body: Текст сообщения.
            subject: Тема письма (используется, например, для email).

        Returns:
            Идентификатор сообщения у внешнего провайдера,
            если он доступен.

        Raises:
            ProviderError: если отправка завершилась ошибкой.
        """
        raise NotImplementedError
