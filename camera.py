import cv2

def capture_image(file_path):
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    # Capture frame-by-frame
    ret, frame = cap.read()

    # If the frame was captured successfully, save it to a file
    if ret:
        cv2.imwrite(file_path, frame)
        print(f"Image captured and saved as {file_path}")
    else:
        print("Error: Failed to capture image")

    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
