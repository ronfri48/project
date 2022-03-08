from mudproject.services.DnsRecordsManager import DnsRecordsManager
import pytest

def test_dns_record_manager_failed_to_find_record():
    dns_record_manager = DnsRecordsManager()
    with pytest.raises(Exception, match="Could not find dns in cache"):
        dns_record_manager.get_ip("google.com", allow_dns_query=False)


def test_dns_record_manager_get_ip():
    dns_record_manager = DnsRecordsManager()
    dns = "google.com"
    ip = dns_record_manager.get_ip(dns)

    assert ip == "11.11.11.11"

    dummpy_ip = "1.2.3.4"
    dns_record_manager.update_dns_ip(dns, dummpy_ip)

    ip = dns_record_manager.get_ip(dns)
    assert ip == dummpy_ip