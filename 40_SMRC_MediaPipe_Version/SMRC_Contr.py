#!/usr/bin/python3
############################################################
# Class SMRC_Contr
# This class realizes the application control code for
# using a camera
# This class invokes a parallel process for rule checking.
#
# File: SMRC_Contr.py
# Author: Detlef Heinze 
# Version: 2.0    Date: 20.11.2023   
###########################################################

from picamera2 import Picamera2

import time
import numpy as np
from PIL import ImageDraw as D

#Imports for the mediapipe object-detection task
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#Imports for parallel execution of rule checker process
from multiprocessing import Process, Pipe

#Checking the version of a package
from importlib.metadata import version

#Projec imports
from DetectionRegions import DetectionRegions
import RuleChecker as rc

#The controller class for the SMRC
class SMRC_Contr(object):
    
    # Constructor which defines default values for settings
    def __init__(self,
                 aView,
                 minObjectScore= 0.52,
                 threshold= 5):  #detect up to 5 objects
        
        self.myView= aView
        
        #Initialization for object detection
        self.default_model ='SMRC_model_qat_int8.tflite' #An int8 model trained with qauntized aware training
        self.default_labels = 'railwayLabels.txt'
        self.default_threshold= minObjectScore
        self.default_top_k= threshold    # max count of detected objects
        print('Initializing Mediapipe Object Detector')
        print("MediaPipe Version:",version('mediapipe'))
        print('Loading {} with {} labels.'.format(self.default_model, self.default_labels))
        print('A maximum of {} objects are detected with a score greater than {}.'.format(self.default_top_k, self.default_threshold))
        
        #Initialize MediaPipe object detction task
        BaseOptions = mp.tasks.BaseOptions
        ObjectDetector = mp.tasks.vision.ObjectDetector
        ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = ObjectDetectorOptions(
            base_options=BaseOptions(model_asset_path= self.default_model),
            max_results=self.default_top_k,
            score_threshold= self.default_threshold,
            running_mode=VisionRunningMode.IMAGE)
        self.detector= ObjectDetector.create_from_options(options)
        
        self.labels = self.read_label_file(self.default_labels)      
        self.inference_size = (320,320)
        print('Inference size: ', self.inference_size )
        
        print('\nDetectable classes:')
        for aLabel in self.labels:
            print(self.labels.get(aLabel, aLabel))
        
        #Image counter for canvas
        self.imageObj=0
        
        #Initialize the detection regions
        self.detRegions= DetectionRegions(self.labels)
        
        #Initialize the RuleChecker and start parallel process
        print('\nInitializing RuleChecker...')
        self.ruleChecker= rc.RuleChecker(self)
        self.parent_conn, self.child_conn = Pipe() #Pipe for communication
        self.child_process = Process(target=self.ruleChecker.checkRules,
                                     args=(self.child_conn,))
        print('Starting rule checker process')
        self.child_process.start()
    
    #Read the label file and create a dictionary
    #with key = linenumber and value= text of line
    def read_label_file(self,aFilename):
        with open(aFilename, 'r') as file:
            lines = file.readlines()
        return {i: line.strip() for i, line in enumerate(lines, 1)}
    
    
    # Configure PiCam
    # Return parameter: created PiCam
    def configurePiCam(self):
        print("Configuring Picamera2:", self.inference_size)
        self.cam = Picamera2()
        config = self.cam.create_still_configuration(
                        main={"size": self.inference_size})
        self.cam.configure(config)
        self.cam.start()
        time.sleep(2)
        return self.cam
    
    #Take a photo and return a PIL image
    def takePhoto(self):
        
        return self.cam.capture_image("main")
    
    #Predict the picture using the detector and return a list of detections.
    def predict_image(self, pil_image):
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB, data=np.asarray(pil_image))
        return self.detector.detect(mp_image)
        
    #Get and process the results of inference. Update image with objects found.
    def process_inference_results(self, image, detection_result, showDetectionRegions=False):
        
        return self.append_objs_to_img(image, detection_result.detections, self.labels, showDetectionRegions)
    
    #Add a rectangle, score and object class name to each object found on image.
    #Additionally add detection regions if user want it.
    #Calculate which detected object overlaps a region and update state
    def append_objs_to_img(self, image, detections, labels, showDetectionRegions=False):
        draw= D.Draw(image)
        #Clear detectObjDict for use with actual detected objects
        detectedObjDict= self.detRegions.getClearedDetectedObjDict()
        for detection in detections:
            #print(detection)
            bbox = detection.bounding_box
            x0, y0 = bbox.origin_x, bbox.origin_y
            x1, y1 = x0 + bbox.width, y0+ bbox.height

            classname= detection.categories[0].category_name
            percent= detection.categories[0].score*100
            label = '{:2.0f}% {}'.format(percent,classname )
            draw.rectangle([(x0, y0), (x1, y1)],outline= 'white', width=2)
            draw.text((x0+5, y0+4),label)
            
            #Detect overlap of object with a detection region
            for regionName in self.detRegions.getRegionNames():
                if self.isRectangleOverlap(self.detRegions.getRegion(regionName), (x0,y0,x1,y1)):
                    detectedObjDict[regionName].add(classname) 
                    self.detRegions.updateEngineAllocation(regionName, classname,x0,y0, self.parent_conn)
                    break #One obj can only be in one region
        
        self.detRegions.updateEngineAbsentState(self.parent_conn)
        
        #Update the table showing which train element is on image in which region
        self.myView.updateTable(self.detRegions)
        #Show the detection regions on image if checkbox is selected
        if showDetectionRegions:
            for regionName in self.detRegions.getRegionNames():
                region= self.detRegions.getRegion(regionName)
                draw.rectangle([(region[0], region[1]), (region[2], region[3])],
                               outline= 'white', width=1)
                draw.text((region[0]+3, region[1]-10),regionName)
                
        return image
    
    #Utility for checking if two recangles overlap
    def isRectangleOverlap(self, r1, r2):
        if (r1[0]>=r2[2]) or (r1[2]<=r2[0]) or (r1[3]<=r2[1]) or (r1[1]>=r2[3]):
            return False
        else:
            return True
    
    #Process results after checking rules.
    #Poll parent_conn to check if the rule checker
    #process has delivered a change of rule violation status. 
    def process_ruleChecker_results(self, myView):
        #Update the violationsTabel on the view if
        #rule checker process has delivered an update
        while self.parent_conn.poll():
            updateDict= self.parent_conn.recv()
            myView.updateViolationsTable(updateDict)
            
    #Terminate the rule checker process
    def terminate_child_process(self):
        self.child_process.terminate()
        self.child_process.join()
        if not self.child_process.is_alive():
            print('Rule checker process terminated')
        
        
            
        
    
        
        
