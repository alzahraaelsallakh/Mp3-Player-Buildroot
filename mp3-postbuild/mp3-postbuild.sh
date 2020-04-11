#!/bin/sh


echo 'PS1="MP3_Shell>"' >> ${TARGET_DIR}/etc/profile

output/host/bin/aarch64-linux-gcc myApplications/printHello.c -o ${TARGET_DIR}/myApplications/printHello.o

echo "/myApplications/printHello.o" >> ${TARGET_DIR}/etc/profile

echo "cd /mp3Files" >> ${TARGET_DIR}/etc/profile

echo "./mp3commandline" >> ${TARGET_DIR}/etc/profile

########################Audio Output Settings##########################################

#sudo cp $(dirname $0)/mp3-player/S50-Bluetooth-Daemon-service ${TARGET_DIR}/etc/init.d/
#sudo chmod 777 ${TARGET_DIR}/etc/init.d/S50-Bluetooth-Daemon-service

#sudo cp $(dirname $0)/mp3-player/Bluetooth_init ${TARGET_DIR}/root/mp3-player/
#sudo cp $(dirname $0)/mp3-player/audio_ouput ${TARGET_DIR}/root/mp3-player/

#sudo chmod -R 777 ${TARGET_DIR}/root
