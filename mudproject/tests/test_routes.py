from flask import Flask
import os

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

def test_post_mud_file():