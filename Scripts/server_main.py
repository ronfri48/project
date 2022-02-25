from flask import Flask
from update_mud_configs import MUD

app = Flask(__name__)

ONE_MIN = 1000 * 60

mud = MUD(ONE_MIN)

@app.route('/update-mud', methods=['POST'])
def update_mud():
  file_path = f"/var/www/uploads/{file.filename}"
  if request.method == 'POST':
    file = request.files['mud_file']
    file.save(file_path)
    mud.handle_update_mud_request(file_path)
