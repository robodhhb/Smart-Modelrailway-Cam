#############################################################
# imageSequence for Raspberry Pi
# This program takes a sequence of images with the Pi-Camera.
# Started with no arguments it takes within 2 seconds 14
# images with resolution 320 x 320.
#
# Parameter:
#    -wt aNumber   Width of resolution
#    -ht aNumber   Height of resolution
#    -d  aNumber   Timespan to take pictures (Millisecons)
#    -f  aNumber   Frames per second 
#
# The image sequence is taken after pressing button "t". 
# Exit with any button. 
#
#
# File: imageSequence.py
# Author: Detlef Heinze 
# Version: 1.1    Date: 22.06.2022       
###########################################################

import time
import picamera
import argparse

parser = argparse.ArgumentParser(prog = 'imageSequence',
    description = 'Take a sequence of images')

parser.add_argument('-wt', '--width', type=int, default=320)
parser.add_argument('-ht', '--height', type=int, default=320)
parser.add_argument('-d', '--duration', type=int, default=2000) #ms
parser.add_argument('-f', '--fps', type=int, default=7)
args = parser.parse_args()
print(args)

with picamera.PiCamera() as camera:
    camera.resolution = (args.width, args.height)
    camera.framerate = args.fps
    print("Camera warm up....")
    camera.start_preview()
    # Give the camera some warm-up time
    time.sleep(2)
    start = time.time()
    camera.stop_preview()
    
    picCount= int(args.duration/1000*args.fps)
    while input("Press 't' and enter to take images. Any key to exit: ") == 't':
        for i, filename in enumerate(
                camera.capture_continuous('image{timestamp:%d%b%y%H%M%S%f}.jpg', use_video_port=True)):
            print(filename)
            if i == picCount-1:
                break  
    
    