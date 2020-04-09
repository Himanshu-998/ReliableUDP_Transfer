# ReliableUDP_Transfer
Computer networks assignment to add reliability features over UDP protocol 


The server is going in infinte wait after sending the 1st packet, Since client is not replying.

This is happening because we have to use timeout instead of sleep method

These are few links which I found to be useful.

https://www.programcreek.com/python/example/3209/socket.recvfrom

https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method

The typical approach is to use select() to wait until data is available or until the timeout occurs. Only call recv() when data is actually available.


### Example code to use select method
```
read_sockets, write_socket, exception_sockets = select.select(sockets_list, [], sockets_list)
```

```
 Calls Unix select() system call or Windows select() WinSock call with three parameters:
       - rlist - sockets to be monitored for incoming data
       - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
       - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
     Returns lists:
       - reading - sockets we received some data on (that way we don't have to check sockets manually)
       - writing - sockets ready for data to be send thru them
       - errors  - sockets with some exceptions
     This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
 ```
