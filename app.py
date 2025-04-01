import cv2
import numpy as np
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Load Haar Cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
upperbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_upperbody.xml")


def detect_faces(img):
    """Detect faces and draw rectangles around them."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return img


def detect_eyes(img):
    """Detect face first, then find eyes within the face region for better accuracy."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces first
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10)
    
    if len(faces) == 0:
        return img  # If no face is detected, return the original image without processing

    for (fx, fy, fw, fh) in faces:
        # Draw face rectangle (optional)
        # cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)
        
        # Region of Interest (ROI) for eyes within the face
        face_roi = gray[fy:fy + fh, fx:fx + fw]
        color_roi = img[fy:fy + fh, fx:fx + fw]  # For drawing rectangles on the original image

        # Detect eyes inside the face ROI
        eyes = eye_cascade.detectMultiScale(face_roi, scaleFactor=1.02, minNeighbors=3)
        
        for (ex, ey, ew, eh) in eyes:
            # Draw eye rectangles relative to the face region
            cv2.rectangle(color_roi, (ex, ey), (ex + ew, ey + eh), (255, 255, 255), 2)

    return img




def detect_mouth(img):
    """Detect mouth and draw rectangles around it."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces first
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10)

    if len(faces) == 0:
        return img  # If no face is detected, return the original image without processing
    
    for (fx, fy, fw, fh) in faces:
        # Draw face rectangle (optional)
        # cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)
        
        # Region of Interest (ROI) for eyes within the face
        mouth_roi = gray[fy:fy + fh, fx:fx + fw]
        color_roi = img[fy:fy + fh, fx:fx + fw]  # For drawing rectangles on the original image

        # Detect eyes inside the face ROI
        mouth = mouth_cascade.detectMultiScale(mouth_roi, scaleFactor=1.1, minNeighbors=15)
        
        for (ex, ey, ew, eh) in mouth:
            # Draw eye rectangles relative to the face region
            cv2.rectangle(color_roi, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

    return img


def detect_fullbody(img):
    """Detect full body and draw rectangles around it."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bodies = fullbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

    for (x, y, w, h) in bodies:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return img


def detect_upperbody(img):
    """Detect upper body and draw rectangles around it."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    upper_body = upperbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

    for (x, y, w, h) in upper_body:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 165, 0), 2)

    return img


@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files or "detection_type" not in request.form:
        return jsonify({"error": "No file or detection type provided"}), 400

    file = request.files["file"]
    detection_type = request.form["detection_type"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    img = cv2.imread(filepath)

    # Map detection type to function
    detection_functions = {
        "face": detect_faces,
        "eyes": detect_eyes,
        "mouth": detect_mouth,
        "fullbody": detect_fullbody,
        "upperbody": detect_upperbody,
    }

    if detection_type not in detection_functions:
        return jsonify({"error": "Invalid detection type"}), 400

    processed_img = detection_functions[detection_type](img)

    processed_path = os.path.join(PROCESSED_FOLDER, file.filename)
    cv2.imwrite(processed_path, processed_img)

    return jsonify({"message": f"{detection_type} detection complete", "filename": file.filename})


@app.route("/processed/<filename>", methods=["GET"])
def get_processed_image(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(debug=True)



@app.route("/processed/<filename>", methods=["GET"])
def get_processed_image(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(debug=True)
