import ReliableUDPSocket

PACKETSIZE = 2048


#Send ACKs to server to transfer is complete.
#multiple packets so if any packet losses, it will stop after 10 packets.
def finisdownload(client_socket, server_addr):

    for i in range(1,10):
        pack = client_socket.makePacket("ACK")
        client_socket.udp_socket.sendto(pack,server_addr)
    
    print("Download Finished.\n Closing connection with server.")


def download(client_socket,server_addr,file,target_file):
    
    # set the sequence number to 1 for 1st packet
    client_socket.setseqN(1)

    #Number of times the client will send a request for file to server is set to 9 
    request = 1
    while request < 10:
        packet = client_socket.makePacket(file)
        client_socket.udp_socket.sendto(packet,server_addr)
        try:
            message, serveraddr = client_socket.udp_socket.recvfrom(PACKETSIZE)
        except:
            continue
        if not message:
            request += 1
        else:
            #Discard this packet, Since we know server got our request and will send again the 1st packet
            print("Request Accepted!")
            break
    
    if request == 10:
        print("Unable to connect to the server! Please try again later...")

    else:
        recv_file = open(target_file,"w")
        while True:
            try:
                message, serveraddr = client_socket.udp_socket.recvfrom(PACKETSIZE)
            except:
                continue
            message = client_socket.unloadPacket(message)
            if client_socket.check_packet(message) == 1:
                print(message[1])
                if message[1] == "$$$":
                    print("File Received, Check current working directory.")
                    finisdownload(client_socket,server_addr)
                    break
                recv_file.write(message[1])
                reply_packet = client_socket.makePacket("ACK")
                client_socket.udp_socket.sendto(reply_packet,serveraddr)

                # Flip the sequence number to avoid saving same packet twice
                client_socket.flipseqN()
    return

if __name__ == "__main__":

    client_socket = ReliableUDPSocket.ReliableUDPSocket()
    client_socket.bind_socket("127.0.0.1",12346)
    file = input("Filename > ")
    target_file = input("Save as > ")
    server_addr = ("127.0.0.1",12345)
    download(client_socket,server_addr,file,target_file)
