from email.message import EmailMessage
from email.utils import make_msgid
import smtplib

from app.core.config import settings
from app.providers.base import BaseProvider, ProviderError

class EmailProvider(BaseProvider):
    def send(
        self,
        to: str,
        body: str,
        subject: str | None = None,
    ) -> str | None:
        message = EmailMessage()
        message["From"] = settings.SMTP_FROM
        message["To"] = to
        message["Subject"] = subject or ""
        message["Message-ID"] = make_msgid()
        message.set_content(body)
        
        try:
            with smtplib.SMTP(
                settings.SMTP_HOST,
                settings.SMTP_PORT,
                timeout=30,
            ) as smtp:
                if settings.SMTP_USE_TLS:
                    smtp.starttls()

                smtp.login(
                    settings.SMTP_USERNAME,
                    settings.SMTP_PASSWORD,
                )

                smtp.send_message(message)

            # SMTP usually does not return a message_id, 
            # so we use the Message-ID header.
            return message["Message-ID"]

        except Exception as exc:
            raise ProviderError(str(exc)) from exc
