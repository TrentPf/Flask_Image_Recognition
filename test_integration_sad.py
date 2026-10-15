"""Integration tests for invalid prediction requests."""


def test_missing_file(client):
    """A missing uploaded file should display an error."""
    response = client.post(
        "/prediction",
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." in response.data
