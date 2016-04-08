#!/usr/bin/env python

# ----- BEGIN INITIALIZATION -----
import os
from serial import Serial
import socket
import struct

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SERIAL_PATH = os.path.join(BASE_DIR, 'dev', 'ttyS0')

serial = Serial(SERIAL_PATH, 38400)
# ----- END INITIALIZATION ----- 

# ----- SOCKETS -----
MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3456
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
# -----

free_spots = [True,True,True,True,True,True,True,True,True,True]
directions = {
                1: {"1": "right"},
                2: {"1": "mid", "2":"right"},
                3: {"1": "mid", "2": "mid", "3":"right"},
                4: {"1": "mid", "2": "left"},
                5: {"1": "mid", "2": "mid", "3":"left"},
                6: {"1": "left", "4": "mid", "5":"mid", "6":"right", "7":"right"},
                7: {"1": "left", "4": "mid", "5":"mid", "6":"right", "7":"mid", "8":"right"},
                8: {"1": "left", "4": "mid", "5":"mid", "6":"mid"},
                9: {"1": "left", "4": "mid", "5":"mid", "6":"right", "7":"left"},
               10: {"1": "left", "4": "mid", "5":"mid", "6":"right", "7":"mid", "8":"left"},
}

def set_fields(destination):
    for fields in directions[destination]:
        for field in fields:
            command = field + "/" + fields[field]
            sock.sendto(command, (MCAST_GRP, MCAST_PORT))

def choose_parking():
    for i in range(10): 
        if free_spots[i]:
            return i

while True:
    command = sock.recv(128)
    command = command.split('/')
    dev_id = int(command[0])
    is_on = command[1]
    
    if is_on == "1":
        free_spots[dev_id - 1] = True
    elif is_on == "0":
        free_spots[dev_id - 1] = False
    else:
        break

    set_fields(choose_parking())
    
