import sys, getopt
import time
import datetime

from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botcandlestick import BotCandlestick

def main(argv):
    chart = BotChart("bittrex", "BTC-LTC", "fiveMin", False)

    log = BotLog()

    strategy = BotStrategy(capital=0.01, pair="BTC-LTC", client=chart.conn)

    # candlesticks = []
    # developing_candlestick = BotCandlestick()

    while True:
        try:
            price = chart.get_current_price()
        except Exception as e:
            log.log("ERROR: Exception occurred: " + e.message, "error")
            time.sleep(int(1))
            price = chart.get_current_price()

        log.log("Received price: " + str(price))

        strategy.live_tick(price)

        # if developing_candlestick.is_closed():
        #     candlesticks.append(developing_candlestick)
        #     strategy.tick(developing_candlestick)
        #     developing_candlestick = BotCandlestick()
        
        time.sleep(int(1))

if __name__ == "__main__":
    main(sys.argv[1:])