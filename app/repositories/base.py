from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def flush(self) -> None:
        self.session.flush()
