#!/usr/bin/env python

from core import eISCP, command_to_iscp, iscp_to_command
import commands

class Onkyo(object):
    
    
    def __init__(self):        
        receiver = self.discoverReceiver()
        self.Host = receiver.host
        self.DefaultMusicVolume = 20
        self.VolumeLevels = []
        self.volumeThread = None
        self.volumeDivider = 7
                    
    def TogglePower(self):
        currentPowerState = self.PowerState()
            
        if currentPowerState == 0:
            self.setPowerState(1)
        else:
            self.setPowerState(0)
        
    def PowerState(self):
        with eISCP(self.Host) as receiver:
            response = receiver.raw("PWRQSTN")
            if response == "PWR00":            
                return 0
            else:            
                return 1
        
    def setPowerState(self, state):
        with eISCP(self.Host) as receiver:
            print("Setting Onkyo Power State to %s" % state)
            receiver.raw("PWR0%s" % state)
            
            time.sleep(5) # Give the receiver some time to wake up
            if state == 1:
                # Only change default volume if the current setting is Spotify/Network
                selectedInput = receiver.raw("SLIQSTN")
                print("Current selected input is %s" % selectedInput)
                if selectedInput == "SLI2B":    
                    print("Setting default volume level")
                    if(self.VolumeLevel() > self.DefaultMusicVolume):
                        self.setVolumeLevel(self.DefaultMusicVolume) #On start set the volume level to default        
            
    def setVolumeLevel(self, volumeLevel):
        if self.PowerState() == 1:
            with eISCP(self.Host) as receiver:
                response = receiver.raw("MVL%s" % str(hex(volumeLevel))[2:])
                print("Response from setting volume level is: %s" % str(response))
                print(hex(volumeLevel))
                print("Volume level set to %s" % volumeLevel)
            
    def VolumeLevel(self):
        if self.PowerState() == 1:
            with eISCP(self.Host) as receiver:
                response = receiver.raw("MVLQSTN")
                decimalVolume = int(response[3:], 16)
                return decimalVolume
        else:
            return 0
        
    def rotateVolume(self, volumeLevel):
        isNegative = False
        if volumeLevel < 0:
            isNegative = True
            
        volume = abs(volumeLevel/self.volumeDivider)
        currentVolume = self.VolumeLevel()
        print("Current Volume is %s" % currentVolume)
        if isNegative:
            self.setVolumeLevel(currentVolume - volume)
        else:
            self.setVolumeLevel(currentVolume + volume)
    
    def discoverReceiver(self):
        receivers = eISCP.discover(timeout=1)
        receiver = receivers[0]
        return receiver  
        
 
                