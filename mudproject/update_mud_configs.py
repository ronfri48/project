import abc
import socket
import subprocess
from datetime import datetime
from collections import namedtuple

from mud_parser.profile import Profile


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
   
  def _apply_mud_pool(self):
    # TODO: Move MUD files from places to switch path
    pass
  
  def _parse_mud_file(self, mud_file_content):
    return Profile(mud_file_content).policies
  
  def handle_update_mud_request(self, mud_file_path):
    with open(mud_file_path, 'rb') as mud_file:
      try:
        content = mud_file.read()
        mud_file_content = self._parse_mud_file(content)
      except Exception as e:
        print(e)
        raise e
      
    for mud in mud_file_content:
      self._add_to_mud_pool(mud.io_name, mud.hostname, mud.ip)
    
    self._apply_mud_pool()
    MUD.reload_muds()
    
  def handle_invalidate_request(self):
    self._remove_invalid_entries()
    self._apply_mud_pool()
    MUD.reload_muds()
