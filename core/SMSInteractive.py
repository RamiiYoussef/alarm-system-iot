#!/usr/bin/env python3
#Created By Rami Mohep

import time
import _thread
from core import config
import smtplib
    
def interactive(input):

    #Setup Server Connection
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login( config.FROM, config.PASS )

    #Message Template
    #Leading '\n' is required for sending an email with ':' (SMS/MMS Gateway)
    MSG  = '\nDoor was '
    DOOR_MSG = {True:'opened', False:'closed'}
    
    #Compile message string to print and send.
    #Ex: '\nDoor was closed at 5:50:20 PM'
    #This way is used because it is quickest and we have race conditions!
    str_print =''.join([MSG, DOOR_MSG[input], ' at ',
                        time.strftime('%I:%M:%S %p')])
    
    print(str_print)
    server.sendmail(config.FROM, config.TO, str_print)
    server.quit()
