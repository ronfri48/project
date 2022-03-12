import os
import abc
import asyncio
import socket
import subprocess
from datetime import datetime
from collections import namedtuple

from mudproject.mud_parser.profile import Profile
import mudproject.services.dns_records_manager as DnsRecordsManager

from mudproject.faucet_config.faucet_editor import parse_base_file, add_new_ips, save_faucet_config

IOT = namedtuple('IOT', ['fqdn', 'ip', 'timestamp'])

# TODO: Fix to real path
ACLS_PATH = os.path.join(os.path.dirname(__file__), r'faucet_config\config')

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')


def reload_muds():
    asyncio.run(run('pkill -HUP -f faucet.faucet'))
    # Means: subprocess.call(['pkill', '-HUP', '-f', 'faucet.faucet'])


class MUD:
    def __init__(self, validity_time):
        self._mud_pool = {}
        self._validity_time = validity_time

    def _clear_from_mud_pool(self, iot_name):
        self._mud_pool.pop(iot_name, None)

    def _add_to_mud_pool(self, iot_name, fqdn, ip):
        if iot_name not in self._mud_pool.keys():
            self._mud_pool[iot_name] = []

        self._mud_pool[iot_name].append(IOT(fqdn, ip, int(datetime.now().timestamp())))

    @abc.abstractmethod
    def _get_hostname_ip(dns):
        return repr(socket.gethostbyname(dns))

    def _remove_invalid_entries(self, should_update_ip=True):
        current_timestamp = int(datetime.now().timestamp())
        for iot, entries in self._mud_pool.iter_items():
            new_entries = []
            for entry in entries:
                if self._validity_time < current_timestamp - entry.timestamp:
                    if should_update_ip:
                        new_ip = MUD._get_hostname_ip(entry.fqdn)
                        print(f'Updating dns record: {entry.fqdn}: {entry.ip} -> {entry.fqdn}: {new_ip} for iot {iot}')
                        new_entries.append(IOT(entry.fqdn, new_ip, int(datetime.now().timestamp())))
                    else:
                        print(f'Invalidating dns record: {entry.fqdn}: {entry.ip} for iot {iot}')

                    continue

                new_entries.append(entry)

            self._mud_pool[iot] = new_entries

    def _apply_mud(self, iot_name):
        config_path = os.path.join(ACLS_PATH, f'{iot_name}_acl.yml')
        faucet_config = parse_base_file(config_path)
        rule_name = list(faucet_config['acls'].keys())[0]
        faucet_config['acls'][rule_name] = add_new_ips(faucet_config['acls'][rule_name],
                                                     [iot.ip for iot in self._mud_pool[iot_name]])

        save_faucet_config(config_path, faucet_config)

    def _apply_mud_pool(self):
        for iot_name in self._mud_pool.keys():
            self._apply_mud(iot_name)

    def _parse_mud_file(self, mud_file_content):
        return Profile(mud_file_content)

    def handle_update_mud_request(self, mud_file_path):
        with open(mud_file_path, 'rb') as mud_file:
            try:
                content = mud_file.read()
                mud_profile = self._parse_mud_file(content)
            except Exception as e:
                print(e)
                raise e

        iot_name = mud_profile.system_info
        # Reset current rules
        self._clear_from_mud_pool(iot_name)

        # Add rules from mud file to mud_pool
        dns_record_manager = DnsRecordsManager.get()
        for policy_key, policy_acls in mud_profile.policies.items():
            for name, acl in policy_acls.items():
                if policy_key == 'from-device-policy':
                    for key, entry in acl.entries.items():
                        for k, match in entry.matches.items():
                            if k == 'ipv4' and hasattr(match, 'mud_dst_dnsname') and len(match.mud_dst_dnsname):
                                try:
                                    fqdn = match.mud_dst_dnsname
                                    ip = dns_record_manager.get_ip(fqdn)
                                    self._add_to_mud_pool(iot_name, fqdn, ip)
                                except Exception as e:
                                    print(e)

        self._apply_mud(iot_name)
        reload_muds()

    def handle_update_dns_record(self, fqdn, new_ip):
        dns_record_manager = DnsRecordsManager.get()
        current_ip = dns_record_manager.get_ip(fqdn, allow_dns_query=False)
        if current_ip == new_ip:
            return

        dns_record_manager.update_dns_ip(fqdn, new_ip)
        # the ip was changed - need to iterate on the mud files and update the relevant rules

        number_of_changed_mud = 0
        for iot_name, entries in self._mud_pool.items():
            new_entries = []
            is_changed = False
            for entry in entries:
                if entry.fqdn == fqdn:
                    is_changed = True
                    new_entries.append(IOT(entry.fqdn, new_ip, int(datetime.now().timestamp())))
                else:
                    new_entries.append(entry)

            if is_changed:
                number_of_changed_mud += 1
                self._apply_mud(iot_name)

        if number_of_changed_mud > 0:
            reload_muds()

    def handle_invalidate_request(self):
        self._remove_invalid_entries()
        self._apply_mud_pool()
        reload_muds()
