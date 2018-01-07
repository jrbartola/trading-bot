from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS, cross_origin
from bot.backtest import backtest

from datetime import datetime

app = Flask(__name__, static_folder='C:\\Users\\Jesse\\Documents\\Python\\TradingBot\\www\\static', template_folder='../www/static/templates')
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
    return render_template("index.html")

@app.route("/backtest")
def backtesting():
    import json

    coin_pair = request.args.get('pair')
    period_length = request.args.get('period')
    capital = float(request.args.get('capital'))
    stop_loss = float(request.args.get('stopLoss'))
    num_data = float(request.args.get('dataPoints'))

    result = backtest(coin_pair, period_length, capital, stop_loss, num_data)

    return json.dumps({'response': 200, 'result': result})


if __name__ == '__main__':
    app.run(debug=True)