 # Import necessary libraries
import cv2

# Load pre-trained HOG descriptor
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Open video stream
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('Vid3_overhead.mov')
cap = cv2.VideoCapture('Vid1_UP.mov')
# cap = cv2.VideoCapture('Vid2_higher.mov')

# Initialize tracker (optional)
tracker = None

while True:
    # Read frame from video stream
    ret, frame = cap.read()

    # resize frame
    frame = cv2.resize(frame, (640, 480))

    # Detect people in the frame
    (rects, weights) = hog.detectMultiScale(frame, winStride=(12, 8),
                                            padding=(8, 4), scale=1.05)

    # Draw bounding boxes around detected people
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Initialize tracker if not already initialized
        if tracker is None:
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, (x, y, w, h))

    # Update tracker if initialized
    if tracker is not None:
        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Display the output
    cv2.imshow('People Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

