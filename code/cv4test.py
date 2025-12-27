import cv2
import numpy as np

# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('Vid3_overhead.mov')
cap = cv2.VideoCapture('Vid1_UP.mov')
# cap = cv2.VideoCapture('Vid2_higher.mov')

fgbg_mog = cv2.bgsegm.createBackgroundSubtractorMOG()

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    fgmask = fgbg_mog.apply(frame)
    cv2.imshow('fgmask',fgmask)
    cv2.imshow('frame',frame)
    frame_count += 1
    if frame_count >= 300:
        break

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

