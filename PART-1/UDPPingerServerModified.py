# UDPPingerServer.py 
# We will need the following module to generate randomized lost packets 
import random 
from socket import * 
 
# Create a UDP socket  
# Notice the use of SOCK_DGRAM for UDP packets 
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1) 
# Assign IP address and port number to socket 
serverSocket.bind(('127.0.0.0', 12001)) 
print("Server is Listening")

while True: 
    # Generate a random number between 1 to 10 (both inclusive)  
    try:
        
        # Receive the client packet along with the address it is coming from

        message, address = serverSocket.recvfrom(1024)  
        # Capitalize the message from the client  
        message = message.upper() 
        # If rand is greater than 8, we consider the packet lost and do not respond to the client
        # print(rand)
        
        # Otherwise, the server response      
        serverSocket.sendto(message, address)

    except:
        #CLient must have closed abruptly
        serverSocket.close
        serverSocket = socket(AF_INET, SOCK_DGRAM) 
        # Assign IP address and port number to socket 
        serverSocket.bind(('127.0.0.0', 12001)) 
        print("Server is Listening")

    

