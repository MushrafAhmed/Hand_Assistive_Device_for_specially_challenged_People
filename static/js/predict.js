// index.js (or any suitable name)
// Add your JavaScript code here

// Function to start the video capture
function startVideoCapture() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                // Set the video stream as the source for the video element
                const video = document.getElementById('video-stream');
                video.srcObject = stream;

                // Start capturing frames and sending to the server for prediction
                captureFrameAndPredict(stream);
            })
            .catch(function (error) {
                console.error('Error accessing webcam:', error);
            });
    } else {
        console.error('getUserMedia not supported');
    }
}

// Function to capture frames and send to the server for prediction
function captureFrameAndPredict(stream) {
    const video = document.getElementById('video-stream');

    // Function to capture a frame from the video stream and send it to the server
    function captureFrameAndSend() {
        // Create a new canvas element to draw the video frame
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');

        // Set the canvas dimensions to match the video frame
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Draw the current video frame onto the canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert the canvas image to a data URL
        const imageDataUrl = canvas.toDataURL('image/png');

        // Send the captured frame to the server for prediction
        predictFromImage(imageDataUrl);
    }

    // Start capturing frames and sending to the server at a desired interval (e.g., 1 second)
    setInterval(captureFrameAndSend, 1000);
}

// Function to send the captured frame to the server for prediction
function predictFromImage(imageDataUrl) {
    // Create a new FormData object
    const formData = new FormData();

    // Append the image data to the FormData object
    formData.append('image-data', imageDataUrl);

    // Send the POST request to the server
    fetch('/predict', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())  // Read response as JSON
        .then(data => {
            // Handle the response from the server
            if (data.prediction) {
                // Display the predicted text on the web page
                const predictedText = data.prediction;
                document.getElementById('predicted_text').textContent = predictedText;
            }
        })
        .catch(error => {
            // Handle any errors that occurred during the request
            console.error('Error:', error);
        });
}

// Start the video capture when the page loads
window.onload = function () {
    startVideoCapture();
};
