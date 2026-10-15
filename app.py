"""Flask routes for the hand-digit recognition application."""
# Importing required libs
from flask import Flask, render_template, request
from PIL import UnidentifiedImageError
from model import preprocess_img, predict_result

# Instantiating flask app
app = Flask(__name__)


# Home route
@app.route("/")
def main():
    """Display the image upload page."""
    return render_template("index.html")


# Prediction route
@app.route('/prediction', methods=['POST'])
def predict_image_file():
    """Process an uploaded image and display the predicted digit."""
    uploaded_file = request.files.get("file")

    if uploaded_file is None or not uploaded_file.filename:
        return render_template(
            "result.html",
            err="File cannot be processed."
        )

    try:
        processed_image = preprocess_img(uploaded_file.stream)
        prediction = predict_result(processed_image)
    except (OSError, ValueError, UnidentifiedImageError):
        return render_template(
            "result.html",
            err="File cannot be processed."
        )

    return render_template(
        "result.html",
        predictions=str(prediction)
    )


# Driver code
if __name__ == "__main__":
    app.run(port=9000, debug=True)
