import logging

from fastapi import UploadFile
from pydantic import validate_email

from app.db.uow import UnitOfWork
from app.exceptions.contact_import import AbsentNameFieldError
from app.models.contact_method import ChannelType
from app.services.contact_import.parser_factory import ParserFactory
from app.services.contact_import.result import ImportResult


logger = logging.getLogger(__name__)


class ContactImportService:
    def import_contacts(
        self,
        uow: UnitOfWork,
        file: UploadFile,
    ) -> ImportResult:
        """
        Imports contacts from CSV/XLSX.

        Returns:
            number of imported contacts.
        """
        
        parser = ParserFactory.get(file.filename)
        rows = parser.parse(file)
        
        result = ImportResult(total=len(rows))

        logger.info(
            "Starting import of %s contacts from '%s'",
            result.total,
            file.filename,
        )

        for idx, row in enumerate(rows, start=1):
            try:
                imported = self._import_row(uow, row)

                if imported:
                    result.imported += 1
                else:
                    result.skipped += 1

            except Exception as exc:
                result.skipped += 1
                result.errors.append(
                    {
                        "row": idx,
                        "reason": str(exc),
                    }
                )

                logger.warning(
                    "Row %s import failed: %s",
                    idx,
                    exc,
                )

        logger.info(
            "Import finished: total=%s imported=%s skipped=%s errors=%s",
            result.total,
            result.imported,
            result.skipped,
            len(result.errors),
        )

        return result

    def _import_row(self, uow: UnitOfWork, row: dict) -> bool:
        """
        Returns:
        - True -> imported
        - False -> skipped
        """

        if not row.get("name"):
            raise AbsentNameFieldError()
        
        email = row.get("email")
        
        if email:
            email = validate_email(email)

        contact = uow.contact_repo.create(
            external_id=row.get("external_id"),
            name=row["name"],
            is_active=True,
        )

        self._create_methods(uow, contact.id, row)

        return True
    
    def _create_methods(
            self,
            uow: UnitOfWork,
            contact_id: int,
            row: dict,
    ) -> None:
        for channel, field in (
            (ChannelType.EMAIL, "email"),
            (ChannelType.TELEGRAM, "telegram"),
            (ChannelType.SMS, "phone"),
        ):
            address = row.get(field)

            if not address:
                continue

            uow.contact_method_repo.create(
                contact_id=contact_id,
                channel=channel,
                address=str(address).strip(),
            )
