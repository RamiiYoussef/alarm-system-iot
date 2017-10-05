#!/usr/bin/python3.5
# Created By Rami Mo7ep

# For use with normally closed (NC) Reed Switch connected to ground & GPIO input
# If using normally open (NO), simply reverse the booleans.

import time
import smtplib
import _thread
from core.banners import random_banner as banner
from core.color import *
from core.Phishing import *
from core import color,updater,config,raiDB,SMSInteractive
import argparse ,os ,textwrap ,sys ,subprocess, shutil ,random

try:
    need_clean = False

    # Setting up connection to SMTP Server for sending email/sms.
    print('[*] Setting up SMS...')

    # Function to call on new thread
    # Because of race conditions, this needs to be done quickly or on diff thread
    def send_msg(opened):
        # SMS Interactive
        SMSInteractive.interactive(opened)

    time.sleep(1)

    # Setting up connection to SMTP Server for sending email/sms.
    print('[*] Setting up Database...')

    def inset_database(opened, doorType):
        # database Interactive
        raiDB.interactive(opened, doorType)

    time.sleep(1)
    # Initializing GPIO
    print('[*] Setting up hardware...')

    # next_state to check for to send message
    next_stateMain = True
    next_stateGlass = False
    
    need_clean = True

    time.sleep(1)
    # Running actual program
    print('[*] Ready!')
    # Run infinitely
    while True:
        # Check for next state For Main Door
        if next_stateMain == True:
            # Insert data to database
            _thread.start_new_thread(inset_database, (next_stateMain, 'main',))
            # Send message on different thread
            _thread.start_new_thread(send_msg, (next_stateMain,))
            # Negate next_state
            next_stateMain = not next_stateMain

        # Check for next state For Glass Door
        if next_stateGlass == True:
            # Inser data to database
            _thread.start_new_thread(inset_database, (next_stateGlass, 'glass',))
            # Negate next_state
            next_stateGlass = not next_stateGlass
            
        time.sleep(0.3)
        
except KeyboardInterrupt:
    # For Keyboard Interrupt exit
    need_clean = False

if need_clean:
    # For normal exit
    print('Clean ..')


