#!/usr/bin/python3
############################################################
# Convert the VIA export file "VIA_SMRC_json.json" 
# in json-format to csv for Google model maker. 
# Divide the region set in 80% training data,
# 10% validation data and 10% test data using a random
# generator.
#
# Run this program in the folder where the input file
# and the images are located. 
#
#
# File: VIAjson2MadelMaker.py
# Author: Detlef Heinze 
# Version: 1.1    Date: 27.06.2022       
###########################################################
  
import PIL 
from PIL import Image
import json
import csv
import os
import time
import random 

input_file= 'VIA_SMRC_json.json'
output_file= 'training.csv'
#The following colab_file_path (Google Colaboratory) is stored in each 
#line of the output file. It is not accessed from this program
colab_file_path= '/content/drive/MyDrive/TrainData/' 

print('Processing....')
startTime= time.time()
cwd= os.path.abspath(os.getcwd()) 
print(cwd)
# Opening JSON file
with open(input_file) as json_file:
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        data = json.load(json_file)
        count= 0
        countRegion= 0
        countTest=0
        countTrain=0
        countValidation= 0
        for pic in data:
            #Get filename and read it to get resolution
            filename= data[pic]['filename']
            img = Image.open(filename)
            imWidth, imHeight = img.size
            print('Processing: ', filename, ': ', imWidth, ' x ', imHeight)
            #print(data[pic])
            #for key in data[pic]:
            #    print('    ',key)
            
            #print(data[pic]['regions'])
            for region in data[pic]['regions']:
                #print(region)
                #for key1 in region:
                #    print('    ', key1)
                #    print('    ',region[key1])
                classname= region['region_attributes']['classname']
                print('    Classname: ', classname)
                x_topLeft= region['shape_attributes']['x']
                y_topLeft= region['shape_attributes']['y']
                x_bottomRight= x_topLeft + region['shape_attributes']['width']
                y_bottomRight =y_topLeft + region['shape_attributes']['height']
                print('    Absolut coordinates: ', x_topLeft,y_topLeft,x_bottomRight, y_bottomRight)
                x_topLeft = x_topLeft/imWidth
                y_topLeft=  y_topLeft/imHeight
                x_bottomRight = x_bottomRight/imWidth
                y_bottomRight = y_bottomRight/imHeight
                print('    Relative coordinates:', x_topLeft,y_topLeft,x_bottomRight, y_bottomRight)
                #Choose rowType with 80% TRAIN, 10% VALIDATION and 10% TEST
                rand= random.random()
                if rand <= 0.8:
                    rowType= 'TRAIN'
                    countTrain+=1
                elif rand <= 0.9:
                    rowType='VALIDATION'
                    countValidation+=1
                else:
                    rowType= 'TEST'
                    countTest+=1
                #Build the row-string now
                row= [rowType, colab_file_path + filename, classname, x_topLeft,y_topLeft, None , None, \
                      x_bottomRight, y_bottomRight, None, None] #None=empty cell
                writer.writerow(row)
                countRegion+=1
            img.close()
            count+=1
        print(count, 'pictures processed with', countRegion, 'regions in')
        print(round(time.time() - startTime,4), 'seconds')
        print('Number of training data', countTrain)
        print('Number of validation data', countValidation)
        print('Number of test data', countTest)
            