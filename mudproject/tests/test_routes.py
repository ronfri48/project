from flask import Flask
import os
import json

from mudproject.handlers.routes import configure_routes


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.get_data() == b'Hello, World!'
    assert response.status_code == 200


def test_post_mud_file():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/update-mud'

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    mud_file = os.path.join(__location__, 'huebulbmud.json')  # os.path.join(sys.path[0], "huebulbmud.json")
    mud_data = open(mud_file, "rb")
    data = {"mud_file": (mud_data, "huebulbmud.json")}

    response = client.post(
        url,
        data=data,
        buffered=True,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200


def test_post_update_dns_record():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()

    mud_url = '/update-mud'
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    mud_file = os.path.join(__location__, 'huebulbmud.json')  # os.path.join(sys.path[0], "huebulbmud.json")
    mud_data = open(mud_file, "rb")
    data = {"mud_file": (mud_data, "huebulbmud.json")}

    response = client.post(
        mud_url,
        data=data,
        buffered=True,
        content_type="multipart/form-data",
    )
    url = '/update-dns'
    ip_domain_data = json.dumps({"ip": '1.2.3.4', "domain": "https://huebulb.com/huebulb"})
    update_ip_domain = client.post(
        url,
        headers={'Content-Type': 'application/json'},
        data=ip_domain_data
    )
    assert response.status_code == 200
    assert update_ip_domain.status_code == 200
