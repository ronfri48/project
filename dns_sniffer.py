#!usr/bin/python
""" DNSnif.py-It basically captures all the DNS Queries from the traffic and It can be used
    with an arp poisioning tool to capture the all the DNS Queries over the network

    Author:Aditya Agrawal
    Twitter: @exploitprotocol
    Author is not responsible for any effect's caused by this script
"""

from scapy.all import *
from scapy.layers.dns import DNSQR

serverip = '127.0.0.1'
result = {}


def packet_handler(pkt):
    if pkt.haslayer(DNSQR):
        if pkt[DNSQR].qname[0:-1] in result.keys():
            result[pkt[DNSQR].qname[0:-1]] = result[pkt[DNSQR].qname[0:-1]] + 1
        else:
            result[pkt[DNSQR].qname[0:-1]] = 1


def print_result():
    final = sorted(result, key=lambda x: result[x])
    print("No Of Times Visited" + "   " + "Domain Visited")
    for x in final:
        print(f"     {str(result[x])}                 {x}")


sniff(count=int(9), filter="udp port 53 and ip src " + str(serverip), prn=packet_handler)
print_result()