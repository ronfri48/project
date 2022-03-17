import os
import sys
import json
import requests



def post_initial_mud_file(mud_path):
    mud_updater_ip = '127.0.0.1'
    url = f'http://{mud_updater_ip}:5000/update-mud'

    file = {'mud_file': open(mud_path, "rb").read()}
    response = requests.post(
        url,
        files=file
    )

    assert response.status_code == 200


if __name__ == '__main__':
    post_initial_mud_file(sys.argv[1])