import socket
import shelve
import logging

# PROD config
CACHE_FILE_PATH = "/var/www/uploads/DnsRecordsManager.db"


__all__ = ["DnsRecordsManager", "create", "get"]


class DnsRecordsManager:
    def __init__(self):
        file_path = CACHE_FILE_PATH
        self._cache = shelve.open(file_path, writeback=True)

    def update_dns_ip(self, dns_name, ip):
        logging.info(f"update_dns_ip: called with DNS name: '{dns_name}' and ip: {ip}")
        self._cache[dns_name] = ip

    def get_ip(self, dns_name, allow_dns_query=True):
        logging.info(f"get_ip: called with DNS name: '{dns_name}'")
        if dns_name not in self._cache:
            if not allow_dns_query:
                return None
            ip = socket.gethostbyname(dns_name)
            self.update_dns_ip(dns_name, ip)
        
        return self._cache[dns_name]

    def _clear_cache(self):
        logging.info(f"clear_cache: Called")
        self._cache.clear()


dns_records_manager = None


def get():
    global dns_records_manager
    dns_records_manager = dns_records_manager if dns_records_manager else DnsRecordsManager()
    return dns_records_manager


def clear():
    global dns_records_manager
    if dns_records_manager:
        dns_records_manager._clear_cache()