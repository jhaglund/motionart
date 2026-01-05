#!/usr/bin/env python3

import sys

# cursor: url 
# Add a directory to the Python path
new_directory = '/home/josh/.local/lib/python3.10/site-packages'
sys.path.append(new_directory)

import cv2
# import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
import yaml
import time
# import mouse
import threading
from pynput.mouse import Button, Controller


# open config
with open('./config.live.yml', 'r') as file:
    config = yaml.safe_load(file) 

# setup capture source
cap = cv2.VideoCapture(config['cap_source'])
# cap = cv2.VideoCapture(config['cap_source'], cv2.CAP_DSHOW) # this is the magic!

cap.set(cv2.CAP_PROP_FRAME_WIDTH, config['camera_x'])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config['camera_y'])

print('frame deets', cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

backSub = cv2.createBackgroundSubtractorMOG2()

filename = 'output3'+ (str(config['cap_source']) + '-cv3-' + str(config['min_contour_area']) + '.avi').replace('/', '-')
print('filename', filename)
# the output will be written to output-motion.avi
out = cv2.VideoWriter(
    './' + filename,
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    ((config['crop_2_x'] - config['crop_1_x']), (config['crop_2_y'] - config['crop_1_y'])))


if not cap.isOpened():
    print("Error opening video file")

cycle_start = time.time()
cycle_count = 1
# center_x = config['camera_x'] / 2
# center_y = config['camera_y'] / 2
center_x = np.floor((config['crop_2_x'] - config['crop_1_x']) / 2)
center_y = np.floor((config['crop_2_y'] - config['crop_1_y']) / 2)
x_avg_sum = center_x
y_avg_sum = center_y
x_avg_sum_avg = center_x
y_avg_sum_avg = center_y
x_avg = center_x
y_avg = center_y
ratio_x = config['screen_x'] / config['camera_x']
ratio_y = config['screen_y'] / config['camera_y']
threads = []

print('center', center_x, center_y)

mouse = Controller()


def moveMouse(x, y):
    mouse.position = (min(x, config['screen_x']), min(y, config['screen_y']))
    print('mouse move', x, y)
    # mouse.move( min(x, config['screen_x']), min(y, config['screen_y']), absolute=True, duration=config['mouse_move_interval']-0.3 )
    

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    #crop the frame
    # frame_crop = frame
    frame_crop = frame[config['crop_1_y'] : config['crop_2_y'], config['crop_1_x'] : config['crop_2_x']]
    
    # resize the frame
    # frame = cv2.resize(frame, (640, 480))


    # Apply background subtraction
    fg_mask = backSub.apply(frame_crop)

    # Find contours
    contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print(contours)
    # frame_ct = cv2.drawContours(frame_crop, contours, -1, (0, 255, 0), 2)

    # apply global threshold to remove shadows
    retval, mask_thresh = cv2.threshold( fg_mask, 180, 255, cv2.THRESH_BINARY)

    # set the kernal
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # Apply erosion
    mask_eroded = cv2.morphologyEx(mask_thresh, cv2.MORPH_OPEN, kernel)

    min_contour_area = config['min_contour_area']  # Define your minimum area threshold
    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    frame_out = frame_crop.copy()
    x_sum = 0
    y_sum = 0
    
    # if we got large_contours, use to update the average
    if(len(large_contours) > 0 ):
        for cnt in large_contours:
            # print('contour area', cv2.contourArea(cnt))
            # get x, y, width and height
            x, y, w, h = cv2.boundingRect(cnt)
            # draw the rectangle
            # frame_out = cv2.rectangle(frame_crop, (x, y), (x+w, y+h), (0, 0, 200), 3)
            #use x, y as the mouse position
            x_sum += x + ( w * 0.5 )
            y_sum += y + ( h * 0.5 )
            # print(x, y)
        x_avg = np.floor( x_sum / len(large_contours) )
        y_avg = np.floor( y_sum / len(large_contours) )
        # print('avg:', x_avg, y_avg)
        x_avg_sum += x_avg
        y_avg_sum += y_avg
        cycle_count += 1

    # # once per interval update
    # if( (time.time() - cycle_start) > config['mouse_move_interval']):
    #     print('INTERVAL ' + str(cycle_count) + ' per ' + str(config['mouse_move_interval']) + ' seconds')
    #     # print('x_avg_sum, y_avg_sum, cycle_count', x_avg_sum, y_avg_sum, cycle_count)
    #     x_avg_sum_avg = np.floor(x_avg_sum / cycle_count)
    #     y_avg_sum_avg = np.floor(y_avg_sum / cycle_count)
    #     print('avg_sum', x_avg_sum_avg, y_avg_sum_avg, )
    #     mouse_x = int((x_avg_sum_avg * ratio_x) * config['scale_x'])
    #     mouse_y = int((y_avg_sum_avg * ratio_y) * config['scale_y'])
    #     t = threading.Thread(target=moveMouse, args=(mouse_x, mouse_y, ), )
    #     t.start()
    #     threads.append(t)
    #     # print(x_avg_sum_avg, y_avg_sum_avg)
    #     # reset avg, counter and timer
    #     cycle_count = config['recycle_multiplier'] + config['center_multiplier']
    #     cycle_start = time.time()
    #     # x_avg_sum = center_x
    #     # y_avg_sum = center_y
    #     x_avg_sum = (x_avg_sum_avg * config['recycle_multiplier']) + (center_x * config['center_multiplier'])
    #     y_avg_sum = (y_avg_sum_avg * config['recycle_multiplier']) + (center_y * config['center_multiplier'])
        
    # frame_out = cv2.circle(frame_crop, (int(x_avg), int(y_avg)), 4, (255, 0, 0), -1)
    # frame_out = cv2.circle(frame_crop, (int(x_avg_sum_avg), int(y_avg_sum_avg)), 40, (0, 0, 255), -1)
    # print('int(x_avg_sum_avg), int(y_avg_sum_avg)', int(x_avg_sum_avg), int(y_avg_sum_avg))
    # Display the resulting frame


    cv2.imshow('Frame_original', frame_out)
    # cv2.imshow('fg_mask', fg_mask)
    # cv2.imshow('Frame_ct', frame_ct)
    # cv2.imshow('Frame_final', frame_out)
    # Write the output video 
    out.write(frame_out.astype('uint8'))
    # print('loop')


    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
# and release the output
out.release()

cv2.destroyAllWindows()

# Wait for threads to finish
for t in threads:
    t.join()


