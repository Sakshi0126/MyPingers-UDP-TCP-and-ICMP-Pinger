# UDPPingerServer.py 
# We will need the following module to generate randomized lost packets 
import socket
import struct
import random



def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]

        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer

# Create a UDP socket  
# Notice the use of SOCK_DGRAM for UDP packets 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
# Assign IP address and port number to socket 
serverSocket.bind(('127.0.0.0', 12000)) 


icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

print("Server is Listening")

while True: 
    # Generate a random number between 1 to 10 (both inclusive)  
    try:
        rand = random.randint(1, 10)     
        # Receive the client packet along with the address it is coming from

        message, address = serverSocket.recvfrom(1024)  
        # Capitalize the message from the client  
        message = message.upper() 
        # If rand is greater than 8, we consider the packet lost and do not respond to the client
        # print(rand)
        if rand > 8:
            icmp_type = 3  # Destination unreachable
            icmp_code = 0  # Network unreachable
            icmp_checksum = 0
            icmp_id = 0
            icmp_seq = 0

            icmp_packet = struct.pack('bbHHh', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
            icmp_checksum = checksum(icmp_packet)
            icmp_packet = struct.pack('bbHHh', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)

            icmpSocket.sendto(icmp_packet, address)
            continue
        # Otherwise, the server response      
        serverSocket.sendto(message, address)

    except:
        #CLient must have closed abruptly
        serverSocket.close
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Assign IP address and port number to socket 
        serverSocket.bind(('127.0.0.0', 12000)) 
        print("Server is Listening")
 


