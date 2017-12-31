from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
import random
import matplotlib.pyplot as plt

class BotStrategy(object):
    def __init__(self, pair, capital, backtesting=False, client=None):
        self.output = BotLog()
        self.prices = []
        self.closes = [] # Needed for Momentum Indicator
        self.trades = []
        self.current_price = None
        self.timestamp = None
        self.current_close = None
        self.max_trades_at_once = 1
        self.indicators = BotIndicators
        self.profit = 0
        self.pair = pair
        self.reserve = capital
        self.backtesting = backtesting
        self.client = client

    def tick(self, candlestick):
        op, clos = candlestick.open, candlestick.close

        # For backtest history, uniformly sample a random price between the opening and closing
        self.current_price = random.uniform(min(op, clos), max(op, clos))

        # Append a timestamp so we can add it to the plot
        self.timestamp = candlestick.time
        #self.current_price = float(candlestick.price_average)

        self.prices.append(self.current_price)

        self.evaluate_positions()
        self.update_open_trades()

    def live_tick(self, current_price):
        if not self.backtesting:
            self.current_price = current_price

            self.prices.append(self.current_price)

            # Make sure we have enough information to allow our indicators to work properly
            if len(self.prices) < 50:
                return

            # Reduce the maximum number of data points in memory to at most 100
            self.prices = self.prices[-100:]

            self.evaluate_positions()
            self.update_open_trades()

    def evaluate_positions(self):
        #_, _, macd = self.indicators.macd(self.prices)
        rsi = self.indicators.rsi(self.prices)
        nine_period = self.indicators.moving_average(self.prices, 9)
        fifteen_period = self.indicators.moving_average(self.prices, 15)
        bb1, bb2 = self.indicators.bollinger_bands(self.prices, k=2.)
        bb_diff = bb1 - bb2
        percent_diff = self.indicators.percent_difference(self.prices)
        # print(percent_diff)

        open_trades = []
        for trade in self.trades:
            if trade.status == "OPEN":
                open_trades.append(trade)

        if len(open_trades) < self.max_trades_at_once:
            # if self.current_price < nine_period and self.current_price < fifteen_period and rsi < 40:
            if self.current_price < nine_period and self.current_price < fifteen_period and rsi < 50 and self.current_price < bb1 - 0.8 * bb_diff and percent_diff > 0:
                assert self.reserve > 0

                if self.client:
                    buy_at = self.current_price + 0.000001

                    #### USE CLIENT TO SEND API REQUEST TO BUY THE TRADE AT A BIT HIGHER THAN THE LAST PRICE
                    # ret = self.client.buy_limit(self.pair, self.reserve / buy_at, buy_at)
                    ret = self.client.trade_buy(market=self.pair, order_type="MARKET",
                                                 quantity=self.reserve / self.current_price, time_in_effect="FILL_OR_KILL")

                    if ret['success'] is True:
                        self.output.log("Buy order was placed with UUID: " + ret['result']['uuid'], "success")
                        new_trade = BotTrade(self.pair, buy_at, self.reserve, stop_loss=0.00001)
                        self.reserve = 0
                        self.trades.append(new_trade)
                    else:
                        self.output.log("Buy order was unsuccessful. Reason: " + ret['message'], "error")
                else:
                    plt.plot(self.timestamp, self.current_price, 'gx')
                    new_trade = BotTrade(self.pair, self.current_price, self.reserve, stop_loss=0.00001)
                    self.reserve = 0
                    self.trades.append(new_trade)

        for trade in open_trades:
            if self.current_price > (0.3 * bb_diff) + trade.entry_price or (self.current_price > nine_period and self.current_price > fifteen_period and rsi > 60):# and self.current_price > bb2 + 0.75 * bb_diff:
                if self.client:

                    #### USE CLIENT TO SEND API REQUEST TO CLOSE THE TRADE AT A BIT LOWER THAN THE LAST PRICE
                    # ret = self.client.sell_limit(trade.pair, trade.amount, self.current_price - 0.000001)
                    ret = self.client.trade_sell(market=trade.pair, order_type="MARKET",
                                                 quantity=trade.amount, time_in_effect="FILL_OR_KILL")

                    if ret['success'] is True:
                        self.output.log("Sell order was placed with UUID: " + ret['result']['uuid'], "success")
                        profit, total = trade.close(self.current_price)
                        self.profit += profit
                        self.reserve = total
                    else:
                        self.output.log("Sell order was unsuccessful. Reason: " + ret['message'], "error")

                else:
                    plt.plot(self.timestamp, self.current_price, 'rx')
                    profit, total = trade.close(self.current_price)
                    self.profit += profit
                    self.reserve = total

    def update_open_trades(self):
        for trade in self.trades:

            # Check our stop losses
            if trade.status == "OPEN" and trade.stop_loss and self.current_price < trade.stop_loss:

                # Use the exchange APIs if we are live with a client
                if self.client:

                    sell_at = self.current_price - 0.000001

                    #### USE CLIENT TO SEND API REQUEST TO CLOSE THE STOP LOSS TRADE AT A BIT LOWER THAN THE LAST PRICE
                    # ret = self.client.sell_limit(trade.pair, trade.amount, sell_at)
                    ret = self.client.trade_sell(market=trade.pair, order_type="MARKET",
                                                 quantity=trade.amount, time_in_effect="FILL_OR_KILL")

                    if ret['success'] is True:
                        self.output.log("STOP LOSS! Placed sell order with UUID: " + ret['result']['uuid'], "error")
                        profit, total = trade.close(sell_at)
                        self.profit += profit
                        self.reserve = total
                    else:
                        self.output.log("Sell order was unsuccessful. Reason: " + ret['message'], "error")
                else:
                    profit, total = trade.close(self.current_price)
                    plt.plot(self.timestamp, self.current_price, 'bx')
                    self.output.log("STOP LOSS! Closed Trade at " + str(self.current_price) + " BTC. Profit: " + str(profit) + ", BTC: " + str(total), "error")
                    self.profit += profit
                    self.reserve = total

    def show_positions(self):
        for trade in self.trades:
            trade.show_trade()
