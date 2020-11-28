#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 16:18:41 2019

@author: angelo
"""
# create random ip address
import ipaddress
from socket import *

# Global ipaddresses
index = 1
net4 = ipaddress.IPv4Network('192.168.1.0/24')

# GLOBAL
serverPort = 12000
host = ''  # i think this needs to be localhost

# Dictionary of MAC addresses {  macAddress : clientAddress,   }
hold = {}

# creating socket for the Server
serverSocket = socket(AF_INET, SOCK_DGRAM)
# binds host address and port
serverSocket.bind((host, serverPort))


def ipInUse():
    return ("Client has an IP address in use")


def decline():
    return ("DECLINE")


# check mac address if it already has an IP addressed to it
def checkMac(dict, mac):
    if mac in dict:
        return (True)


# checks if the IP pool is full
def isIpPoolFull(i):
    if i == 254:
        return (True)


def checkIP(dict, value):
    if value not in dict.values():
        return True


def release(dict, mac):
    dict.pop(mac, None)


def renew(dict, mac):
    dict[mac] = str(net4[index])


def choice(input, hold, macAddress):
    if input == '1':
        print("Client", macAddress, "RELEASE")
        release(hold, macAddress)
        serverSocket.sendto("RELEASE".encode(), clientAddress)
    elif input == '2':
        print("Client", macAddress, "RENEW")
        if (checkMac(hold, macAddress)):
            print("Client has an IP")
            serverSocket.sendto("Already Have IP".encode(), clientAddress)
        else:
            renew(hold, macAddress)
            serverSocket.sendto("RENEW".encode(), clientAddress)
    elif input == '0':
        print("Client", macAddress, "QUIT")
        serverSocket.sendto("QUIT".encode(), clientAddress)


# how many client the server can listen too at the same time
print('\nThe server is ready to receive\n')

while 1:

    # getting DISCOVER message from client
    message, clientAddress = serverSocket.recvfrom(2048)
    # Getting the Discover messages sent from client and decodes it
    macAddress = message.decode().upper()

    # if IP is full declines
    if (isIpPoolFull(index)):
        serverSocket.sendto("DECLINE".encode(), clientAddress)
        print("All IP address is full")

    # checking the Discover message if client has an IP
    if (checkMac(hold, macAddress)):
        test = hold[macAddress]
        serverSocket.sendto(test.encode(), clientAddress)  # if client already has an IP
        serverSocket.sendto("DECLINE".encode(), clientAddress)
        print("DISCOVER message received ", '[', decline(), ']')
        print(ipInUse())
        continue
    else:
        serverSocket.sendto(str(net4[index]).encode(), clientAddress)
        # print("DISCOVER message received ", '[', macAddress, ']')
        # see if REQUEST was sent by client
        request, clientAddress = serverSocket.recvfrom(2048)
        request = request.decode()


    # REQUESTING
    #if request == "REQUEST":
     #   print("client REQUEST approved")
        # check if the IP is already in use
    if (checkIP(hold, str(net4[index]))):# if not in MacAddress gets an IP
        print("OFFERED", '[', str(net4[index]), ']')  # sends a offered IP to client
        hold[macAddress] = str(net4[index])
        # sending client the IP address it was offered
        print("REQUEST ACKNOWLEDGE sending \n[Client : IP address]")
        print('[', macAddress, ':', str(net4[index]), ']')
        serverSocket.sendto(str(net4[index]).encode(), clientAddress)
    print("\n\n\n")

        # if server is recieving a release, renew or quit command from client
    rrq, clientAddress = serverSocket.recvfrom(2048)
    rrq = rrq.decode()
    #print("test", rrq)
    choice(rrq, hold, macAddress)

