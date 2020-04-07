import socket
import os
import hashlib
import pickle
from time import sleep
# 127.0.0.1 resolves to localhost or the same machine
IP = "127.0.0.1"
PORT = 12345
HEADERSIZE = 32
PACKET_SIZE = 512

# AF_INET is an address family that is used to designate type of addresses that socket can communicate (IPv4 in this case)
# SOCK_DGRAM is a datagram based protocol (UDP)
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Bind, so that server informs the OS that it will be using the given IP and PORT
server_socket.bind((IP, PORT))

#Default parameter as Temp in case of any error in passing filename
def validRequest(filename = "Temp"):
    try:
        if os.path.isfile(filename):
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False

#This method will send and wait for an ACK by the client

def get_packet(messgae,seqence_number):
    #Generating Checksum for error detection
    checksum = hashlib.sha256(messgae.encode('utf-8')).hexdigest()
    #pickle.dumps return the pickled representation of the object obj as a bytes object, instead of writing it to a file.
    return pickle.dumps([checksum,messgae,seqence_number])


def send_file_to(client_address):
    #First step is to send an ACK that we got the request
    message = "OK"
    packet = get_packet(message,0)
    while True:
        server_socket.sendto(packet,client_address)
        #Sleep for 5 milliseconds
        print("Messge sent to client!")
        sleep(0.05)
        reply, client_addr = server_socket.recvfrom(PACKET_SIZE)
        # Recieved a reply from the same client
        # There may be multiple request by this time on the socket
        if client_addr == client_address:
            if reply.decode('utf-8') == "OK":
                print("OK!")
                break
        


# Listen indefinitely if there comes any request for a file
while True:

    try:
        #The client will first send the file name.
        #client_request will hold the file name.
        #client_address will hold a tuple of client IP and PORT.

        client_request, client_address = server_socket.recvfrom(HEADERSIZE)

        print(f"Received request from {client_address}")
        #Check is the file is present will the system
        # if the file is found by the server then send an ACK if not send a NAK.
        if client_request:
            filename = client_request.decode('utf-8')
            print(f"Requested file: {filename}")

        # TODO: for now i have removed checking if file is present because of some error, I will later update this
        if validRequest(filename) or True:
            # an ACK with seqence number 0, and Ok messgae
            send_file_to(client_address)
    


    except Exception as e:
        print(str(e))

