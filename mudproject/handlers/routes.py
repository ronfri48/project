from distutils.command.upload import upload
from flask import request
from mudproject.update_mud_configs import MUD
import time, traceback
import threading


# PROD config
#UPLOAD_FOLDER = "/var/www/uploads"

# dev config
UPLOAD_FOLDER = "/Users/eladbirnboim/uploads"

# const 
MUD_FILE = "mud_file"
ONE_HOUR = 1000 * 60 * 60


# global variables
mud = MUD(ONE_HOUR)

# jobs 
def every(delay, task):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task()
    except Exception:
      traceback.print_exc()
      # in production code you might want to have this instead of course:
      # logger.exception("Problem while executing repetitive task.")
    # skip tasks if we are behind schedule:
    next_time += (time.time() - next_time) // delay * delay + delay

# TODO remove comment
#threading.Thread(target=lambda: every(300, mud.handle_invalidate_request)).start()


def configure_routes(app):
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/update-mud', methods=['POST'])
    def update_mud():
        if request.method == 'POST' and MUD_FILE in request.files:
            mud_file = request.files[MUD_FILE]
            file_path = f"{UPLOAD_FOLDER}/{mud_file.filename}"
            file = mud_file
            file.save(file_path)
            mud.handle_update_mud_request(file_path)
            return 'Ok', 200
        
        return 'Bad Request', 400