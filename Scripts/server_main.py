from flask import Flask
from update_mud_configs import MUD
import time, traceback
import threading

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

app = Flask(__name__)

ONE_HOUE = 1000 * 60 * 60

mud = MUD(ONE_HOUE)


threading.Thread(target=lambda: every(300, mud.handle_invalidate_request)).start()

@app.route('/update-mud', methods=['POST'])
def update_mud():
  file_path = f"/var/www/uploads/{file.filename}"
  if request.method == 'POST':
    file = request.files['mud_file']
    file.save(file_path)
    mud.handle_update_mud_request(file_path)
