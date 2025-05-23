
# My Pingers

We are making this project about TCP,UDP,ICMP pingers in which client pings the server and server send the response to client and at client side we are are displaying the Min.RTT, Max.RTT, Avg.RTT and also displaying the packet loss percentage. 


##  Team Members:

SAKSHI BADOLE---CS24MTECH11008

ABDULLA OVAIS---CS24METCH12014

SIMEON SAHASRAMSA GAJULA---SM24MTECH11002
##


# Part-1 UDP

First we run the UDP server for which the command is

sudo python3 UDPPingerServer.py
#
Now We run the UDPPingerClient

sudo python3 UDPPingerClient.py
#
For Modified server

first we run the command through which loss 20% of packet without random function:

sudo tc qdisc add dev <interface name> root netem loss 20%

after this command we run this:

sudo python3 UDPPingerServerModified.py

Now run the udp client   

sudo python3 UDPPingerClient.py

Now delete the changes command for this is   

sudo tc qdisc del dev <interface name> root


#
For UDP icmp error message first run server the command is:

sudo python3 UDPICMPPingerServer.py

For client the command is:

sudo python3 UDPICMPPingerClient.py


#
# Part-2 TCP
First we run the TCP server for which the command is

sudo python3 TCPPingerServer.python3

Now we run the client 

sudo python3 TCPPingerClient.py
#
For TCP Modified server in which we use multi threading and display the request from diffrent client on the server side

sudo python3 TCPPingerModifiedServer.py

Now run the multiplie TCP client

sudo python3 TCPPingerClient.py
#
For TCP icmp error message first run the server

sudo python3 TCPICMPPingerServer.py

now run the client 

sudo python3 TCPICMPPingerClient.py
#

# Part-3 ICMP

Run the ICMP pinger

sudo python3 ICMPPinger.py
#
Now Configure iptables rules and command iptables

sudo iptables -A INPUT -s <source_ip_address> -p icmp -j REJECT
--reject-with <error_response>

after running this we have To clear all iptables rules and command for this

sudo iptables -F
#


