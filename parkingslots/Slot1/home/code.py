#!/usr/bin/env python

# ----- BEGIN INITIALIZATION -----
import os
from serial import Serial

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SERIAL_PATH = os.path.join(BASE_DIR, 'dev', 'ttyS0')

ser = Serial(SERIAL_PATH, 38400)
# ----- END INITIALIZATION ----- 


import socket
import time
import thread

MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3456

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)    

flag = 0

ser.write(chr(128+1))		#motion

SLOT_ID = 1

status = 0
ser.write(chr(64+8+4))		# green

def timer():
	global flag

	while True:
		if flag == 0:
			flag = 1
		else:
			flag = 0
			time.sleep(3)


def change_lamp(status):
	if status == 0:
		status = 1
		ser.write(chr(64+32+16))	# red
	else:
		status = 0
		ser.write(chr(64+8+4))		# green
		#time.sleep(5)

	return status


#thread.start_new_thread( timer, () )

while True:

	cc = ser.read(1)
	if len(cc)>0 :

		if cc == chr(128+64+1):

			status = change_lamp(status)

			print status

			message = str(SLOT_ID) + "/" + str(status)

			print 'SENT: ' + message
			
			sock.sendto(message, (MCAST_GRP, MCAST_PORT))
