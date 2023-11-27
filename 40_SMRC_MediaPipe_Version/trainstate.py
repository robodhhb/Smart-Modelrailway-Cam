#!/usr/bin/python3
############################################################
# This file contains utilities for the SMRC project
#
# File: trainstate.py
# Author: Detlef Heinze 
# Version: 2.0    Date: 20.11.2023 
###########################################################

import enum #Acces to enumertaion class type

# Possible states of a train element
class TrainState(enum.Enum):
    initial = 0 #state at startup
    absent =  1 #not visible on image in a detection region
    stopped = 2 #has stopped in a detection region
    moving =  3 #is moving in a detection region