#!/usr/bin/python3
###############################################################
# Main application file for the Smart Modelrailway-Cam.
# It implements object detection using the Google MediaPipe
# object detection task. It uses a Mobilenet
# Model. It has been trained using transfer learning with
# images of model locomotives and wagons (Spur N).
# The MediaPipe ModelMaker trained the model on CoLab.
# This file is for use on a Raspberry 4B
# running PiOS Bullseye 64bit or higher
#
# File: SMRC_Main.py
# Author: Detlef Heinze 
# Version: 2.0   Date: 20.11.2023 
###########################################################

import tkinter as tk
import platform as pf
#See more imports below if it runs on Raspberry Pi

# Return "RaspberryPi" if this code is running on a Raspberry Pi
# with Picamera2 installed. 
def get_platform():
    info= pf.uname()
    try:
        from picamera2 import Picamera2
        if info.system == 'Linux':
            print('Running on Raspberry Pi using Picamera2 for camera access.')
            return 'RaspberryPi'
        else:
            print('Picamera2 is not supported on your system. Aborting...')
            return'None'
        
    except:
        print('Running on a not supported platform or legacy PiOS like PiOS Buster or older:',info.system)
        return'None'

# Behaviour of window close button
def on_closing():
    if mainWin.cameraState == myView.CamState.off:
        if hasattr(mainWin, "smrcc"):
            print('\nStopping application')
            mainWin.smrcc.terminate_child_process()
            print('Stopping camera')
            mainWin.smrcc.cam.stop()
        root.destroy()
        print("Window closed")
    else:
        print('Stop camera before closing window.')

#Create an start main application window
print("\nStarting Smart Model-Railway-Cam 2.0\n")
runningOn= get_platform()

if runningOn == 'RaspberryPi':
    #Import the needed modules
    #and create the main window.
    import SMRC_View as myView
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mainWin= myView.SMRC_View(root)
    #Start window if initialisations are successfull
    if mainWin.initOK:
        root.mainloop()
    else:
        on_closing()
else:
    print('Abort after fatal error')
    