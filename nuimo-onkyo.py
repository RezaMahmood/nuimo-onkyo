#!/usr/bin/env python

from nuimo import Nuimo
from bluepy.btle import UUID, DefaultDelegate, Peripheral, BTLEException
import sys
import os

import time
from onkyo import Onkyo

class NuimoOnkyoDelegate(DefaultDelegate):
    
    def __init__(self, nuimoOnkyo):
        DefaultDelegate.__init__(self)
        self.nuimo = nuimoOnkyo
        
    def handleNotification(self, cHandle, data):
        if int(cHandle) == self.nuimo.characteristicValueHandles['BATTERY']:
            print('BATTERY', ord(data[0]))
            #nuimoOnkyo.battery(ord(data[0]))
        elif int(cHandle) == self.nuimo.characteristicValueHandles['FLY']:
            print('FLY', ord(data[0]), ord(data[1]))
            #nuimoOnkyo.fly(ord(data[0]), ord(data[1]))
        elif int(cHandle) == self.nuimo.characteristicValueHandles['SWIPE']:
            self.nuimo.swipe(ord(data[0]))            
        elif int(cHandle) == self.nuimo.characteristicValueHandles['ROTATION']:
            value = ord(data[0]) + (ord(data[1]) << 8)
            if value >= 1 << 15:
                value = value - (1 << 16)
            self.nuimo.rotate(value)
        elif int(cHandle) == self.nuimo.characteristicValueHandles['BUTTON']:
            self.nuimo.button(ord(data[0]))

class NuimoOnkyo(Nuimo):
            
    def __init__(self, macAddress):
        Nuimo.__init__(self, macAddress)
        self.onkyo = Onkyo()
        
        print("Onkyo Host: %s" % self.onkyo.Host)
        print("Onkyo power state is %s" % self.onkyo.PowerState())
        print("Onkyo volume level is %s" % self.onkyo.VolumeLevel())
        
    
    def fly(self, flyValue):
        print(flyValue)
        
    def swipe(self, swipeValue):
        print(swipeValue)
        
    def rotate(self, rotateValue):
        print(int(rotateValue))
        self.onkyo.rotateVolume(rotateValue)
        
    def button(self, buttonValue):
        if buttonValue == 0:
            # check power state of Onkyo
            print("Button pressed. Onkyo PowerState is %s" % self.onkyo.PowerState())
            self.onkyo.TogglePower()

    def getNuimoBatteryLevel(self):
        return
        
if __name__ == "__main__":
    
    ######## Nuimo MAC Address #########
    nuimomac = "F6:B2:90:F2:DF:08"
    ####################################
    
    nuimoOnkyo = NuimoOnkyo(nuimomac)
    
    nuimoOnkyo.set_delegate(NuimoOnkyoDelegate(nuimoOnkyo))
    
    print("Trying to connect to %s.  Press Ctrl+C to cancel." % nuimomac)
    try:
        nuimoOnkyo.connect()
    except BTLEException as e:
        print("Bluetooth exception occurred:", str(e))
        sys.exit()
    print("Connected. Waiting for input events...")
    
    # Display some LEDs matrices and wait for notifications
    nuimoOnkyo.displayLedMatrix(
        "         " +
        " ***     " +
        " *  * *  " +
        " *  *    " +
        " ***  *  " +
        " *    *  " +
        " *    *  " +
        " *    *  " +
        "         ", 2.0)
    time.sleep(2)    

    try:
        while True:
            nuimoOnkyo.waitForNotifications()
    except BTLEException as e:
        print("Connection error:", str(e))
    except KeyboardInterrupt:
        print("Program aborted")