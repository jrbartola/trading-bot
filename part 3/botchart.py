from poloniex import Poloniex
from bittrex import Bittrex
from time import time
import urllib, json
from botcandlestick import BotCandlestick

# Create a mapping between string-based periods and their equivalent in seconds
period_map = {"oneMin": 60, "fiveMin": 300, "thirtyMin": 1800, "hour": 3600, "day": 86400, "week": 604800}

class BotChart(object):
    def __init__(self, exchange, pair, period, startTime=time()-100000, endTime=time(), backtest=True):

        self.pair = pair
        self.period = period

        self.startTime = startTime
        self.endTime = endTime

        self.data = []

        if exchange == "poloniex":
            self.conn = Poloniex('key goes here', 'Secret goes here')
            if backtest:
                poloData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
                for datum in poloData:
                    if (datum['open'] and datum['close'] and datum['high'] and datum['low']):
                        self.data.append(BotCandlestick(self.period,datum['open'],datum['close'],datum['high'],datum['low'],datum['weightedAverage']))

        if exchange == "bittrex":
            # Creating an instance of the Bittrex class with our secrets.json file
            with open("secrets.json") as secrets_file:
                secrets = json.load(secrets_file)
                secrets_file.close()
                self.conn = Bittrex(secrets['bittrex_key'], secrets['bittrex_secret'])

            if backtest:
                rawdata = self.conn.get_historical_data(market=self.pair, unit=period, n=1000)
                for datum in rawdata:
                    stick = BotCandlestick(period_map[self.period], datum['O'], datum['C'], datum['H'], datum['L'], (datum['O'] + datum['C'])/2.)
                    self.data.append(stick)


    def get_points(self):
        return self.data

    def get_current_price(self):
        current_values = self.conn.api_query("returnTicker")
        last_pair_price = current_values[self.pair]["last"]
        return last_pair_price
