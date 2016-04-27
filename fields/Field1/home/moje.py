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
import struct

MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3457

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


# ----- END INITIALIZATION ----- 

myId = 1;
ser.write(chr(0))

while True:
  command = sock.recv(128)
  info = command.split('/')
  if info[0] == str(myId):
    if info[1] == "left":
      ser.write(chr(0))
    elif info[1] == "mid":
      ser.write(chr(18))
    elif info[1] == "right":
      ser.write(chr(31))
