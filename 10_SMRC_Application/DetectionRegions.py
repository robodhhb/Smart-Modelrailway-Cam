#!/usr/bin/python3
############################################################
# Class DetectionRegions
# This class realizes a container for detection regions
# which are a rectangular area on an image where objects
# shall be detected. It also holds the current detected
# class for each region and the last position (upper left
# corner of rectangle) of the class detected.
#
# File: DetectionRegions.py
# Author: Detlef Heinze 
# Version: 1.1  Date: 29.06.2022    
###########################################################

import json #Access to json files

import trainstate as ts #Possible states of objects


#This class implements the detection regions on an image. 
class DetectionRegions(object):
    
    # Constructor which defines default values for settings
    def __init__(self, aLabelDict):
        self.detectionRegionDict= {} #All regions for detection
        self.detectedObjDict = {}  # For each region a set holding
                                   # the actual detected train classes
        self.name=""
        self.input_JSON_file= "detectionRegions.json"
        
        self.importJSON(self.input_JSON_file)
        
        #Create an initialized  dictionary which holds the last allocation of the train
        #elements seperated for each region and within a region for each
        #train element (=class). The allocation is (x,y) of the upper left
        #corner of the rectangle around the detected train element.
        #None means that there is no train element of the class in that region.
        #With this information we can determine if the train element is new
        #in the region, moving or stopping. This is stored in the classState.
        self.classAllocation= {}
        self.classState= {}
        for region in self.detectionRegionDict:
            self.classAllocation[region]= {}
            self.classState[region]= {}
            for key in aLabelDict:
                #aLabelDict is a dictionary with class-number as key and
                #class names (the train elements) as strings.
                self.classAllocation[region][aLabelDict[key]]= None
                self.classState[region][aLabelDict[key]]= ts.TrainState.initial
        
        self.allClassesSet= set()
        for key in aLabelDict:
            self.allClassesSet.add(aLabelDict[key])
            
    #Add a recangular region with name and (x1,y1, x2,y2)as bbox
    def addRegion(self, name, bbox):
        self.detectionRegionDict[name]= bbox
        
    #Return the region with name   
    def getRegion(self, name):
        return self.detectionRegionDict[name]
    
    #Get the whole dictionary with all regions
    def getRegions(self):
        return self.detectionRegionDict
    
    #Get all region names
    def getRegionNames(self):
        return list(self.detectionRegionDict)
    
    #Return the number of regions
    def countRegions(self):
        return len(self.getRegionNames())
    
    #Import regions from a json file.
    def importJSON(self, input_file):
        print('\nImporting: ', input_file)
        try:
            with open(input_file) as json_file:
                data = json.load(json_file)
                self.name= data['name']
                print("Detection regions for: ", self.name)
                for region in data['regions']:
                    name= region['name']
                    bbox= (region['x1'], region['y1'],region['x2'],region['y2'])
                    print(name, bbox)
                    self.addRegion(name,bbox)
                    self.detectedObjDict[name]= set()
        except:
            print('Error: Could not import', self.input_JSON_file)
            print('Using one default detection region: 300 x 300 pixel')
            self.addRegion('Default', (10, 10, 310, 310))
            self.detectedObjDict['Default']= set()
    
    #Return the dictionary holding currently detected objects
    #after clearing.
    def getClearedDetectedObjDict(self):
        for region in self.detectionRegionDict:
            self.detectedObjDict[region]= set()
        return self.detectedObjDict
    
    #Update the location of a detected object with classname and region
    #and the x,y position on image. If the class has been detected on the
    #last image it is calculated if it moves or has stopped. This functionality
    #applies to all classes which name start with ':'. This are locomotives.
    #We can only detect motion for classes which are unique in a region. Therefore
    #two or more same locomotives in one region are forbidden. 
    def updateEngineAllocation(self, regionName, classname, x, y, parent_conn):
        if classname[0]== ':': #Is classname an engine?
            if self.classAllocation[regionName][classname] is None:
                self.classAllocation[regionName][classname]= (x,y)
                print('New allocation:', classname)
            else:
                lastPosition= self.classAllocation[regionName][classname]
                self.classAllocation[regionName][classname]= (x,y)
                if (abs(lastPosition[0] - x) + abs(lastPosition[1] -y)) > 11: 
                    if self.classState[regionName][classname] != ts.TrainState.moving:
                        self.classState[regionName][classname]= ts.TrainState.moving
                        
                        parent_conn.send([regionName,classname, ts.TrainState.moving])
                elif (self.classState[regionName][classname] != ts.TrainState.stopped) and \
                          x > 10 and y > 10: #for the case if it is at the lower borders
                    self.classState[regionName][classname]= ts.TrainState.stopped
                
                    parent_conn.send([regionName,classname, ts.TrainState.stopped])
    
    
    #Find out for all classes which name start with ':' if it has been detected
    #on the last image (or has initial state) but is now absent. Update
    #state to absent and send a message to the child process for rule checking.
    def updateEngineAbsentState(self, parent_conn):
        for region in self.detectionRegionDict:
            if len(self.detectedObjDict[region]) == 0:#Actual nothing detected in region
                for classname in self.allClassesSet:
                    #if classname is an engine and last state != absent
                    if classname[0]== ':' and self.classState[region][classname] != ts.TrainState.absent:
                        self.classState[region][classname]= ts.TrainState.absent
                        self.classAllocation[region][classname]= None
                        
                        parent_conn.send([region,classname, ts.TrainState.absent])
            else:
                #Find all classes not in a region
                diffSet=self.allClassesSet.difference(self.detectedObjDict[region])
                for classname in diffSet:
                    #if classname is an engine and is absent
                    if classname[0]== ':' and self.classState[region][classname] != ts.TrainState.absent:
                        self.classState[region][classname]= ts.TrainState.absent
                        self.classAllocation[region][classname]= None
                        
                        parent_conn.send([region,classname, ts.TrainState.absent])
        
    #Return for a region the state string describing the states of
    #the locomotives in that region
    def getStateString(self, regionName):
        str=''
        for aClass in self.classState[regionName]:
            state= self.classState[regionName][aClass]
            if state == ts.TrainState.stopped:
                str= str + "hält "
            elif state == ts.TrainState.moving:
                str= str+ "fährt "
        return str
    
    #Set all class states to initial state
    def resetClassStates(self):
        for region in self.detectionRegionDict:
            for className in self.allClassesSet:
                self.classState[region][className]= ts.TrainState.initial

        
if __name__ == "__main__":
    detReg= DetectionRegions({0: ':Engine0', 1: ':Engine1'})
    print(detReg.getRegion('Gleis 2'))
    print(detReg.getRegionNames())
    print('Size: ', detReg.countRegions())
    print(detReg.detectedObjDict)
    
    
   
        
    
    
        
        