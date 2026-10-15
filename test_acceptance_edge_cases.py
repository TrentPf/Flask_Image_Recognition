"""Acceptance tests for image upload edge cases."""

from io import BytesIO

from PIL import Image


def make_image(image_format="PNG", size=(50, 50)):
    """Create a valid image file in memory."""
    image_stream = BytesIO()
    image = Image.new("RGB", size, color=(255, 0, 0))
    image.save(image_stream, format=image_format)
    image_stream.seek(0)
    return image_stream


def test_edge_case_large_image_upload(client):
    """Check that a large valid image can be uploaded."""
    response = client.post(
        "/prediction",
        data={"file": (make_image(size=(1500, 1500)), "large.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data


def test_edge_case_invalid_metadata(client):
    """Check that invalid image contents produce an error."""
    response = client.post(
        "/prediction",
        data={"file": (BytesIO(b"invalid data"), "invalid.jpg")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." in response.data


def test_edge_case_non_standard_image_extensions(client):
    """Check that a valid WebP image can be processed."""
    response = client.post(
        "/prediction",
        data={"file": (make_image("WEBP"), "image.webp")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data


def test_edge_case_sequential_image_uploads(client):
    """Check that two consecutive uploads are processed."""
    first_response = client.post(
        "/prediction",
        data={"file": (make_image(), "first.png")},
        content_type="multipart/form-data",
    )

    second_response = client.post(
        "/prediction",
        data={"file": (make_image(), "second.png")},
        content_type="multipart/form-data",
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert b"File cannot be processed." not in first_response.data
    assert b"File cannot be processed." not in second_response.data


def test_edge_case_unexpected_headers(client):
    """Check that an additional HTTP header does not block uploads."""
    response = client.post(
        "/prediction",
        data={"file": (make_image(), "headers.png")},
        content_type="multipart/form-data",
        headers={"X-Unexpected-Header": "value"},
    )

    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data


def test_edge_case_empty_file(client):
    """Check that an empty uploaded file is rejected."""
    response = client.post(
        "/prediction",
        data={"file": (BytesIO(b""), "empty.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." in response.data
