#!/usr/bin/python
###########################################################################
##
## Sequencer project
##
## Auhor: Findlay Bewicke-Copley
## Date: 09-03-2024
##
###########################################################################

from gpiozero import LED, Button
from signal import pause
import os
import time
import subprocess

pinDict = {
    "RecordLED":"9",
    "RecordButton":"10",
    "PowerLED":"11",
    "PlayButton":"8"
    }


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
        self.recordStartTime = 0
        self.recPressCount = 0
        self.recordProcess = subprocess.Popen(["echo", "recordProcess", "created"])   
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
        self.recPressCount += 1
        ## if already recording do nothing
        if self.recordProcess.poll() is None:
            pass
        elif self.playProcess.poll() is None:
            pass
        ## if not recording
        else:
            print("recording")
            ## turn on record LED
            self.LEDs["Record"].on()
            ## set record start time 
            self.recordStartTime = time.time()
            ## start recording
            self.recordProcess = subprocess.Popen(["arecord", "/home/findlay/Sample.wav" ,"-f", "dat"])


    def stopRecord(self):
        if self.returnTimeDifference(self.recordStartTime) > 1 or self.recPressCount > 1:
            self.recordProcess.kill()
            self.LEDs["Record"].off()
            self.recPressCount = 0

    def play(self):
        if self.recordProcess.poll() is None:
            pass
        elif self.playProcess.poll() is None:
            ## self.playProcess.kill()
            pass
        else:
            self.playProcess = subprocess.Popen(["aplay", "/home/findlay/Sample.wav"])

    def buttonsOn(self):
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
