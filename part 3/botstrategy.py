from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
import random

class BotStrategy(object):
    def __init__(self, capital):
        self.output = BotLog()
        self.prices = []
        self.closes = [] # Needed for Momentum Indicator
        self.trades = []
        self.current_price = None
        self.current_close = None
        self.max_trades_at_once = 1
        self.indicators = BotIndicators
        self.profit = 0
        self.reserve = capital

    def tick(self,candlestick):
        op, clos = candlestick.open, candlestick.close

        # For backtest history, uniformly sample a random price between the opening and closing
        self.current_price = random.uniform(min(op, clos), max(op, clos))
        #self.current_price = float(candlestick.price_average)

        self.prices.append(self.current_price)
        
        #self.current_close = float(candlestick['close'])
        #self.closes.append(self.current_close)
        
        #self.output.log("Price: "+str(candlestick.price_average)+"\tMoving Average: "+str(self.indicators.moving_average(self.prices,15)))

        self.evaluate_positions()
        self.update_open_trades()
        #self.showPositions()

    def evaluate_positions(self):
        #_, _, macd = self.indicators.macd(self.prices)
        rsi = self.indicators.rsi(self.prices)

        open_trades = []
        for trade in self.trades:
            if trade.status == "OPEN":
                open_trades.append(trade)

        if len(open_trades) < self.max_trades_at_once:
            if self.current_price < self.indicators.moving_average(self.prices, 9):# and rsi < 45:
                new_trade = BotTrade(self.current_price, self.reserve, stop_loss=0.0001)
                self.trades.append(new_trade)

        for trade in open_trades:
            if self.current_price > self.indicators.moving_average(self.prices, 9) and rsi > 55:
                profit, total = trade.close(self.current_price)
                # print("Profit is " + str(profit))
                # if profit < 0:
                #     print("Lost Profit")
                self.profit += profit
                self.reserve = total

    def update_open_trades(self):
        for trade in self.trades:
            if trade.status == "OPEN":
                trade.tick(self.current_price)

    def show_positions(self):
        for trade in self.trades:
            trade.show_trade()
