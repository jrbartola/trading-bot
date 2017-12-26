import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy

coins_bttx = ["BTC-ETH", "BTC-LTC", "BTC-XMR", "BTC-OMG", "BTC-XRP", "BTC-SC", "BTC-XEM", "BTC-DASH", "BTC-LSK",
         "BTC-GNT", "BTC-VTC", "BTC-ETC", "BTC-STRAT", "BTC-DGB"]

coins_pol = ["BTC_ETH", "BTC_LTC", "BTC_XMR", "BTC_OMG", "BTC_XRP", "BTC_SC", "BTC_XEM", "BTC_DASH", "BTC-STR", "BTC_LSK",
         "BTC_GNT", "BTC_VTC", "BTC_ETC", "BTC_STRAT", "BTC_DGB"]

def main(coin):
    chart = BotChart("bittrex", coin, "oneMin", start_time=1514044163)

    strategy = BotStrategy(capital=0.01, pair=coin)

    for candlestick in chart.get_points():
        strategy.tick(candlestick)

    print("Total Profit (" + coin + "): " + str(strategy.profit))

if __name__ == "__main__":
    for coin in coins_bttx:
        main(coin)
        #main(sys.argv[1:])