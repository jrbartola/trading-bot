import sys, getopt
import time

from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botcandlestick import BotCandlestick

def main(argv):
    chart = BotChart("bittrex", "BTC-LTC", 300, False)

    strategy = BotStrategy()

    candlesticks = []
    developingCandlestick = BotCandlestick()

    while True:
        try:
            developingCandlestick.tick(chart.get_current_price())
        except Exception as e:
            time.sleep(int(30))
            developingCandlestick.tick(chart.get_current_price())

        if developingCandlestick.is_closed():
            candlesticks.append(developingCandlestick)
            strategy.tick(developingCandlestick)
            developingCandlestick = BotCandlestick()
        
        time.sleep(int(30))

if __name__ == "__main__":
    main(sys.argv[1:])