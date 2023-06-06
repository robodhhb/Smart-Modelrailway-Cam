############################################################
# Training of the model for the Smart-Model-Railway-Cam
# This program implements transfer-learning. It cannot
# be executed in isolation. It is called from the jupyter
# notebook "trainSMRC.ipynb". 
#
# File: train.py
# Author: Detlef Heinze 
# Version: 1.0    Date: 06.06.2023   
###########################################################
import numpy as np
import os

from tflite_model_maker.config import QuantizationConfig
from tflite_model_maker.config import ExportFormat
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

import tensorflow as tf
assert tf.__version__.startswith('2')

from pprint import pprint #Pretty printing for output

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)

print("\nTransfer-Learning")
print("Splitting trainng data into training-,validation- and test-data).")
train_data, validation_data, test_data = object_detector.DataLoader.from_csv('training.csv')

print("\nUsing an EfficientDet-Lite0 model for training with 320x320 image resolution.")
spec = object_detector.EfficientDetLite0Spec()

print("\nTraining starts......")
model = object_detector.create(train_data=train_data, 
                               model_spec=spec, 
                               validation_data=validation_data, 
                               epochs=40, 
                               batch_size=8, 
                               train_whole_model=True)
print("\nEvaluating created model")
print("Evaluation result:") 
result= model.evaluate(test_data)                             
pprint(result, width=10)

TFLITE_FILENAME = 'smrc_model.tflite'
LABELS_FILENAME = 'railwayLabels.txt'

print("\nExport model to tflite-format")
model.export(export_dir='.', tflite_filename=TFLITE_FILENAME, label_filename=LABELS_FILENAME,
             export_format=[ExportFormat.TFLITE, ExportFormat.LABEL])

print("\n\nEvaluating tflite-model") 
print("Evaluation result:")             
result= model.evaluate_tflite(TFLITE_FILENAME, test_data)
pprint(result, width=10)

             
     


                               