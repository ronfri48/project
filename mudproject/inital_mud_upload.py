import os
import json
import requests



def post_initial_mud_file():
    mud_updater_ip = '127.0.0.1'
    url = f'http://{mud_updater_ip}:5000/update-mud'

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    mud_file = os.path.join(__location__, 'huebulbmud.json')  # os.path.join(sys.path[0], "huebulbmud.json")
    file = {'mud_file': open(mud_file, "rb")}
    mud_data = open(mud_file, "rb")
    data = {"mud_file": (mud_data, "huebulbmud.json")}
    print(mud_data)
    response = requests.post(
        url,
        data=data,
        headers={'Content-Type': 'application/json','buffered': 'True', },
        files=file
    )

    assert response.status_code == 200


def post_update_dns_record():

    mud_url = '/update-mud'
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    mud_file = os.path.join(__location__, 'huebulbmud.json')  # os.path.join(sys.path[0], "huebulbmud.json")
    mud_data = open(mud_file, "rb")
    data = {"mud_file": (mud_data, "huebulbmud.json")}

    response = requests.post(
        mud_url,
        data=data,
        buffered=True,
        content_type="multipart/form-data",
    )
    url = '/update-dns'
    ip_domain_data = json.dumps({"ip": '1.2.3.4', "domain": "https://huebulb.com/huebulb"})
    update_ip_domain = requests.post(
        url,
        headers={'Content-Type': 'application/json'},
        data=ip_domain_data
    )
    assert response.status_code == 200
    assert update_ip_domain.status_code == 200

post_initial_mud_file()