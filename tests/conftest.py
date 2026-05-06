from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings
from app.db.base import Base


engine = create_engine(settings.TEST_DATABASE_URL)
session_maker = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


pytest_plugins = [
    "tests.fixtures.contact",
    "tests.fixtures.contact_method",
    "tests.fixtures.group",
    "tests.fixtures.delivery",
    "tests.fixtures.notification_template",
    "tests.fixtures.notification",
]


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    
    session = session_maker(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
