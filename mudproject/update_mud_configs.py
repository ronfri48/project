import abc
import socket
import subprocess
from datetime import datetime
from collections import namedtuple

from mud_parser.profile import Profile
import mudproject.services.DnsRecordsManager as DnsRecordsManager


IOT = namedtuple('IOT', ['hostname', 'ip', 'timestamp'])

  
class MUD:
  def __init__(self, validity_time):
    self._mud_pool = {}
    self._validity_time = validity_time
  
  @abc.abstractmethod
  def reload_muds():
    subprocess.call(['pkill', '-HUP', '-f', 'faucet.faucet'])
  
  def _add_to_mud_pool(self, iot_name, hostname, ip):
    if 'iot_name' not in self._mud_pool.keys():
      self._mud_pool['iot_name'] = []
    
    self._mud_pool['iot_name'].append(IOT(hostname, ip, int(datetime.now().timestamp())))
  
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
            new_ip = MUD._get_hostname_ip(entry.hostname)
            print(f'Updating dns record: {entry.hostname}: {entry.ip} -> {entry.hostname}: {new_ip} for iot {iot}')
            new_entries.append(IOT(entry.hostname, new_ip, int(datetime.now().timestamp())))
          else:
            print(f'Invalidating dns record: {entry.hostname}: {entry.ip} for iot {iot}')
          
          continue
        
        new_entries.append(entry)
      
      self._mud_pool[iot] = new_entries
   
  def _apply_mud(self, iot_name):
    # TODO: Move MUD files from places to switch path
    pass
  
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
    for mud in mud_profile.policies:
      self._add_to_mud_pool(iot_name, mud.hostname, mud.ip)
    
    self._apply_mud()
    MUD.reload_muds()

  def handle_update_dns_record(self, dns, new_ip):
    dns_record_manager = DnsRecordsManager.get()
    current_ip = dns_record_manager.get_ip(dns, allow_dns_query=False)
    if current_ip == new_ip:
      return
    
    dns_record_manager.update_dns_ip(dns, new_ip)
    # the ip was changed - need to iterate on the mud files and update the relavent rules
  
    number_of_changed_mud = 0
    for iot_name, entries in self._mud_pool.iter_items():
      new_entries = []
      is_changed = False
      for entry in entries:
        if entry.hostname == dns:
          is_changed = True
          new_entries.append(IOT(entry.hostname, new_ip, int(datetime.now().timestamp())))
        else:
          new_entries.append(entry)
      
      if is_changed:
        number_of_changed_mud += 1
        self._apply_mud(iot_name)
      
    if number_of_changed_mud > 0:
      MUD.reload_muds()

    
  def handle_invalidate_request(self):
    self._remove_invalid_entries()
    self._apply_mud_pool()
    MUD.reload_muds()
