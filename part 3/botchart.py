from poloniex import poloniex
import urllib, json
import pprint
from botcandlestick import BotCandlestick

period_map = {"fiveMin": 300, "thirtyMin": 1800, "hour": 3600, "day": 86400, "week": 604800}

class BotChart(object):
    def __init__(self, exchange, pair, period, startTime=None, endTime=None, backtest=True):
        from time import time

        self.pair = pair
        self.period = period

        self.startTime = int(time() - 500000) if not startTime else startTime
        self.endTime = self.startTime + 500000 if not endTime else endTime

        self.data = []
        
        if exchange == "poloniex":
            self.conn = poloniex('key goes here','Secret goes here')

            if backtest:
                poloData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
                for datum in poloData:
                    if (datum['open'] and datum['close'] and datum['high'] and datum['low']):
                        self.data.append(BotCandlestick(self.period,datum['open'],datum['close'],datum['high'],datum['low'],datum['weightedAverage']))

        if exchange == "bittrex":
            if backtest:
                url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName="+self.pair+"&tickInterval="+self.period+"&_="+str(self.startTime)
                response = urllib.urlopen(url)
                rawdata = json.loads(response.read())['result']
                for datum in rawdata:
                    stick = BotCandlestick(period_map[self.period], datum['O'], datum['C'], datum['H'], datum['L'], (datum['O'] + datum['C'])/2.)
                    self.data.append(stick)


    def getPoints(self):
        return self.data

    def getCurrentPrice(self):
        currentValues = self.conn.api_query("returnTicker")
        lastPairPrice = {}
        lastPairPrice = currentValues[self.pair]["last"]
        return lastPairPrice
