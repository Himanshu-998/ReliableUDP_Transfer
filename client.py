import ReliableUDPSocket
import time

# Packet size is a constant to read from the PACKETSIZE bytes from the socket
PACKETSIZE = 2048


# # Send ACKs to server to inform transfer is complete.
# # multiple packets so if any packet losses, it will stop after 10 packets.
# # Here we are not taking care if this ACK is lost.
# Client will close the connection after receiving the file.

def finisdownload(client_socket, server_addr):

    for i in range(1,10):
        pack = client_socket.makePacket("ACK".encode("utf-8"))
        client_socket.udp_socket.sendto(pack,server_addr)


def download(client_socket,server_addr,file,target_file):
    
    # Set the sequence number to 1 for 1st packet
    client_socket.setseqN(1)

    # Number of times the client will send a request for file to server is set to 9 
    # Socket timeout is set to 10 millisecond by default, So after every 10 milliseconds, The socket will
    # throw an error and it is handled, and request will be sent again 
    request = 1
    while request < 10:
        # file is type string ("filename") so we need to encode it before creating packet
        # For more information look ReliableUDPSocket class
        packet = client_socket.makePacket(file.encode("utf-8"))
        client_socket.udp_socket.sendto(packet,server_addr)
        try:
            message, serveraddr = client_socket.udp_socket.recvfrom(PACKETSIZE)
        except:
            # socket timeout raises socket.timeout as error when there is nothing to receive on the socket after socket.gettimeout() time has elapsed.
            # Here it is set to 10 milli seconds
            # we dont need to handle anything here so pass  
            pass
        if not message:
            request += 1
        else:
            #Discard this packet, Since we know server got our request and will send again the 1st packet
            print("Request Accepted!")
            break
    
    if request == 10:
        print("Unable to connect to the server! Please try again later...")

    else:
        # beginning of transfer of file is stored in tic
        tic = time.time()
        print("Download Started!")
        toc = None
        # recv_file is the target file object
        recv_file = open(target_file,"wb")
        # Until we dont receive the final packet with "$$$" as data we continue listening on the socket
        while True:
            try:
                message, serveraddr = client_socket.udp_socket.recvfrom(PACKETSIZE)
            except:
                #if there is socket timeout go back to listening on the socket
                continue
            message = client_socket.unloadPacket(message)
            if client_socket.check_packet(message) == 1:
                # if message is "$$$"  we have received the file and can close the connection with the server
                if message[1] == "$$$".encode("utf-8"):
                    print("File Received, Check current working directory!")
                    finisdownload(client_socket,server_addr)
                    # record the finish time
                    toc = time.time()
                    # calculate and print the time taken to download the file.
                    print(f"Time taken for transfer: {int(toc - tic)}s.")
                    break
                # Write the received data from the packet into the file
                recv_file.write(message[1])
                # Create a packet with an Acknowledgement
                reply_packet = client_socket.makePacket("ACK".encode("utf-8"))
                # send packet to the server
                client_socket.udp_socket.sendto(reply_packet,serveraddr)
                # Flip the sequence number to avoid saving same packet twice
                client_socket.flipseqN()
    return

if __name__ == "__main__":

    # Create a client side socket.
    client_socket = ReliableUDPSocket.ReliableUDPSocket()
    # We bind the socket to a fixed address. 
    client_socket.bind_socket("127.0.0.1",12346)

    file = input("Filename > ")
    target_file = input("Save as > ")
    server_addr = ("127.0.0.1",12345)
    download(client_socket,server_addr,file,target_file)
