from poloniex import Poloniex
#from bittrex import Bittrex
import matplotlib.pyplot as plt
from bittrex_v2 import Bittrex, API_V2_0, API_V1_1
from time import time
import urllib, json
from botcandlestick import BotCandlestick
from botindicators import BotIndicators

# Create a mapping between string-based periods and their equivalent in seconds
period_map = {"oneMin": 60, "fiveMin": 300, "thirtyMin": 1800, "hour": 3600, "day": 86400, "week": 604800}

class BotChart(object):
    def __init__(self, exchange, pair, period, start_time=time() - 100000, end_time=time(), backtest=True):

        self.pair = pair
        self.period = period

        self.startTime = start_time
        self.endTime = end_time

        self.data = []

        with open("secrets.json") as secrets_file:
            secrets = json.load(secrets_file)
            secrets_file.close()

        if exchange == "poloniex":
            self.conn = Poloniex(secrets['poloniex_key'], secrets['poloniex_secret'])

            if backtest:
                rawdata = self.conn.api_query("get_chart_data", {"currencyPair" :self.pair, "start": self.startTime, "end": self.endTime, "period": self.period})
                for datum in rawdata:
                    if datum['open'] and datum['close'] and datum['high'] and datum['low']:
                        self.data.append(BotCandlestick(self.period, datum['open'], datum['close'], datum['high'], datum['low'], datum['weightedAverage']))

        if exchange == "bittrex":
            self.connv1 = Bittrex(secrets['bittrex_key'], secrets['bittrex_secret'], api_version=API_V1_1)
            self.conn = Bittrex(secrets['bittrex_key'], secrets['bittrex_secret'], api_version=API_V2_0)

            if backtest:
                rawdata = self.conn.get_candles(market=self.pair, tick_interval=self.period)['result'][:3000]
                plt.plot(list(map(lambda x: x['C'], rawdata)))
                # rawdata = self.conn.get_historical_data(market=self.pair, unit=period, n=5000)
                for i in range(len(rawdata)):
                    datum = rawdata[i]
                    stick = BotCandlestick(period_map[self.period], datum['O'], datum['C'], datum['H'], datum['L'], (datum['O'] + datum['C'])/2.)
                    stick.time = i
                    self.data.append(stick)

    def get_points(self):
        closings = list(map(lambda x: x.close, self.data))
        bbupper, bblower = BotIndicators.entire_bollinger_bands(closings)
        plt.plot(bbupper, 'g--')
        plt.plot(bblower, 'b--')
        #plt.plot(BotIndicators.entire_moving_average(closings, period=15), 'b--')
        #plt.plot(BotIndicators.entire_moving_average(closings, period=9), 'g--')

        return self.data

    def get_current_price(self):
        # If we are using bittrex, then self.connv1 will be defined (this check is pure stupidity
        # as Bittrex removed the get_ticker API route from V2.0 -___-
        if self.connv1:
            current_values = self.connv1.get_ticker(self.pair)
        else:
            current_values = self.conn.get_ticker(self.pair)
        last_pair_price = current_values['result']["Last"]
        return last_pair_price
