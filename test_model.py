"""Tests for image preprocessing and model predictions."""

from io import BytesIO

import numpy as np
import pytest
from PIL import Image

from model import preprocess_img, predict_result


def make_test_image():
    """Create a valid image in memory for testing."""
    image_stream = BytesIO()
    image = Image.new("RGB", (50, 50), color=(255, 0, 0))
    image.save(image_stream, format="PNG")
    image_stream.seek(0)
    return image_stream


def test_preprocess_img():
    """Check the output dimensions and normalized pixel values."""
    processed_img = preprocess_img(make_test_image())

    assert processed_img.shape == (1, 224, 224, 3)
    assert np.min(processed_img) >= 0
    assert np.max(processed_img) <= 1


def test_predict_result():
    """Check that a prediction returns an integer class index."""
    processed_img = preprocess_img(make_test_image())
    prediction = predict_result(processed_img)

    assert isinstance(prediction, (int, np.integer))


def test_invalid_image_path():
    """Check that a nonexistent image path raises an error."""
    with pytest.raises(FileNotFoundError):
        preprocess_img("invalid/path/to/image.jpeg")


def test_image_shape_on_prediction():
    """Check the prediction result type after preprocessing."""
    processed_img = preprocess_img(make_test_image())
    prediction = predict_result(processed_img)

    assert isinstance(prediction, (int, np.integer))


def test_model_predictions_consistency():
    """Check that repeated predictions return the same class."""
    processed_img = preprocess_img(make_test_image())

    predictions = [
        predict_result(processed_img)
        for _ in range(5)
    ]

    assert all(
        prediction == predictions[0]
        for prediction in predictions
    )
