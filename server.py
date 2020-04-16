import ReliableUDPSocket
import sys
from time import sleep

PACKETSIZE = 2048

def read_chunk(file, chunk_size = 512):
   # Lazy function to read a file piece by piece 
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data

def sendfile(server_socket,filename,client_addr):
    pkn = 1
    # set the sequence number to 1 for 1st packet
    server_socket.setseqN(1)

    with open(filename,"rb") as file:
        for data in read_chunk(file):
            print(f"packet: {pkn}")
            print(data)
            pkt = server_socket.makePacket(data)
            while True:
                server_socket.udp_socket.sendto(pkt,client_addr)
                try:
                    message, clientaddr = server_socket.udp_socket.recvfrom(PACKETSIZE)
                except:
                    continue
                message = server_socket.unloadPacket(message)
                if server_socket.check_packet(message) == 1 and client_addr == clientaddr:
                    if message[1] == "ACK".encode("utf-8"):
                        break
            # Increment sequence number after every succesfull transfer
            #server_socket.incrementseqN()
            server_socket.flipseqN()
            pkn += 1
    
    # Finsing transfer
    pkt = server_socket.makePacket("$$$".encode("utf-8"))
    #send 10 times if there is a packet loss
    for i in range(1,10):
        server_socket.udp_socket.sendto(pkt,client_addr)
        try:
            message, clientaddr = server_socket.udp_socket.recvfrom(PACKETSIZE)
        except:
            continue
        message = server_socket.unloadPacket(message)
        validity = server_socket.check_packet(message)
        # validity == -1 beacuse we dont about sequence number
        if validity == 1 or validity == -1 and client_addr == clientaddr:
            if message[1] == "ACK".encode("utf-8"):
                break
    print("File Transfer finished!")

# The server keeps listening on the port for any incoming request
def listen(server_socket):
    while True:
        try:
            file_req, client_addr = server_socket.udp_socket.recvfrom(PACKETSIZE)
        except:
            continue
        file_req = server_socket.unloadPacket(file_req)
        if server_socket.check_packet(file_req) == 1:
            sendfile(server_socket,file_req[1],client_addr)
            break

if __name__ == "__main__":
    server_socket = ReliableUDPSocket.ReliableUDPSocket()
    server_socket.bind_socket("127.0.0.1",12345)
    while True:
        listen(server_socket)
