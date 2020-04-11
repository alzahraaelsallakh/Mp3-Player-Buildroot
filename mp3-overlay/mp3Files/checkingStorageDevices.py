#!/usr/bin/env python3

import subprocess
import re 
import time


memoryCardFlag = 0
usbFlashFlag = 0

existedMountDevices = []
existedDevices = []

memoryCardRegex = r'(mmcblk\d\w\d)'
usbFlashRegex = r'(sd\w\d)'


folderPreNaming = "mount_" 


def mountFunction(deviceName):

    folder = folderPreNaming + deviceName
    
    # Creating mount point for each device command
    creatingMountPointCMD = "mkdir /media/" + folder

    # Ececuting creating mount point command
    subprocess.check_output(creatingMountPointCMD, shell=True)

    # Mounting device on its mount point command
    mountingCMD = "mount /dev/"+deviceName + " /media/"+folder

    # Executing mounting device command
    subprocess.check_output(mountingCMD, shell=True)

    print("mounted")

def umountFunction(deviceName):

    deviceName = "/media/" + folderPreNaming + deviceName
    
    # Umounting mount point command
    umountCMD = "umount " + deviceName

    # Executing umounting device command
    subprocess.check_output(umountCMD, shell=True)

    # Deleting mount point command
    removeCMD = "rm -r " + deviceName
    # Executing mount point command
    subprocess.check_output(removeCMD, shell=True)

    print("Umounted")

def getConnectedDevices():
    global existedDevices

    # Listing devices connected to system and grepping memory cards command
    memoryCardCheckCMD = "fdisk -l | grep /mmcblk[0-9][a-z][0-9]"
    
    # Listing devices connected to system and grepping usb flash devices
    usbFlashCheckCMD = "fdisk -l | grep /sd[a-z][0-9]"

    try:
        # Executing listing memory card if existed command
        memoryCardOutput = subprocess.check_output(memoryCardCheckCMD, shell=True)
        memoryCardOutput = memoryCardOutput.decode().strip()
        memoryCardFlag = 1
    except:
        memoryCardFlag = 0

    try:
        # Executing listing usb flash if existed command
        usbFlashOutput = subprocess.check_output(usbFlashCheckCMD, shell=True)
        usbFlashOutput = usbFlashOutput.decode().strip()
        usbFlashFlag = 1
    except:
        usbFlashFlag = 0

    # Extracting memory cards devices' names from output by applying regular expressions
    if memoryCardFlag:
        existedMemoryCards = re.findall(memoryCardRegex,memoryCardOutput)
        for dev in existedMemoryCards:
            # Appending devices' name to existedDevices list
            existedDevices.append(dev)


    # Extracting usb flash devices' names from output by applying regular expressions
    if usbFlashFlag:
        existedUsbFlashes = re.findall(usbFlashRegex,usbFlashOutput)
        for dev in existedUsbFlashes:
            # Appending devices' name to existedDevices list
            existedDevices.append(dev)

def checkMountPoints():
    global existedMountDevices

    # Listing media directory content command
    existedMountPointsCMD = "ls /media/"

    # Executing listing media directory content command
    existedMountPointsOutput = subprocess.check_output(existedMountPointsCMD, shell=True)
    existedMountPointsOutput = existedMountPointsOutput.decode().strip() 


    if (len(existedMountPointsOutput)):
        # Existed mount devices
        existedMountDevices = existedMountPointsOutput.replace(folderPreNaming,"").strip()
        existedMountDevices = existedMountDevices.split('\n')
        
    else:
        existedMountDevices = []


def handleMounting():
    
    # Case1: no devices are connected but exist mount points -> umount and remove all points
    if (len(existedDevices) == 0 and len(existedMountDevices)!= 0):

        for dev in existedMountDevices:
            umountFunction(dev)

    # Case2: There're connected devices but no mount points -> mkdir and mount all
    elif (len(existedDevices) != 0 and len(existedMountDevices) == 0):
        for dev in existedDevices:
            mountFunction(dev)

    # Case3: There're connected devices and mount points -> compare, then mount or umount
    else:
        # Handling 3 impossible cases:
        # This state will be done when the lenght of both lists is zero

        while (len(existedDevices) != 0 and len (existedMountDevices) != 0):

            # 1- If device is connected and has mount point -> Check that is mounted, if not then mount -> remove device from both lists
            commonDevices = list(set(existedDevices).intersection(existedMountDevices))
            for dev in commonDevices:

                # Checking if device is already mounted
                alreadyMountedDeviceCMD = "mount | grep " + dev
                try:
                    # Executing checking already mounted devices command
                    alreadyMountedDeviceOutput = subprocess.check_output(alreadyMountedDeviceCMD, shell=True)
                    alreadyMountedDeviceOutput = alreadyMountedDeviceOutput.decode().strip()
                
                except:
                    
                    folder = folderPreNaming + dev

                    # Mounting device on its mount point command
                    mountingCMD = "mount /dev/"+dev + " /media/"+folder
                    # Executing mounting device command
                    subprocess.check_output(mountingCMD, shell=True)

                existedDevices.remove(dev)
                existedMountDevices.remove(dev)

            # 2- If device is connected and has no mount point -> mkdir then mount -> remove device from existedDevices
            while (len(existedDevices) != 0):
                for dev in existedDevices:
                    mountFunction(dev)
                    existedDevices.remove(dev)

            # 3- If device is not connected but has mount point -> umount then rm -> remove device from existedMountDevices
            while (len(existedMountDevices) != 0):
                for dev in existedMountDevices:
                    umountFunction(dev) 
                    existedMountDevices.remove(dev)

if __name__ == "__main__":
    while True:
        getConnectedDevices()
        checkMountPoints()
        handleMounting()
        time.sleep(1)