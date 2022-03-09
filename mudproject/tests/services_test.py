import mudproject.services.DnsRecordsManager as DnsRecordsManager
import pytest
import os

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before your test:
    DnsRecordsManager.clear()

    yield
    # Code that will run after your test:
    DnsRecordsManager.clear()

def test_dns_record_manager_failed_to_find_record():
    dns_record_manager = DnsRecordsManager.get()
    with pytest.raises(Exception, match="Could not find dns in cache"):
        dns_record_manager.get_ip("ynet.co.il", allow_dns_query=False)


def test_dns_record_manager_get_ip():
    dns_record_manager = DnsRecordsManager.get()
    dns = "ynet.co.il"
    ip = dns_record_manager.get_ip(dns)

    assert ip == "23.3.109.210"

    dummpy_ip = "1.2.3.4"
    dns_record_manager.update_dns_ip(dns, dummpy_ip)

    ip = dns_record_manager.get_ip(dns)
    assert ip == dummpy_ip