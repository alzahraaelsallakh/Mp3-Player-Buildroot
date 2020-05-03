#!/bin/sh


# Setting shell prompt to "MP3_Shell" 
echo 'PS1="MP3_Shell>"' >> ${TARGET_DIR}/etc/profile

# Compiling "welcome to application" program
output/host/bin/aarch64-linux-gcc myApplications/printHello.c -o ${TARGET_DIR}/myApplications/printHello.o

# Running "welcome to application" program at initial time
echo "/myApplications/printHello.o" >> ${TARGET_DIR}/etc/profile

# Setting working directory to "mp3Files" at initial time
echo "cd /mp3Files" >> ${TARGET_DIR}/etc/profile

# Running keyboard commands script
echo "./mp3commandline" >> ${TARGET_DIR}/etc/profile

# Bluetooth setup
echo 'root=/dev/mmcblk0p2 rootwait console=tty1 console=ttyS0,115200' > output/images/rpi-firmware/cmdline.txt
