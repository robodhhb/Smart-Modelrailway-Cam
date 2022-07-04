#!/usr/bin/python3
###############################################################
# MailSender sends mails to an e-mail box of an SMTP server
# like for example t-online.de. It sends the mail from one e-mail
# adress to another adress. It is used as notifier.
# You must config 5 values: See below

# File: MailSender.py
# Author: Detlef Heinze 
# Version: 1.1    Date: 29.06.2022 
###########################################################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailSender(object):
    
    # Constructor which initializes the object
    def __init__(self):
        
        #e-mail-config: Here config 5 values.
        #senderAdress and reicerAdress must be different !
        self.senderAdress= "yourSenderEmailAdress"
        self.pwd= "passordOfSender"
        self.smtpHost= 'yourSMTPHost'
        self.port= 0  #Port of your SMTP Host
        
        self.receiverAdress="ReceiverEmailAdress"
        self.eMailSubject="SMRC Regelverletzung"
        
        # SMTP-object initialisation
        try:
            self.smtp = smtplib.SMTP(host=self.smtpHost, port=self.port)
            self.smtp.starttls()
            self.smtp.login(self.senderAdress, self.pwd)
            print("E-mail on rule violation to:", self.receiverAdress)
        except Exception as e:
            print('\nSMTP error: Cannot login to', self.senderAdress, "with port", self.port)
            print('See init function of MalSender.py.')
            print(e)
    
    #Send aText to the eMailAdress
    def sendMail(self, aText):
        msg = MIMEMultipart() 
        msg['From']=self.senderAdress
        msg['To']=self.receiverAdress
        msg['Subject']=self.eMailSubject

        msg.attach(MIMEText(aText, 'plain'))

        try:
            self.smtp.send_message(msg)
            print("   E-mail notification sent to:", self.receiverAdress)
        except Exception as e:
            print("\nCould not send e-mail notifiction")
            print(e)
        
        
if __name__ == "__main__":
    mailSender= MailSender()
    mailSender.sendMail("Gleis 3: Dampflok hält")
    
    
        