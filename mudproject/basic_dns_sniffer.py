#!usr/bin/python
""" DNSnif.py-It basically captures all the DNS Queries from the traffic and It can be used
    with an arp poisioning tool to capture the all the DNS Queries over the network

    Author:Aditya Agrawal
    Twitter: @exploitprotocol
    Author is not responsible for any effect's caused by this script
"""

from scapy.all import *
from scapy.layers.dns import DNSQR
from scapy.layers.dhcp import IP
import socket
import json
import requests

server_ip = '127.0.0.1'
mud_updater_ip = '10.0.0.3'

result = {}


def _get_hostname_ip(domain):
    return repr(socket.gethostbyname(domain))


def packet_handler(pkt):
    if pkt.haslayer(IP):
        ip_src = pkt[IP].src
        ip_dst = pkt[IP].dst
        print(f"src: {ip_src} -> dst: {ip_dst}")

    if pkt.haslayer(DNSQR):
        a = pkt[DNSQR]
        domain = str(a.qname)[2:-2]
        domain_ip = _get_hostname_ip(domain)[1:-1]
        print(f"domain: {domain}, ip: {domain_ip}")
        result[domain] = domain_ip

        url = f'http://{mud_updater_ip}:5000/update-dns'
        ip_domain_data = json.dumps({"ip": f"{domain_ip}", "domain": f"{domain}"})

        update_ip_domain = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=ip_domain_data
        )
        assert update_ip_domain.status_code == 200


packet_filter = " and ".join([
    "udp dst port 53",          # Filter UDP port 53
    "udp[10] & 0x80 = 0",       # DNS queries only
    ])

sniff(filter=packet_filter, prn=packet_handler)
print("RONF")