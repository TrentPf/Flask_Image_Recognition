"""Acceptance tests for successful image uploads."""

from io import BytesIO

from PIL import Image


def make_image(size=(50, 50)):
    """Create a valid PNG image for upload."""
    image = Image.new("RGB", size, color=(255, 0, 0))
    image_stream = BytesIO()
    image.save(image_stream, format="PNG")
    image_stream.seek(0)
    return image_stream


def test_acceptance_successful_upload(client):
    """Check that a valid image upload produces a result."""
    response = client.post(
        "/prediction",
        data={"file": (make_image(), "test.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data


def test_acceptance_valid_large_image(client):
    """Check that a larger valid image can be processed."""
    response = client.post(
        "/prediction",
        data={"file": (make_image((1000, 1000)), "large.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data


def test_acceptance_valid_image_size_upload(client):
    """Check that a different image resolution is accepted."""
    response = client.post(
        "/prediction",
        data={"file": (make_image((640, 480)), "sized.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
