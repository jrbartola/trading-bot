import sys, getopt
import time
import datetime

from chart import Chart
from strategy import BotStrategy
from logger import Logger
from candlestick import Candlestick

def main(argv):
    chart = Chart("bittrex", "BTC-LTC", "fiveMin", False)

    logger = Logger

    strategy = BotStrategy(capital=0.01, pair="BTC-LTC", client=chart.conn)

    # candlesticks = []
    # developing_candlestick = BotCandlestick()

    while True:
        try:
            price = chart.get_current_price()
        except Exception as e:
            logger.log("ERROR: Exception occurred: " + e.message, "error")
            time.sleep(int(1))
            price = chart.get_current_price()

        logger.log("Received price: " + str(price))

        strategy.live_tick(price)

        # if developing_candlestick.is_closed():
        #     candlesticks.append(developing_candlestick)
        #     strategy.tick(developing_candlestick)
        #     developing_candlestick = BotCandlestick()
        
        time.sleep(int(1))

if __name__ == "__main__":
    main(sys.argv[1:])