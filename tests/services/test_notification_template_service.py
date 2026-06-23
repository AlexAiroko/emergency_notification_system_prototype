from types import SimpleNamespace

import pytest
from sqlalchemy.exc import IntegrityError

from app.exceptions.notification_template import (
    TemplateAlreadyExistsError,
    TemplateBodyEmptyError,
    TemplateInactiveError,
    TemplateNotFoundError,
)


def test_create_template(template_service, uow):
    template = SimpleNamespace(id=1)

    uow.template_repo.create.return_value = template

    result = template_service.create_template(
        uow,
        body="body",
        name="name",
        subject="subject",
    )

    assert result is template

    uow.template_repo.create.assert_called_once_with(
        body="body",
        name="name",
        subject="subject",
        is_active=True,
    )


@pytest.mark.parametrize(
    "body",
    [
        "",
        " ",
        "     ",
        "\n",
    ],
)
def test_create_template_empty_body(template_service, uow, body):
    with pytest.raises(
        TemplateBodyEmptyError,
        match="Template body cannot be empty",
    ):
        template_service.create_template(
            uow,
            body=body,
            name="name",
        )

    uow.template_repo.create.assert_not_called()


def test_create_template_already_exists(template_service, uow):
    uow.template_repo.create.side_effect = IntegrityError(
        statement="",
        params={},
        orig=Exception(),
    )

    with pytest.raises(
        TemplateAlreadyExistsError,
        match="Template already exists",
    ):
        template_service.create_template(
            uow,
            body="body",
            name="name",
        )


def test_get_template(template_service, uow):
    template_service.get_template(uow, 10)

    uow.template_repo.get.assert_called_once_with(10)


def test_get_template_not_found(template_service, uow):
    uow.template_repo.get.return_value = None

    with pytest.raises(
        TemplateNotFoundError,
        match="Template 10 not found",
    ):
        template_service.get_template(uow, 10)


def test_get_many_templates(template_service, uow):
    template_service.get_many_templates(
        uow,
        limit=20,
        offset=5,
    )

    uow.template_repo.get_many.assert_called_once_with(
        limit=20,
        offset=5,
    )


def test_get_active_templates(template_service, uow):
    template_service.get_active_templates(
        uow,
        limit=30,
        offset=10,
    )

    uow.template_repo.get_active.assert_called_once_with(
        limit=30,
        offset=10,
    )


def test_update_template(template_service, uow):
    template_service.update_template(
        uow,
        template_id=1,
        subject="subj",
        body="body",
    )

    uow.template_repo.update_content.assert_called_once_with(
        template_id=1,
        subject="subj",
        body="body",
    )


def test_update_template_none_subject(template_service, uow):
    template_service.update_template(
        uow,
        template_id=1,
        subject=None,
        body="body",
    )

    uow.template_repo.update_content.assert_called_once_with(
        template_id=1,
        subject="",
        body="body",
    )


def test_update_template_empty_body(template_service, uow):
    with pytest.raises(
        TemplateBodyEmptyError,
        match="Template body cannot be empty",
    ):
        template_service.update_template(
            uow,
            template_id=1,
            subject="subj",
            body=" ",
        )

    uow.template_repo.update_content.assert_not_called()


def test_activate_template(template_service, uow):
    template_service.activate_template(uow, 5)

    uow.template_repo.activate.assert_called_once_with(5)


def test_deactivate_template(template_service, uow):
    template_service.deactivate_template(uow, 5)

    uow.template_repo.deactivate.assert_called_once_with(5)


def test_ensure_template_is_active(template_service, uow):
    template = SimpleNamespace(
        is_active=True,
    )

    uow.template_repo.get.return_value = template

    result = template_service.ensure_template_is_active(
        uow,
        10,
    )

    assert result is template


def test_ensure_template_not_found(template_service, uow):
    uow.template_repo.get.return_value = None

    with pytest.raises(
        TemplateNotFoundError,
        match="Template 10 not found",
    ):
        template_service.ensure_template_is_active(
            uow,
            10,
        )


def test_ensure_template_inactive(template_service, uow):
    uow.template_repo.get.return_value = SimpleNamespace(
        is_active=False,
    )

    with pytest.raises(
        TemplateInactiveError,
        match="Template 10 is inactive",
    ):
        template_service.ensure_template_is_active(
            uow,
            10,
        )
