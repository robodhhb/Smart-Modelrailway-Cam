#!/usr/bin/python3
###############################################################
# Main application file for the Smart Modelrailway-Cam.
# It implements object detection with the Coral USB
# Accelarotor (Edge TPU Coprozessor) using an EfficentDet
# Model. It has been trained using transfer learning with
# images model locomotives and wagons (Spur N). 
# This file is for use on a Raspberry 4B
# running PiOS Buster (Legacy)
#
# File: SMRC_Main.py
# Author: Detlef Heinze 
# Version: 1.1    Date: 29.06.2022  
###########################################################

import tkinter as tk
import platform as pf
#see more imports below if it runs on Raspberry Pi


# Return if this code is running on a Raspberry Pi
def get_platform():
    info= pf.uname()
    try:
        from picamera import PiCamera
        if info.system == 'Linux':
            print('Running on Raspberry Pi using PiCamera for camera access.')
            return 'RaspberryPi'
        else:
            print('Running on Raspberry Pi but not on Linux. Aborting...')
            return'None'
    except:
        print('Running on a not supported platform:', info.system)
        return'None'

# Behaviour of window close button
def on_closing():
    if mainWin.cameraState == myView.CamState.off:
        if hasattr(mainWin, "smrcc"):
            mainWin.smrcc.terminate_child_process()
        root.destroy()
        print("Window closed")
    else:
        print('Stop camera before closing window.')

#Create an start main application window
print("\nStarting Smart Model-Railway-Cam 1.0\n")
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)

runningOn= get_platform()
#Import the needed modules
#and create the main window.
if runningOn == 'RaspberryPi':
    import SMRC_View as myView
    mainWin= myView.SMRC_View(root)
    #Start window if initialisations are successfull
    if mainWin.initOK:
        root.mainloop()
    else:
        on_closing()
    