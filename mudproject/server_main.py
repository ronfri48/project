from flask import Flask
from update_mud_configs import MUD
import time, traceback
import threading
from mudproject.handlers.routes import configure_routes

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

configure_routes(app)

if __name__ == '__main__':
    app.run()
