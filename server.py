#!/usr/bin/env python

# ----- BEGIN INITIALIZATION -----
import os
import socket
import struct
import gdata.spreadsheet.service

import json
import time
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

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

# ----- GOOGLE SPREADSHEETS -----
json_key = json.load(open('iot-first-third-0180cc30f0c9.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gc = gspread.authorize(credentials)

# Open a worksheet from spreadsheet with one shot
wks = gc.open("Parking").sheet1
# -----

MAX_PARK = 2

free_spots = [True,True]
directions = {
                1: {"1": "left"},
                2: {"1": "right"}
}

sheet_cells = {
                1: "C3",
                2: "E3"
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
    wks.update_acell(sheet_cells[dev_id], is_on)
    if choose_parking() >= 0 :
        set_fields(choose_parking()+1)
    else:
        print "Wszystkie miejsca zajete"
