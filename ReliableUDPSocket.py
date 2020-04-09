import socket
import os
import hashlib
import pickle
from time import sleep

class ReliableUDPSocket:

    UDP_IP = None
    UDP_PORT = None
    UDP_ADDR = None
    upd_socket = None
    sequenceNumber = None

    # AF_INET is an address family that is used to designate type of addresses that socket can communicate (IPv4 in this case)
    # SOCK_DGRAM is a datagram based protocol (UDP)
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sequenceNumber = 1

    # Bind, so that server informs the OS that it will be using the given IP and PORT
    def bind_socket(self,ip,port):
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.UDP_ADDR = (ip,port)
        self.udp_socket.bind(self.UDP_ADDR)
    
    # Increment the sequence number by 1
    def incrementseqN(self):
        self.sequenceNumber += 1 

    # Update thw sequence number by desired value
    def setseqN(self,number):
        self.sequenceNumber = number

    # Flip the sequence number, used to implement Stop and wait protocol
    def flipseqN(self):
        self.sequenceNumber ^= 1

    # We will use sha256 for encrypting the message, incase message gets tampered or corrupted
    # Each checksum is of 113 bytes
    def makePacket(self,message):
        # Unicode-objects must be encoded before hashing
        checksum = hashlib.sha256(message.encode('utf-8')).hexdigest()
        packet =  pickle.dumps([checksum,message,self.sequenceNumber])
        return packet

    def unloadPacket(self,packet):
        return pickle.loads(packet)


    # If data is not tamperd and has expected seqnumber return 1.
    # if data is tampered return 0
    # else return -1
    def check_packet(self,packet):
        # if hashed data matches with given checksum we know it is valid
        if packet[0] == hashlib.sha256(packet[1].encode('utf-8')).hexdigest():
            if self.sequenceNumber == packet[2]:
                return 1
            else:
                return -1
        else:
            0


    

