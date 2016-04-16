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

MAX_PARK = 3

free_spots = [True,True,True]
directions = {
                1: {"1": "right"},
                2: {"1": "mid", "2":"right"},
                3: {"1": "mid", "2":"left"}
}

def set_fields(destination):
    for id in directions.get(destination):
        command = id + "/" + directions.get(destination).get(id);
        #print "\n" + command + "\n"
        sock.sendto(command, (MCAST_GRP, MCAST_PORT+1))

def choose_parking():
    for i in range(MAX_PARK): 
        if free_spots[i]:
            return i
    return -1

while True:
    command = sock.recv(128)
    command = command.split('/')
    dev_id = int(command[0])
    is_on = command[1]

    if is_on == "1":
        print str(dev_id) + " zajete"
        free_spots[dev_id - 1] = False
    elif is_on == "0":
        print str(dev_id) + " wolne"
        free_spots[dev_id - 1] = True

    if choose_parking() >= 0 :
        set_fields(choose_parking()+1)
    else:
        print "Wszystkie miejsca zajete"