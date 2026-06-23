from unittest.mock import Mock


class FakeUnitOfWork:
    def __init__(self):
        self.template_repo = Mock()
        self.notification_repo = Mock()
        self.delivery_repo = Mock()
        self.group_repo = Mock()
        self.contact_repo = Mock()

        self.commit = Mock()
        self.rollback = Mock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
