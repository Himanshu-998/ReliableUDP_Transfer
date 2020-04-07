import socket
import sys
from time import sleep
import pickle
import hashlib
#Fixed Headersize
HEADERSIZE = 32
PACKET_SIZE = 512

try:
    req = sys.argv[1]
except:
    print("Fewer arguments passed to the program, Please enter the filename!")
    req = input("Filename > ")

client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def decode_packet(packet):
    #picle.loads return the reconstituted object hierarchy of the pickled representation bytes_object of an object.
    return pickle.loads(packet)


#try:

while True:

    client_socket.sendto(req.ljust(HEADERSIZE).encode('utf-8'),("127.0.0.1", 12345))
    print("sent a req to server")
    #wait for 5 milliseconds
    sleep(0.05)

    #Check for a reply on the Port
    message, server_addr = client_socket.recvfrom(PACKET_SIZE)
    print("RR")
    message = decode_packet(message)
    if message[1] == "OK":
        if message[0] == hashlib.sha256(message[1].encode('utf-8')).hexdigest():
            print("OK!")
            break

client_socket.sendto(f"{req}".encode('utf-8'),("127.0.0.1", 1234))

#except Exception as e:
 #   print(str(e))

client_socket.close()