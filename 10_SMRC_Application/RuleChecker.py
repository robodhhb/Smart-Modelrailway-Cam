#!/usr/bin/python3
############################################################
# Class Rule_Checker
# This class realizes a rule checker for for the SMRC.
# It runs in it's own process (function checlRules) started
# by the SMRC_Contr.
#
# File: RuleChecker.py
# Author: Detlef Heinze 
# Version: 1.1    Date: 29.07.2022    
###########################################################

import json #Access to json files

import trainstate as ts
import MailSender as ms #For sending eMails with rule violations
import time

#The RuleChecker class
class RuleChecker(object):
    
    # Constructor which defines default values for settings
    def __init__(self, mySMRC_Contr):
        
        self.contr= mySMRC_Contr
        self.allowedState={}            #States allowed for lokomotive in a region
        self.allowedStateTimeSpan={}    #How long is the state allowed?
        self.stateChangedAt={}          #When does the state has changed?
        self.violation={}               #Violations of rules found
        
        self.undefTimeSpan= 0
        self.noViolation= -1
        self.noViolationStr= "------------------------------------------------------------------------------------------"
        
        #Take aClassStateDict to create two dictionaries
        #with same structure
        aClassStateDict= self.contr.detRegions.classState
        #Initialize dictionaries for rule checkimg
        for region in aClassStateDict:
            self.allowedState[region]= {}
            self.allowedStateTimeSpan[region]= {}
            self.stateChangedAt[region]= {}
            self.violation[region]= {}
            for classname in aClassStateDict[region]:
                if classname[0]==':':  #states are only controlled for locomatives
                    #Initially all states are allowed
                    self.allowedState[region][classname] = set([ts.TrainState.absent,
                                                                ts.TrainState.stopped,
                                                                ts.TrainState.moving])
                    #Initially all states are allowed forever.
                    self.allowedStateTimeSpan[region][classname]= [self.undefTimeSpan,
                                                                   self.undefTimeSpan,
                                                                   self.undefTimeSpan]
                    #Time when the last state change happens.
                    self.stateChangedAt[region][classname]= 0 #0= undef.
                    
                    #Actual violations for region and classname
                    self.violation[region][classname]= self.noViolation
                    
        #Import the not allowed rules and update self.allowedState accordingly
        self.mailNotification= "off"
        self.import_NotAllowedRules()
        
        #Create a mail sender object if it should be used.
        if self.mailNotification == "on":
            self.mailSender= ms.MailSender()
        else:
            self.mailSender = None
        print()
    
    #Import the not allowed rules from json file and validate rules
    #for region, class and state. Then update allowed states accordingly.
    #Also read the timespan for each rule which allows the state of not allowed rules
    #for the time in sec specified.
    def import_NotAllowedRules(self):
        input_file= "notAllowedRules.json"
        print('\nImporting: ', input_file)
        stateSet= set(["absent", "stopped", "moving"])
        
        try:
            with open(input_file) as json_file:
                data = json.load(json_file)
        except:
            print('Error: Could not import', input_file)
            print('Continue with all states for all regions allowed.')
        else:
            self.mailNotification= data["mailNotification"]
            if self.mailNotification != "on":
                self.mailNotification= "off"
            for notAllowedRule in data['NotAllowedRules']:
                region= notAllowedRule['region']
                className= notAllowedRule['class']
                
                #check elements of the json-file for wrong region, class and state
                definitionError= True
                if region in self.allowedState:
                    if className in self.allowedState[region]:
                        for state in notAllowedRule['notAllowed']:
                            if state["state"] in stateSet:
                                timespan= self.castTimeSpan(state["allowedFor"], region, className)
                                if timespan == 0:
                                    #No timespan for state--> state is not allowed
                                    self.remove_rule(region, className, state["state"])
                                    print("Rule ok:", region, className, "not allowed:", state["state"])
                                else:
                                    #Timespan in sec for state --> state is allowed for timespan
                                    self.setTimeSpan(region,className, state["state"],timespan)
                                    self.remove_rule(region, className, state["state"])
                                    print("Rule ok:", region, className, state["state"], "allowed for sec:", timespan)
                                definitionError= False
                if definitionError:
                    print("ERROR: Rule(s) for:", region, className, "has wrong region, class or unknown state.")
                
    #Remove an allowed state from allowedStates       
    def remove_rule(self, region, className, state):
        
        stateCode= None
        if state == "absent":
            stateCode= ts.TrainState.absent
        elif state== "stopped":
            stateCode= ts.TrainState.stopped
        elif state== "moving":
            stateCode= ts.TrainState.moving
            
        try:
            self.allowedState[region][className].remove(stateCode)
            
        except KeyError:
            print("KeyError for:", region, className, state)
     
    #Set timespan as read from the json file
    def setTimeSpan(self, region, className, state, timespan):
        if state == "absent":
            self.allowedStateTimeSpan[region][className][0]= timespan
        elif state== "stopped":
            self.allowedStateTimeSpan[region][className][1]= timespan
        elif state== "moving":
            self.allowedStateTimeSpan[region][className][2]= timespan
    
    #Cast timespan string to int. If no int is specified report error and set it to 0.
    def castTimeSpan(self, timeSpanStr, region, className):
        ret= 0
        try:
            ret= int(timeSpanStr)
        except:
            print("(",region,className,")",timeSpanStr,":Wrong time span format in not allowed rule. Using 0 seconds.")
        return ret
        
        
    #CheckRules runs in a parallel process. It waits for state changes
    #sent from the parent process. If a rule is violated a string for
    #output in the parent process (in the view) is sent back. 
    def checkRules(self, child_conn):
        print('RuleChecker: checking rules')
        run= True
        while run:
            #Check for received item [regionName,classname, state]
            if child_conn.poll(): #True if item is present
                item= child_conn.recv() 
                print('RuleChecker:',item)
                region, classname, state= item
                #Violation check
                if state not in self.allowedState[region][classname]:
                    #New violation
                    print('Violation', region, classname, state)
                    self.violation[region][classname]= state
                    if self.allowedStateTimeSpan[region][classname][state.value-1] != self.undefTimeSpan:
                        self.stateChangedAt[region][classname]= time.time()
                    else:
                        #Only send violation if no time span allows violation for a timespan.
                        #Send violation info to parent process for display
                        self.sendViolations(region, child_conn)
                else:
                    #No violation
                    if self.violation[region][classname] != self.noViolation:
                        #Old violation can be deleted
                        self.violation[region][classname]= self.noViolation
                        self.stateChangedAt[region][classname]= 0
                        self.sendViolations(region, child_conn)
                
            else: #here handle timespans of violations.
                for region in self.violation:
                    for classname in self.violation[region]:
                        if self.violation[region][classname] != self.noViolation and \
                           self.stateChangedAt[region][classname] != 0:
                            deltaTime= time.time() - self.stateChangedAt[region][classname]
                            violation= self.violation[region][classname]
                            allowed= self.allowedStateTimeSpan[region][classname][violation.value-1]
                            if deltaTime >=  allowed:
                                #Set state changed at time to 0. This prevents
                                #sending the violation every loop. 
                                self.stateChangedAt[region][classname]= 0
                                self.sendViolations(region,child_conn)
                            elif deltaTime < 0.15:
                                #Prevent sending violations repeatedly for long allowed time spans
                                self.sendViolations(region,child_conn)
                
            time.sleep(0.06) #Wait for 60ms (15 checks per second are enough)
    
    #Report a rule violation to the parent process for a region 
    def sendViolations(self, region, child_conn):
        result={}
        result[region]= ''
        for className in self.violation[region]:    
            actViolation= self.violation[region][className]
            if actViolation != self.noViolation and \
               self.stateChangedAt[region][className]== 0: #no allowed timespan
                if actViolation == ts.TrainState.absent:
                    result[region]= result[region] + className + " abwesend "
                elif actViolation == ts.TrainState.stopped:
                    result[region]= result[region] + className + " hält "
                elif actViolation == ts.TrainState.moving:
                    result[region]= result[region] + className + " fährt "
        if result[region] == '':
            result[region]= self.noViolationStr
        elif self.mailSender != None:
            self.mailSender.sendMail(region + ":" + result[region])
        child_conn.send(result)
         
                 
              
          
    
                    
                    