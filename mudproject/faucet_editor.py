import os
import yaml
from yaml.loader import SafeLoader


def parse_base_file(base_file_path):
    with open(base_file_path) as f:
        return yaml.load(f, Loader=SafeLoader)


def add_new_ips(existing_rule, base_new_ips):
    for ip in base_new_ips:
        existing_rule.append({'rule': {
            'dl_type': 2048,
            'new_dst': ip,
            'actions': {'allow': 1}
        }})

    return existing_rule


data = parse_base_file(os.path.join(os.path.dirname(__file__), 'acl1.yml'))
data['acls'][list(data['acls'].keys())[0]] = add_new_ips(data['acls'][list(data['acls'].keys())[0]], ['9.9.9.9', '77.7.7.77'])

print(data)