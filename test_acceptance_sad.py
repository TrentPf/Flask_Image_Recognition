"""Acceptance tests for invalid upload requests."""


def test_acceptance_missing_file(client):
    """A missing upload should display an error message."""
    response = client.post(
        "/prediction",
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." in response.data
