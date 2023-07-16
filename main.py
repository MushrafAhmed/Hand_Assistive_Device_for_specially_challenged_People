import cv2
from flask import Flask, jsonify, request, render_template
import base64
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from flask import request
import glob

app = Flask(__name__)
camera = cv2.VideoCapture(0, cv2.CAP_V4L2)

def predict_text(image):
    # Preprocess the image
    # preprocessed_image = preprocess_image(image)

    # Pass the preprocessed image through the model
    # predictions = model.predict(preprocessed_image)

    # Get the predicted text
    predicted_text = "Sample Text"  # Replace with your actual code to extract the text from predictions

    return predicted_text


# Route to capture and process photos
@app.route('/capture', methods=['POST'])
def capture():
    # Retrieve the captured image data from the request
    image_file = request.files.get('image-file')

    # Check if image_file is None or empty
    if image_file is None or image_file.filename == '':
        return jsonify({'error': 'No image file received'})

    # Delete older images if the maximum limit is reached
    image_files = glob.glob(os.path.join(SAVE_IMAGE_FOLDER, '*.png'))
    if len(image_files) >= MAX_SAVED_IMAGES:
        oldest_image = min(image_files, key=os.path.getctime)
        os.remove(oldest_image)

    # Save the image file to a desired location
    save_path = os.path.join(SAVE_IMAGE_FOLDER, image_file.filename)
    image_file.save(save_path)

    # Perform predictions on the saved image
    predicted_text = perform_predictions_on_image(save_path)

    # Optionally, you can return the predicted text as a response
    return jsonify({'predicted_text': predicted_text})


# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

SAVE_IMAGE_FOLDER = 'C:/Users/Lenovo/flask/images'
MAX_SAVED_IMAGES = 5

# Function to perform predictions on the saved image
def perform_predictions_on_image(image_path):
    # Load the saved image
    saved_image = cv2.imread(image_path)

    # Perform any necessary preprocessing on the image

    # Pass the preprocessed image through the model for predictions
    predicted_text = predict_text(saved_image)

    return predicted_text


SMTP_SERVER = 'smtp-relay.sendinblue.com'
SMTP_PORT = 587
SMTP_USERNAME = 'datlarakesh3@gmail.com'
SMTP_PASSWORD = 'Rakesh@2000'

@app.route('/emergency', methods=['POST'])
def handle_emergency():
    # Get the emergency contact details from the request JSON
    data = request.get_json()
    emergency_contact = data.get('emergency_contact')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Compose the email message
    subject = "Emergency Alert!"
    message = f"Emergency! I need help!\n\nLocation: Latitude {latitude}, Longitude {longitude}"
    sender_email = 'datlarakesh3@gmail.com'
    receiver_email = emergency_contact

    # Create a multipart message and set the headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Set up the SMTP connection
    with smtplib.SMTP('smtp-relay.sendinblue.com', 587) as server:
        server.starttls()
        server.login('datlarakesh3@gmail.com', 'Rakesh@2000')
        server.send_message(msg)

    return 'Email sent successfully'

if __name__ == '__main__':
    app.run(debug=True)
