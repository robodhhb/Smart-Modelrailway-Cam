#!/usr/bin/python3
################################################################
# class SMRC_View
# This file implements a view for the Smart Modelrailway-Cam
# on a Raspberry Pi. 
#
# File: SMRC_View.py
# Author: Detlef Heinze 
# Version: 1.1    Date: 29.07.2022   
################################################################

#Imports for user interface
import tkinter as tk
from tkinter import ttk
import enum
import time


#Imports for image preparation and display
from PIL import Image, ImageTk

#Import of own modules
from SMRC_Contr import SMRC_Contr


# Possible states of camera
class CamState(enum.Enum): 
    off = 0
    on = 1
    
#The window class of the application
class SMRC_View(object):

    #Initialize a new SMRC_View
    def __init__(self, master):
        self.master = master
        self.master.geometry('900x430')
        self.master.resizable(0, 0)
        master.title("  Smart Model-Railway-Cam 1.0")
        self.cameraState=CamState.off
        self.initOK= True

        print('Initializing Coral EdgeTPU...')
        try:
            self.smrcc= SMRC_Contr(self)
        except Exception as e:
            self.initOK= False
            print('   ERROR: Coral EdgeTPU is not connected or wrong model format.')
            print(e)  
        else:
            print('Initializing video capture...')
            self.smrcc.configurePiCam()
            self.vertRes= self.smrcc.inference_size[0]
            self.horzRes= self.smrcc.inference_size[1]
            
            self.canv = tk.Canvas(self.master, height=self.vertRes,width= self.horzRes)
            self.canv.grid(column=0, row=0, pady=10, padx= 10) 
            self.canv.create_rectangle(4,4,self.horzRes-1, self.vertRes-1 )

            self.canv.create_text(self.vertRes/2, self.horzRes/2, text='Camera OFF', anchor='center', \
                              font=('TkMenuFont', '20', 'bold'), fill='blue')
            
            self.checkFrame= tk.Frame(self.master)
            self.checkFrame.grid(column=0,row=1)

            self.showDetectRegions= tk.BooleanVar()  
            self.showDetectRegions.set(False)
            self.checkDetectionRegion = tk.Checkbutton(self.checkFrame,text='Bereiche anzeigen', variable=self.showDetectRegions)
            self.checkDetectionRegion.pack(anchor= 'nw')
            
            self.btnStartStop= tk.Button(self.checkFrame, text="Start Camera", \
                                      command=self.btnStartStop_clicked)
            self.btnStartStop.pack(pady=12)
            
            self.insertStateTable()
            self.insertViolationsTable()
            
            print('Opening window')
    
    #Insert a table on view with one row for each detection region and three colomns
    #for each row: Name of region, allocation and state of locomotives.
    def insertStateTable(self):
        self.frameDetectRegions= ttk.Frame(self.master)
        self.frameDetectRegions.grid(column=1, row=0, sticky= "n", pady=12, ipady=10)
        
        temp=tk.Label( self.frameDetectRegions,text="Bereich", font=('TkMenuFont', '10', 'bold'))
        temp.grid(column=1, row=0)
        temp=tk.Label( self.frameDetectRegions,text="Belegung", font=('TkMenuFont', '10', 'bold'))
        temp.grid(column=2, row=0)
        temp=tk.Label( self.frameDetectRegions,text="Lok", font=('TkMenuFont', '10', 'bold'))
        temp.grid(column=3, row=0)
        self.nothingDetected="------------------------------------------------------------------------"
        self.noState="------------"
        
        self.rows= self.smrcc.detRegions.countRegions()
        self.dataTableDict= {}
        regionNames= self.smrcc.detRegions.getRegionNames()
        for i in range(self.rows):
            temp1= tk.Label( self.frameDetectRegions,text=regionNames[i], font=('TkMenuFont', '11', 'normal'))
            temp1.grid(column=1, row=i+2)
            temp2= tk.Label( self.frameDetectRegions,text=self.nothingDetected, font=('TkMenuFont', '11', 'normal'))
            temp2.grid(column=2, row=i+2, padx=15, sticky= 'nw')
            temp3= tk.Label( self.frameDetectRegions,text=self.noState, font=('TkMenuFont', '11', 'normal'))
            temp3.grid(column=3, row=i+2, padx=15)
            self.dataTableDict[regionNames[i]] = [temp1,temp2,temp3]    
    
    #Insert a table on view with one row for each detection region and two colomns
    #for each row: Name of region and rule violations in that reagion
    def insertViolationsTable(self):
        startRow= self.rows + 5
        self.noViolationStr="------------------------------------------------------------------------------------------"
        temp=tk.Label( self.frameDetectRegions,text=" ", font=('TkMenuFont', '10', 'bold'))
        temp.grid(column=1, row= startRow)
        temp=tk.Label( self.frameDetectRegions,text="Bereich", font=('TkMenuFont', '10', 'bold'))
        temp.grid(column=1, row= startRow+1)
        temp=tk.Label( self.frameDetectRegions,text="Regelverletzungen", font=('TkMenuFont', '10', 'bold'))
        temp.grid(column=2, row=startRow+1)
        
        self.violationsTableDict= {}
        regionNames= self.smrcc.detRegions.getRegionNames()
        for i in range(self.rows):
            temp1= tk.Label( self.frameDetectRegions,text=regionNames[i], font=('TkMenuFont', '11', 'normal'))
            temp1.grid(column=1, row=startRow+i+2)
            temp2= tk.Label( self.frameDetectRegions,text=self.noViolationStr,font=('TkMenuFont', '11', 'normal'))
            temp2.grid(column=2, row=startRow+i+2, padx=15, columnspan= 2, sticky= 'nw')
            self.violationsTableDict[regionNames[i]] = [temp1,temp2]  
    
    # Event Handler
    # Event handler for switching camera on and off
    def btnStartStop_clicked(self):
        if self.cameraState == CamState.off:
            self.cameraState= CamState.on
            self.imageCount=0
            self.startTime= time.time()
            self.btnStartStop['text']= 'Stop camera'
            self.runCamera()
        else:
            self.cameraState= CamState.off
            print('Stopping camera')
            self.btnStartStop['text']= 'Start camera'
            self.duration= time.time()-self.startTime
            if self.smrcc.imageObj > 0:
                self.smrcc.imageObj= 0
            self.clearTables()
            self.resetClassStates()
            print('\nImages taken:', self.imageCount)
            print('Images taken per second: ', self.imageCount/self.duration)
            print('Duration: ', self.duration, 's')
            print()

    # Functions
    
    #Update table with actual train elements on image
    def updateTable(self, detRegions):
        for regionName in detRegions.getRegionNames():
            #Join the string elements in a set to one string
            outputStr= '-'.join(detRegions.detectedObjDict[regionName])
            if outputStr == '':
                self.dataTableDict[regionName][1]['text']= self.nothingDetected
            else:
                self.dataTableDict[regionName][1]['text']= outputStr
            
            outputStr= detRegions.getStateString(regionName)
            if outputStr == '':
                self.dataTableDict[regionName][2]['text']= self.noState
            else:
                self.dataTableDict[regionName][2]['text']= outputStr
    
    #Clear all rows and colomns of the tables.
    def clearTables(self):
        for regionName in self.smrcc.detRegions.getRegionNames():
            self.dataTableDict[regionName][1]['text']= self.nothingDetected
            self.dataTableDict[regionName][2]['text']= self.noState
            self.violationsTableDict[regionName][1]['text']= self.noViolationStr
    
    #Set all class states to initial states.
    def resetClassStates(self):
        self.smrcc.detRegions.resetClassStates()
    
    #Update the violation table for regions in the updateDict
    def updateViolationsTable(self, updateDict):
        for region in updateDict:
            self.violationsTableDict[region][1]['text']= updateDict[region]
    
    #Main loop for the Smart Modelrailway-Cam
    def runCamera(self):
        print('Starting camera')
        imageObj= -1
        
        while self.cameraState == CamState.on:
            picData = self.smrcc.takePhoto() #take a photo
            img= Image.frombytes('RGB', (picData.shape[1],picData.shape[0]),
                                 picData.astype('b').tostring())
            
            #Run inference on Coral EdgeTPU and process results
            self.smrcc.predict_image(picData)
            img= self.smrcc.process_inference_results(img, self.showDetectRegions.get())
            #Save PhotoImage to member variable. This
            #prevents the image to be garbage collected
            #before it is displayed.
            self.image= ImageTk.PhotoImage(image=img)
            #Delete last image from canvas.
            if imageObj > 0:
                self.canv.delete(imageObj)
            #Add actual image to canvas
            imageObj= self.canv.create_image(0,0,image=self.image, anchor= 'nw' )
            self.canv.update()
            self.imageCount+=1
            self.smrcc.process_ruleChecker_results(self)
        #Delete last image to show text on canvas
        self.canv.delete(imageObj) 

    

