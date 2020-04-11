#!/usr/bin/env python3

import subprocess
import time


# File that contains all mp3 files on system
availableSongsFile = "/mp3Files/availableSongs.txt"
#availableSongsFile = "availableSongs.txt"

#File that contains current playing list
currentPlayingList = "/mp3Files/songlist.txt"
#currentPlayingList = "RunningSongs.txt"



# Command for tracking all mp3 files on system and storing them to output file -> availableSongsFile 
trackingSongsCMD = "find /media -type f -name '*.mp3' > " + availableSongsFile 
#trackingSongsCMD = "find media/ -type f -name '*.mp3' > " + availableSongsFile 


## -------------------------------------------------------------------------------- ##

# Running script forever until process is killed or system is shut down
while True:


    # Executing tracking files command 
    subprocess.check_output(trackingSongsCMD, shell=True)


    # List contains available songs in right format to be able to run by mp3 player
    # By Appending '\' before spaces in songs' names and deleting any empty lines
    availableSongs = []

    availableListWPTR = open(availableSongsFile,'r+')

    while True:

        line = availableListWPTR.readline()

        if not line:
            break

        rightFormatSongName = line.strip().replace(" ", "\ ")
        availableSongs.append(rightFormatSongName)

    availableListWPTR.close()

    # Opening current playing list file
    playingListPTR = open(currentPlayingList,'r')

    # Reading file and adding songs if any to current playing songs list
    currentSongs  = [song.strip() for song in playingListPTR.readlines()]

    # Getting the difference between all mp3 files on system and current playing list to be updated
    missingSongs = (list(set(availableSongs) - set(currentSongs))) 
    removedSongs = (list(set(currentSongs) - set(availableSongs)))

    # Closing files
    playingListPTR.close()

    # Updating current playing list 
    if not missingSongs:
        print("All is up to date")
    else:
        print("Update is required")

        # Opening current playing list file and appending missed songs to it
        playingListWPTR = open(currentPlayingList,'a')
        for song in missingSongs:
            playingListWPTR.write(song + '\n')
        playingListWPTR.close()


    # Deleting removed/deleted songs from current playing list

    removedSongs  = [song.strip() for song in removedSongs if len(song.strip())]
    if removedSongs:
        print("Songs removed")

        # String to concatenate all deleted lines' numbers
        deletedLinesNumbers = ''

        for song in removedSongs:

            if deletedLinesNumbers:
                deletedLinesNumbers = deletedLinesNumbers + ','

            # Grepping line number command
            lineNumberCMD = "cat " + currentPlayingList + " | grep -n '" + song + "'  | cut -f1 -d:"

            # Executing grepping line number command
            lineNumberOutput = subprocess.check_output(lineNumberCMD, shell=True)
            # Decoding the result of the command and getting line number to be deleted
            lineNumber = lineNumberOutput.decode().strip()
            
            # Appending line number to string containing all deleted lines' numbers
            deletedLinesNumbers = deletedLinesNumbers + lineNumber 

        # Appending 'd' to string to be ready for sed command
        deletedLinesNumbers = deletedLinesNumbers + "'d'"
        
        # Deleting specific lines command
        deletedLinesNumbersCMD = "sed -i " + deletedLinesNumbers + " " + currentPlayingList
        # Executing deleting specific lines command
        subprocess.check_output(deletedLinesNumbersCMD, shell=True)

    time.sleep(1)

