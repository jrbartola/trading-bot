from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

class BotStrategy(object):
    def __init__(self, capital):
        self.output = BotLog()
        self.prices = []
        self.closes = [] # Needed for Momentum Indicator
        self.trades = []
        self.currentPrice = ""
        self.currentClose = ""
        self.numSimulTrades = 1
        self.indicators = BotIndicators()
        self.profit = 0
        self.reserve = capital

    def tick(self,candlestick):
        self.currentPrice = float(candlestick.priceAverage)
        self.prices.append(self.currentPrice)
        
        #self.currentClose = float(candlestick['close'])
        #self.closes.append(self.currentClose)
        
        #self.output.log("Price: "+str(candlestick.priceAverage)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

        self.evaluatePositions()
        self.updateOpenTrades()
        self.showPositions()

    def evaluatePositions(self):
        _, _, macd = self.indicators.MACD(self.prices)

        openTrades = []
        for trade in self.trades:
            if trade.status == "OPEN":
                openTrades.append(trade)

        if len(openTrades) < self.numSimulTrades:
            if self.currentPrice < self.indicators.movingAverage(self.prices,9):
                self.trades.append(BotTrade(self.currentPrice, self.reserve, stopLoss=0.0001))

        for trade in openTrades:
            if self.currentPrice > self.indicators.movingAverage(self.prices, 9) and self.indicators.RSI(self.prices) > 55:
                profit, total = trade.close(self.currentPrice)
                # print("Profit is " + str(profit))
                # if profit < 0:
                #     print("Lost Profit")
                self.profit += profit
                self.reserve = total

    def updateOpenTrades(self):
        for trade in self.trades:
            if trade.status == "OPEN":
                trade.tick(self.currentPrice)

    def showPositions(self):
        for trade in self.trades:
            trade.showTrade()