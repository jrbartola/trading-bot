import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy

coins_bttx = ["BTC-ETH", "BTC-LTC", "BTC-XMR", "BTC-OMG", "BTC-XRP", "BTC-SC", "BTC-XEM", "BTC-DASH", "BTC-STR", "BTC-LSK",
         "BTC-GNT", "BTC-VTC", "BTC-ETC", "BTC-STRAT", "BTC-DGB"]

coins_pol = ["BTC_ETH", "BTC_LTC", "BTC_XMR", "BTC_OMG", "BTC_XRP", "BTC_SC", "BTC_XEM", "BTC_DASH", "BTC_LSK",
         "BTC_GNT", "BTC_VTC", "BTC_ETC", "BTC_STRAT", "BTC_DGB"]

def main(coin):
    chart = BotChart("bittrex", coin, "fiveMin")

    strategy = BotStrategy(capital=0.01)

    for candlestick in chart.getPoints():
        strategy.tick(candlestick)

    print("Total Profit (" + coin + "): " + str(strategy.profit))

if __name__ == "__main__":
    for coin in coins_bttx:
        main(coin)
        #main(sys.argv[1:])