"""Integration tests for successful image uploads."""

from io import BytesIO

from PIL import Image


def test_successful_prediction(client):
    """Check that a valid uploaded image is processed."""
    image_stream = BytesIO()
    image = Image.new("RGB", (50, 50), color=(255, 0, 0))
    image.save(image_stream, format="PNG")
    image_stream.seek(0)

    response = client.post(
        "/prediction",
        data={"file": (image_stream, "test.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"File cannot be processed." not in response.data
