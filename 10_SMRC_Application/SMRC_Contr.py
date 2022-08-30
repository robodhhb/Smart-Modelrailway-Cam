#!/usr/bin/python3
############################################################
# Class SMRC_Contr
# This class realizes the application control code for
# using a camera and a Coral Edge TPU for inferencing.
# The Coral EdgeTPU is accessed via the PyCoral-API.
# This class invokes a parallel process for rule checking.
#
# File: SMRC_Contr.py
# Author: Detlef Heinze 
# Version: 1.1    Date: 29.07.2022    
###########################################################

from picamera import PiCamera
from time import sleep
import numpy as np
from PIL import Image, ImageTk, ImageDraw as D

#Imports for object detection on Coral USB Accelerator
#(EdgdeTPU)
from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference
from pycoral.utils.edgetpu import get_runtime_version

#Imports for parallel execution of rule checker process
from multiprocessing import Process, Pipe

#Projec imports
from DetectionRegions import DetectionRegions
import RuleChecker as rc

#The controller class for the SMRC
class SMRC_Contr(object):
    
    # Constructor which defines default values for settings
    def __init__(self,
                 aView,
                 minObjectScore= 0.6,
                 threshold= 5,  #detect up to 5 objects
                 useVideoPort = True):
        
        self.myView= aView
        
        #Initialization of the EdgeTPU and object detection
        self.default_model ='smrc_model_edgetpu.tflite' #for edgetpu runtime >= Vers. 13
        self.default_labels = 'railwayLabels.txt'
        self.default_threshold= minObjectScore
        self.default_top_k= threshold    # max count of detected objects
        print('Loading {} with {} labels.'.format(self.default_model, self.default_labels))

        print('Installed EdgeTPU runtime version:',get_runtime_version())

        self.interpreter = make_interpreter(self.default_model)
        self.interpreter.allocate_tensors()
        
        self.labels = read_label_file(self.default_labels)      
        self.inference_size = input_size(self.interpreter)
        print('Inference size: ', self.inference_size )
        print('Top_k: ', self.default_top_k)
        print('Threshold:', self.default_threshold)
        print('\nDetectable classes:')
        for aLabel in self.labels:
            print(self.labels.get(aLabel, aLabel))
        
        #camera settings
        self.useVideoPort= useVideoPort
        
        #Image counter for canvas
        self.imageObj=0
        
        #Initialize the detection regions
        self.detRegions= DetectionRegions(self.labels)
        
        #Initialize the RuleChecker and start parallel process
        self.ruleChecker= rc.RuleChecker(self)
        self.parent_conn, self.child_conn = Pipe() #Pipe for communication
        self.child_process = Process(target=self.ruleChecker.checkRules,
                                     args=(self.child_conn,))
        print('Starting rule checker process')
        self.child_process.start()
        print()   
    
    
    # Configure PiCam
    # Return parameter: created PiCam
    def configurePiCam(self):
        print("\nConfigure and warming up PiCamera")
        self.cam = PiCamera()
        self.cam.resolution= self.inference_size
        print("Camera resolution: " + repr(self.cam.resolution))
        self.cam.start_preview()
        sleep(2)
        self.cam.stop_preview()
        return self.cam
    
    #Take a photo returned as numpy array
    def takePhoto(self):
        picData = np.empty((self.cam.resolution[1],
                            self.cam.resolution[0], 3),
                            dtype=np.uint8)
        self.cam.capture(picData, format= 'rgb', use_video_port=self.useVideoPort) #24bit rgb format
        return picData
    
    
    #Predict the picture by running it on the TPU
    def predict_image(self, picData):
        #Call the TPU to detect objects on the image with a neural network
        run_inference(self.interpreter,picData.tobytes())

    #Get and process the results of inference. Update image with objects found.
    def process_inference_results(self,image, showDetectionRegions=False):
        self.objs = get_objects(self.interpreter, self.default_threshold)[:self.default_top_k]
        return self.append_objs_to_img(image, self.objs, self.labels, showDetectionRegions)
    
    #Add a rectangle, score and object class name to each object found on image.
    #Additionally add detection regions if user want it.
    #Calculate which detected object overlaps a region and update state
    def append_objs_to_img(self, image, objs, labels, showDetectionRegions=False):
        #height, width, channels = image.shape
        draw= D.Draw(image)
        #Clear detectObjDict for use with actual detected objects
        detectedObjDict= self.detRegions.getClearedDetectedObjDict()
        for obj in objs:
            bbox = obj.bbox
            x0, y0 = int(bbox.xmin), int(bbox.ymin)
            x1, y1 = int(bbox.xmax), int(bbox.ymax)

            percent = int(100 * obj.score)
            classname= labels.get(obj.id, obj.id)
            label = '{}% {}'.format(percent,classname )
              
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
        
        
            
        
    
        
        
