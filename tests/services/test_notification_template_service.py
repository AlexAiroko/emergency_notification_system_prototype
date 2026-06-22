from types import SimpleNamespace

import pytest


def test_create_template(template_service):
    template = SimpleNamespace(id=1)

    template_service.template_repo.create.return_value = template

    result = template_service.create_template(
        body="body",
        name="name",
        subject="subject",
    )

    assert result is template

    template_service.template_repo.create.assert_called_once_with(
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
    ]
)
def test_create_template_empty_body(template_service, body):
    with pytest.raises(
        ValueError,
        match="Template body cannot be empty",
    ):
        template_service.create_template(
            body=body,
            name="name",
        )

    template_service.template_repo.create.assert_not_called()


def test_get_template(template_service):
    template_service.get_template(10)

    template_service.template_repo.get.assert_called_once_with(10)


def test_get_many_templates(template_service):
    template_service.get_many_templates(
        limit=20,
        offset=5,
    )

    template_service.template_repo.get_many.assert_called_once_with(
        limit=20,
        offset=5,
    )


def test_get_active_templates(template_service):
    template_service.get_active_templates(
        limit=30,
        offset=10,
    )

    template_service.template_repo.get_active.assert_called_once_with(
        limit=30,
        offset=10,
    )


def test_update_template(template_service):
    template_service.update_template(
        template_id=1,
        subject="subj",
        body="body",
    )

    template_service.template_repo.update_content.assert_called_once_with(
        template_id=1,
        subject="subj",
        body="body",
    )


def test_update_template_none_subject(template_service):
    template_service.update_template(
        template_id=1,
        subject=None,
        body="body",
    )

    template_service.template_repo.update_content.assert_called_once_with(
        template_id=1,
        subject="",
        body="body",
    )


def test_update_template_empty_body(template_service):
    with pytest.raises(
        ValueError,
        match="Template body cannot be empty",
    ):
        template_service.update_template(
            template_id=1,
            subject="subj",
            body=" ",
        )

    template_service.template_repo.update_content.assert_not_called()


def test_activate_template(template_service):
    template_service.activate_template(5)

    template_service.template_repo.activate.assert_called_once_with(5)


def test_deactivate_template(template_service):
    template_service.deactivate_template(5)

    template_service.template_repo.deactivate.assert_called_once_with(5)


from types import SimpleNamespace


def test_ensure_template_is_active(template_service):
    template = SimpleNamespace(
        is_active=True,
    )

    template_service.template_repo.get.return_value = template

    result = template_service.ensure_template_is_active(10)

    assert result is template


import pytest


def test_ensure_template_not_found(template_service):
    template_service.template_repo.get.return_value = None

    with pytest.raises(
        ValueError,
        match="Template 10 not found",
    ):
        template_service.ensure_template_is_active(10)


def test_ensure_template_inactive(template_service):
    template_service.template_repo.get.return_value = SimpleNamespace(
        is_active=False,
    )

    with pytest.raises(
        ValueError,
        match="Template 10 is inactive",
    ):
        template_service.ensure_template_is_active(10)
