import os
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)

import tensorflow as tf

# Load the saved model
model = tf.keras.models.load_model("my_image_classifier.h5")

# Save in TensorFlow's 'SavedModel' format
model.save("my_image_classifier.h5", save_format="tf")


# Define labels
label_names = {0: "Chihuahua", 1: "Muffin"}

# Create a directory for uploaded images
UPLOAD_FOLDER = "static/uploaded_images"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No file selected", 400
    
    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        
        # Preprocess the image
        img = image.load_img(filepath, target_size=(64, 64))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict
        prediction = model.predict(img_array)
        predicted_class = int(np.round(prediction[0][0]))
        label = label_names[predicted_class]
        
        return render_template("result.html", label=label, image_url=filepath)

if __name__ == "__main__":
    app.run(debug=True)
