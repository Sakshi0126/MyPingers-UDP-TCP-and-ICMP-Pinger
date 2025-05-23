# 1. Currently, the icmp client pinger program calculates RTT for each packet and prints it out
# individually. Modify this to correspond to the way the standard ping program works. You will
# need to report the minimum, maximum, and average RTTs at the end of all pings from the
# client. In addition, calculate the packet loss rate (in percentage) like in PART-1 and PART-2.

# 2. Your program can only detect timeouts in receiving ICMP echo responses. Modify the Pinger
# program to parse the ICMP response error codes and display the corresponding error results to
# the user. Examples of ICMP response error codes are 0: Destination Network Unreachable, 1:
# Destination Host Unreachable. Note that these modifications can be added to PART-1 and
# PART-2 of the assignment even though you used UDP/TCP sockets for sending pings.

from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
delay_list = []


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


def receiveOnePing(mySocket, ID, timeout, destAddr):

    timeLeft = timeout
    

    while 1:

        startedSelect = time.time()
        #select(inputs, outputs, excepts, timeout=none)
        whatReady = select.select([mySocket], [], [], timeLeft)
        # print(whatReady[0],whatReady[1],whatReady[2])

        howLongInSelect = (time.time() - startedSelect)

        if whatReady[0] == []: # Timeout
            return "Request timed out."
        

        # timeSent = startedSelect + howLongInSelect
        
        # print(startedSelect)
        # print(howLongInSelect)

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        print("Received packet from:", addr,"\n")

        #The ICMP header starts after bit 160 or 20B of the IP header (unless IP options are used).
        ttl = recPacket[9:9]
        recHeader = recPacket[20:28]
        recData = recPacket[28:]
        # print(recPacket,"\n")
        # print(recHeader,"\n")
        recHeader = struct.unpack("bbHHh",recHeader)
        

        if recHeader[0] == 0 and recHeader[1] == 0 and recHeader[3] == ID:
            delay = (timeReceived - startedSelect) * 1000  # Convert to milliseconds
            # print(recData[0].len()+ "bytes from {} : icmp_seq={} ttl={} time={} ms".format(addr, recHeader[4], ttl, "{:.2f}".format(delay)))
            return delay
        elif recHeader[0] == 3:
            if recHeader[1] == 0:
                print("Destination Network Unreachable")
                return None
            elif recHeader[1] == 1:
                print("Destination Host Unreachable")
                return None
            
        else:
            return "Request timed out."
        # print(recHeader,"\n")
        # print("Type:", recHeader[0])
        # print("Code:", recHeader[1])
        # print("Checksum:", recHeader[2])
        # print("ID:", recHeader[3])
        # print("Sequence:", recHeader[4])
        # Fill in start
        # delay_list = delay_list.extend(timeReceived - timeSent)
        # delay = (timeReceived - timeSent)*1000
        # delay_list = delay_list.append(delay)
        # print("Delay : ",delay)
        # Fetch the ICMP header from the IP packet


        # Fill in end
        timeLeft = timeLeft - howLongInSelect

        if timeLeft <= 0:
            return "Request timed out.\n"
        
    

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    # b-signed char, B - unsigned char, H -unsigned short, ,h-short
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)
    
    # Get the right checksum, and put it in the header
    if sys.platform == 'darwin':
    # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum) # 2byte flip htons

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects which can be referenced
    # by their
    # position number within the object.


def doOnePing(destAddr, timeout):

    icmp = getprotobyname("icmp")
  
    # SOCK_RAW is a powerful socket type. For more details:
    # http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    
    
    myID = os.getpid() & 0xFFFF # Return the current process ID
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay


def ping(host, timeout=1, n=10):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    global delay_list
    packet_loss = 0
    packets = n
    i=0
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")

    # Send ping requests to a server separated by approximately one second
    while n!=0:
                
        try:
            delay = doOnePing(dest, timeout)
            delay_list.append(delay)

        except AttributeError:
              
            packet_loss = packet_loss + 1

        except TypeError:
            pass

            
        time.sleep(1) # one second
        n = n-1

    packet_loss_perc = (packet_loss/packets)*100
    
    if delay_list and delay_list[i in range(packets)] != None:

        print("\n--- {} ({}) ping statistics ---\n".format(host,dest))
        print("{} packets transmitted, {} packets received, {}% packet loss".format(packets,(packets-packet_loss), packet_loss_perc))
        print("rtt  min/avg/max  = {}/{}/{} ms".format("{:.2f}".format(min(delay_list)), "{:.2f}".format((sum(delay_list)/len(delay_list))), "{:.2f}".format(max(delay_list))))
        

    else:
        print( packets,"packets lost ")
    



pings = int(input("Enter number of pings: "))
print(pings)
ping('192.168.137.194',n=pings)

