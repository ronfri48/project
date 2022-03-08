import socket
import shelve
import logging

# PROD config
#CACHE_FILE_PATH = "/var/www/uploads/DnsRecordsManager.db"

# dev config
CACHE_FILE_PATH = "/Users/eladbirnboim/uploads/DnsRecordsManager.db"

class DnsRecordsManager:
    def __init__(self, db=None):
        file_path = db if db is not None else CACHE_FILE_PATH
        self._cache = shelve.open('CACHE_FILE_PATH', writeback=True)

    def update_dns_ip(self, dns_name, ip):
        logging.info(f"update_dns_ip: called with DNS name: '{dns_name}' and ip: {ip}")
        self._cache[dns_name] = ip

    def get_ip(self, dns_name, allow_dns_query=True):
        logging.info(f"get_ip: called with DNS name: '{dns_name}'")
        if dns_name not in self._cache:
            if not allow_dns_query:
                raise Exception("Could not find dns in cache")
            ip = socket.gethostbyname(dns_name)
            self.update_dns_ip(dns_name, ip)
        
        return self._cache[dns_name]