#!/usr/bin/python
######################################
##
## Sequencer project
##
## Auhor: Findlay Bewicke-Copley
## Date: 09-03-2024
##
######################################

######################################
## Load dependencies
######################################

from gpiozero import LED, Button
from signal import pause
import os
import time
import subprocess

######################################
## Define GPIO pins with dictionary
######################################

pinDict = {
    "RecordLED":"9",
    "RecordButton":"10",
    "PowerLED":"11",
    "PlayButton":"8"
    }

######################################
##
## Class to hold everything together
##
######################################

class Sequencer:

    def __init__(self, pindict):
        ## Set uo the LED GPIO pins based on the dictionary above
        self.LEDs = {"Record":LED(pinDict["RecordLED"]),
                      "Power":LED(pinDict["PowerLED"])}
        ## Set the button GPIO pins based on the dictionary above
        self.buttons = {"Record":Button(pinDict["RecordButton"]),
                         "Play":Button(pinDict["PlayButton"])}
        ## Play LED flashes to show script started uo correctly.
        self.startUp()
        ## setup values for processes
        self.setupProcess()
        ## set up button functions
        self.buttonsOn()

    def setupProcess(self):
        ## set recording attributes
        ## These let the record button be a latch or hold button
        self.recordStartTime = 0
        self.recPressCount = 0
        ## A process needs to exist to check if it has finished or not
        ## Here this just outputs the string "recordProcess created"
        self.recordProcess = subprocess.Popen(["echo", "recordProcess", "created"])
        ## This will hopefully stop the play button glitching
        self.playStartTime = 0
        self.playPressTime = 0
        ## Again this process needs to exist
        self.playProcess = subprocess.Popen(["echo", "playProcess", "created"])
        
    def allOff(self):
        ## Turn off all LEDs in dictionary
        for led in self.LEDs.values():
            led.off()

    def allOn(self):
        ## turn on all LEDs in dictionary
        for led in self.LEDs.values():
            led.on()

    def record(self):
        ## add 1 to the self.recPressCount
        self.recPressCount += 1
        ## if already recording do nothing
        if self.recordProcess.poll() is None:
            pass
        ## if playing the sample do nothing
        elif self.playProcess.poll() is None:
            pass
        ## Otherwise start recording
        else:
        elif self.playProcess.poll() is None:
        ## if not recording
        else:
            ## turn on record LED
            self.LEDs["Record"].on()
            ## set record start time 
            self.recordStartTime = time.time()
            ## start recording
            ## Using a process like this we can leave it running and still accept input
            ## We can also check whether this process is still running using the poll method (see above)
            self.recordProcess = subprocess.Popen(["arecord", "/home/findlay/Sample.wav" ,"-f", "dat"])
    
    def stopRecord(self):
        ## Avoid ghosting this requires a 0.1 second delay
        if self.returnTimeDifference(self.recordStartTime) < 0.1:
            pass
        ## if the recording has been running for more than one second or the button has been pressed more than once
        elif self.returnTimeDifference(self.recordStartTime) > 1 or self.recPressCount > 1:
            ## kill the process (ending the recording)
            self.recordProcess.kill()
            ## turn off the LED
            self.LEDs["Record"].off()
            ## reset the record press count to 0
            self.recPressCount = 0

    def play(self):
        ## If recording do nothing
        if self.recordProcess.poll() is None:
            pass
        ## If playing do nothing ## TODO change to kill process with some logic
        elif self.playProcess.poll() is None:
            ## self.playProcess.kill()
            pass
        ## Otherwise start a subprocess to play the sample
        else:
            self.playProcess = subprocess.Popen(["aplay", "/home/findlay/Sample.wav"])

    def buttonsOn(self):
        ## Setup the button functions
        self.buttons["Record"].when_pressed = self.record
        self.buttons["Record"].when_released = self.stopRecord
        self.buttons["Play"].when_pressed = self.play

    def returnTimeDifference(self, t):
        return time.time() - t

    def startUp(self):
        ## Turn the LEDs off
        self.allOff()
        ## Turn record LED on
        self.LEDs["Record"].on()
        time.sleep(0.5)
        ## turn stored file LED on
        self.LEDs["Power"].on()
        time.sleep(1)
        ## flash lights
        self.allOff()
        time.sleep(0.2)
        self.allOn()
        time.sleep(0.2)
        ## Off as default start point
        self.allOff()
        time.sleep(1)
        self.LEDs["Power"].on()

x = Sequencer(pinDict)

pause()
