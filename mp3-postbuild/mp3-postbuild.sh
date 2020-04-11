#!/bin/sh


echo 'PS1="MP3_Shell>"' >> ${TARGET_DIR}/etc/profile

output/host/bin/aarch64-linux-gcc myApplications/printHello.c -o ${TARGET_DIR}/myApplications/printHello.o

echo "/myApplications/printHello.o" >> ${TARGET_DIR}/etc/profile

