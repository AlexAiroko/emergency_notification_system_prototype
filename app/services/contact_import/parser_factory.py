from app.exceptions.contact_import import UnsupportedImportFileError
from app.services.contact_import.parsers import (
    BaseContactParser,
    CsvParser,
    ExcelParser,
)


class ParserFactory:
    _PARSERS: dict[str, type[BaseContactParser]] = {
        "csv": CsvParser,
        "xlsx": ExcelParser,
    }
    
    @classmethod
    def get(cls, filename: str | None) -> BaseContactParser:
        if filename is None:
            raise UnsupportedImportFileError("<unknown>")
        
        extension = filename.rsplit(".", 1)[-1].lower()
        
        parser = cls._PARSERS.get(extension)
        
        if parser is None:
            raise UnsupportedImportFileError(filename)
        
        return parser()
