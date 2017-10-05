#!/usr/bin/env python3
# Created By Rami Mohep

# For use with normally closed (NC) Reed Switch connected to ground & GPIO input
# If using normally open (NO), simply reverse the booleans.

import RPi.GPIO as GPIO
import time
import smtplib
import _thread
import config
import databaseInteractive
import SMSInteractive
from py import SMSInteractive

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
        databaseInteractive.interactive(opened, doorType)

    time.sleep(1)
    # Initializing GPIO
    print('[*] Setting up hardware...')

    PINMain = 12
    PINGlass = 11
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PINMain, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PINGlass, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # next_state to check for to send message
    next_stateMain = True
    next_stateGlass = True
    
    need_clean = True

    time.sleep(1)
    # Running actual program
    print('[*] Ready!')
    # Run infinitely
    while True:
        # Check for next state For Main Door
        if GPIO.input(PINMain) == next_stateMain:
            # Insert data to database
            _thread.start_new_thread(inset_database, (next_stateMain, 'main',))
            # Send message on different thread
            _thread.start_new_thread(send_msg, (next_stateMain,))
            # Negate next_state
            next_stateMain = not next_stateMain

        # Check for next state For Glass Door
        if GPIO.input(PINGlass) == next_stateGlass:
            # Inser data to database
            _thread.start_new_thread(inset_database, (next_stateGlass, 'glass',))
            # Negate next_state
            next_stateGlass = not next_stateGlass
            
        time.sleep(0.3)
        
except KeyboardInterrupt:
    # For Keyboard Interrupt exit
    GPIO.cleanup()
    need_clean = False

if need_clean:
    # For normal exit
    GPIO.cleanup()

print('\nEnd!')

if __name__ == '__main__':
    main()
