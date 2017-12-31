from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin

from datetime import datetime

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Add a rotating file handler to keep track of error logging
if app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('errors.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

@app.route("/")
def index():
    return "Entry point.."


if __name__ == '__main__':
    app.run(debug=True)