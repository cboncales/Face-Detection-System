from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Allow requests from React

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Process the image
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.06, minNeighbors=7, minSize=(20, 20))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  

    processed_path = os.path.join(PROCESSED_FOLDER, file.filename)
    cv2.imwrite(processed_path, img)

    return jsonify({"message": "Face detection complete", "filename": file.filename})

@app.route("/processed/<filename>", methods=["GET"])
def get_processed_image(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(debug=True)
