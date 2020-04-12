#!/usr/bin/env python3

import subprocess
import time
import re


scanningCMD = "hcitool scan"

deviceRegex = r'(\d\d:\S*)\s*(.*)'

macAddress = []
deviceName = []

scanningOutput = subprocess.check_output(scanningCMD, shell=True)
scanningOutput = scanningOutput.decode().strip()

scanningMatch = re.findall(deviceRegex,scanningOutput)
for match in scanningMatch:
    if match:
        macAddress.append(match[0])
        deviceName.append(match[1])

if len(deviceName):
    print("Available devices to connect:")
    
    for dev in deviceName:
        print(dev)
    
    connectedDevice = input("Enter device name (Make sure of small/captial cases): ")
    
    if connectedDevice in deviceName:
        connectedDeviceIndex = deviceName.index(connectedDevice)
        connectedDeviceAddress = macAddress[connectedDeviceIndex]

        # Checking if it's connected before
        bluExistedDevicesCMD = "find /var/lib -type d -name " + connectedDeviceAddress
        existedDev = subprocess.check_output(bluExistedDevicesCMD, shell=True)
        existedDev = existedDev.decode().strip()

        if connectedDeviceAddress not in existedDev:

            connectingCMD = "bt-device -c " + connectedDeviceAddress
            subprocess.call(connectingCMD, shell=True)

        else:
            print ("Already connected")
    else:
        print ("Device not found")
