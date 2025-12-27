# import the necessary packages
import numpy as np
import cv2
import yaml

with open('./config.yml', 'r') as file:
    config = yaml.safe_load(file) 

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()
print(config)
# open webcam video stream
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('Vid3_overhead.mov')
# cap = cv2.VideoCapture('Vid1_UP.mov')
cap = cv2.VideoCapture(config['cap_source'])
# cap = cv2.VideoCapture('Vid2_higher.mov')

# the output will be written to output.avi
out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640,480))
count = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    frame = cv2.resize(frame, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    # boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
    boxes, weights = hog.detectMultiScale(frame, winStride=(config['padding'],config['padding']), padding=(config['padding'], config['padding']), scale=config['scale'])

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
    
    # Write the output video 
    out.write(frame.astype('uint8'))
    # Display the resulting frame
    cv2.imshow('frame',frame)

    # advance 30 frames
    count += config['frames_skip'] # i.e. at 30 fps, this advances one second
    cap.set(cv2.CAP_PROP_POS_FRAMES, count)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)

