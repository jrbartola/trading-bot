from botlog import BotLog

class BotTrade(object):
    def __init__(self, current_price, amt_btc, stop_loss=None):
        self.output = BotLog()
        self.status = "OPEN"
        self.entry_price = current_price
        self.exit_price = None
        self.output.log("Trade opened")
        self.amount = amt_btc / current_price
        if stop_loss:
            self.stop_loss = current_price - stop_loss
    
    def close(self, current_price):
        self.status = "CLOSED"
        self.exit_price = current_price
        self.output.log("Trade closed")
        return (self.amount * self.exit_price) - (self.amount * self.entry_price), self.amount * self.exit_price

    def tick(self, current_price):
        if self.stop_loss and current_price < self.stop_loss:
            self.close(current_price)

    def show_trade(self):
        trade_status = "Entry Price: "+str(self.entry_price) + " Status: " + str(self.status) + " Exit Price: " + str(self.exit_price)

        if self.status == "CLOSED":
            trade_status = trade_status + " Profit: "
            if self.exit_price > self.entry_price:
                trade_status = trade_status + "\033[92m"
            else:
                trade_status = trade_status + "\033[91m"

            trade_status = trade_status + str(self.exit_price - self.entry_price) + "\033[0m"

        self.output.log(trade_status)
