import os
import yaml
from yaml.loader import SafeLoader


def save_faucet_config(path, new_content):
    with open(path, 'w') as file:
        _ = yaml.dump(new_content, file)


def parse_base_file(base_file_path):
    with open(base_file_path) as f:
        return yaml.load(f, Loader=SafeLoader)


def add_new_ips(existing_rule, base_new_ips):
    for ip in base_new_ips:
        existing_rule.append({'rule': {
            'dl_type': 2048,
            'nw_dst': ip,
            'actions': {'allow': 1}
        }})

    return existing_rule
