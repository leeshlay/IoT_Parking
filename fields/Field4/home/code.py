#!/usr/bin/env python

# ----- BEGIN INITIALIZATION -----
import os
from serial import Serial
import socket
import struct

MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3456

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SERIAL_PATH = os.path.join(BASE_DIR, 'dev', 'ttyS0')

ser = Serial(SERIAL_PATH, 38400)
# ----- END INITIALIZATION ----- 

myId = 4;
ser.write(str(15))

while True:
  command = sock.recv(10240)
  print command
  info = command.split('/')
  print info
  if info[0] == myId:
  	if info[1] == 'left':
  		ser.write(str(0))
  	elif info[1] == 'mid':
  		ser.write(str(15))
  	elif info[1] == 'right':
  		ser.write(str(31))
