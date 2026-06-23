from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import session_maker
from app.db.uow import UnitOfWork


def get_session() -> Generator[Session, None, None]:
    session = session_maker()
    try:
        yield session
    finally:
        session.close()


def get_uow() -> Generator[UnitOfWork, None, None]:
    with UnitOfWork() as uow:
        yield uow
