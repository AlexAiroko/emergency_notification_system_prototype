import pytest

from tests.fakes.fake_uow import FakeUnitOfWork


@pytest.fixture
def uow():
    return FakeUnitOfWork()
