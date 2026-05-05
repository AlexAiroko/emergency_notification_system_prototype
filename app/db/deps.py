from typing import Generator

from sqlalchemy.orm import Session

from app.db.session import session_maker


def get_session() -> Generator[Session, None, None]:
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
