"""Image preprocessing and prediction for hand-digit recognition."""
# Importing required libs
from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
from PIL import Image

# Loading model
model = load_model("digit_model.h5")


# Preparing and pre-processing the image
def preprocess_img(img_path):
    """Convert an uploaded image into the model's expected input shape."""
    with Image.open(img_path) as image:
        resized_image = image.convert("RGB").resize((224, 224))
        image_array = img_to_array(resized_image) / 255.0

    return image_array.reshape(1, 224, 224, 3)


# Predicting function
def predict_result(predict):
    """Return the digit with the highest prediction score."""
    pred = model.predict(predict)
    return np.argmax(pred[0], axis=-1)
