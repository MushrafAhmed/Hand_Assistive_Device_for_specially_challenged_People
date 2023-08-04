import cv2
from main import predict_text

# Define a function to call predict_text repeatedly
def run_prediction_speed_test():
    image_path = r'C:/Users/Lenovo/flask/images/captured_frame.png'
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load the image.")
        return

    for _ in range(100):  # Repeat the prediction 100 times for profiling accuracy
        # Pass the image to predict_text function
        predicted_text = predict_text(image)

# Call the function and apply the @profile decorator for profiling
if __name__ == '__main__':
    run_prediction_speed_test()