#!/usr/bin/env python

# ----- BEGIN INITIALIZATION -----
import os
import socket
import struct

# ----- END INITIALIZATION ----- 

# ----- SOCKETS -----
MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3456
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
# -----

free_spots = [True,True,True]
directions = {
                1: {"1": "left", "2":"left"},
                2: {"1": "right", "2":"left"},
                3: {"1": "left", "2":"mid"}
}

def set_fields(destination):
    for id in directions.get(destination):
        command = id + "/" + directions.get(destination).get(id);
        print command
        sock.sendto(command, (MCAST_GRP, MCAST_PORT+1))

def choose_parking():
    for i in range(3): 
        if free_spots[i]:
            return i

while True:
    command = sock.recv(128)
    command = command.split('/')
    dev_id = int(command[0])
    is_on = command[1]
    
    if is_on == "1":
        print str(dev_id) + " zajete"
        free_spots[dev_id - 1] = True
    elif is_on == "0":
        print str(dev_id) + " wolne"
        free_spots[dev_id - 1] = False

    set_fields(choose_parking()+1)
    
