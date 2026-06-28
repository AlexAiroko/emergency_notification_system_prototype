import smtplib
import logging

from email.message import EmailMessage
from email.utils import make_msgid

from app.core.config import settings
from app.providers.base import BaseProvider, ProviderError


logger = logging.getLogger(__name__)


class EmailProvider(BaseProvider):
    def send(
        self,
        to: str,
        body: str,
        subject: str | None = None,
    ) -> str | None:
        logger.info(
            "Started sending email (host=%s, port=%s, to=%s)",
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            to,
        )

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
                    logger.info("Starting TLS for email delivery")
                    smtp.starttls()

                logger.info("Authenticating SMTP user=%s", settings.SMTP_USERNAME)
                smtp.login(
                    settings.SMTP_USERNAME,
                    settings.SMTP_PASSWORD,
                )

                smtp.send_message(message)

            logger.info(
                "Email sent successfully (to=%s, message_id=%s)",
                to,
                message["Message-ID"],
            )
            
            # SMTP usually does not return a message_id, 
            # so we use the Message-ID header.

            return message["Message-ID"]

        except Exception as exc:
            logger.exception(
                "Failed to send email (to=%s)",
                to,
            )
            raise ProviderError(str(exc)) from exc
