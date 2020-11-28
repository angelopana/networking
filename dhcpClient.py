#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 16:20:05 2019

@author: angelo
"""
from socket import *
import uuid
import re



def decline():
    return("DECLINE")


#changes this for me
serverName = '144.37.238.159'
serverPort = 12000

#macAddress formatted
macAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

clientSocket = socket(AF_INET, SOCK_DGRAM)


#Sending DISCOVER message a string of a MAC address
clientSocket.sendto(macAddress.encode(),(serverName, serverPort))
print("\nSending DISCOVER message to Sever", '[',macAddress.upper(),']')

serverOffer, serverAddress = clientSocket.recvfrom(2048)
serverOffer = serverOffer.decode()
#if serverOffer == decline():
#    print(decline())
#    exit(1)


print("Server OFFER",'[',serverOffer,']')
print("Client REQUEST sent")
clientSocket.sendto("REQUEST".encode(), (serverName, serverPort))

#reply for the MacAddress and its IP
serverIssuedIp, serverAddress = clientSocket.recvfrom(2048)

serverIssuedIp = serverIssuedIp.decode()


#if Returned from server is Decline Exit out
if serverIssuedIp == decline():
    print("DECLINE, goodbye!")
    #exit(1)


while 1:
    print("\n\nPRESS 1: RELEASE\nPRESS 2: RENEW\nPRESS 0: QUIT")
    userInput = input("What would you like to do: ")
    clientSocket.sendto(userInput.encode(), (serverName, serverPort))
    #get the server side information
    serverChoice, serverAddress = clientSocket.recvfrom(2048)
    serverChoice = serverChoice.decode()
    print("Server ACKNOWLEDGE ",serverChoice)
    # exits if user input choice was to quit
    if userInput == '0':
        exit(1)
    continue

clientSocket.close()


