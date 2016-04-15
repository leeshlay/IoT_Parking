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

MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3456

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
#sock.bind((MCAST_GRP,MCAST_PORT))

# ----- END INITIALIZATION ----- 

myId = 1;
ser.write(chr(31))

while True:
  command = sock.recv(10240)
  print "Field1 " + command
  info = command.split('/')
  print info
  if info[0] == myId:
    if info[1] == 'left':
      ser.write(chr(0))
    elif info[1] == 'mid':
      ser.write(chr(15))
    elif info[1] == 'right':
     ser.write(chr(31))
