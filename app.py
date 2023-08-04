from flask import Flask, jsonify, request,render_template
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import base64
from keras.models import load_model

app = Flask(__name__)

# Load the model
model = load_model("Model/keras_model.h5")

# Create a VideoCapture object to read from the webcam
cap = cv2.VideoCapture(0)

# Route for serving the index.html file
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    # Read a video frame from the webcam
    success, frame = cap.read()

    # Process the video frame, perform hand detection, and make predictions
    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

    offset = 20
    imgSize = 300
    labels = ["A", "B", "C"]

    hands, _ = detector.findHands(frame)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = frame[y - offset:y + h + offset, x - offset:x + w + offset]
        imgCropShape = imgCrop.shape
        if imgCrop.shape[0] == 0 or imgCrop.shape[1] == 0:
            # Skip the resize operation if the image size is empty
            predicted_gesture = 'None'
        else:

            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)

        # Get the predicted gesture
        predicted_gesture = labels[index]
    else:
        # If no hand is detected, set the predicted gesture as 'None'
        predicted_gesture = 'None'

    # Return the predicted gesture to the frontend
    result = {"prediction": predicted_gesture}
    return jsonify(result)

    

if __name__ == '__main__':
    app.run()