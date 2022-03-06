from flask import request

def configure_routes(app):
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/update-mud', methods=['POST'])
    def update_mud():
        file_path = f"/var/www/uploads/{request.files['mud_file'].filename}"
        if request.method == 'POST':
            file = request.files['mud_file']
            file.save(file_path)
            mud.handle_update_mud_request(file_path)
            return 'Ok', 200
        
        return 'Bad Request', 400