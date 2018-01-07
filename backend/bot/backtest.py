import sys, getopt
import matplotlib.pyplot as plt
from chart import Chart
from strategy import BotStrategy
import json

coins_bttx = ["BTC-ETH", "BTC-LTC", "BTC-XMR", "BTC-OMG", "BTC-XRP", "BTC-SC", "BTC-XEM", "BTC-DASH", "BTC-LSK",
         "BTC-GNT", "BTC-VTC", "BTC-ETC", "BTC-STRAT", "BTC-DGB"]

coins_pol = ["BTC_ETH", "BTC_LTC", "BTC_XMR", "BTC_OMG", "BTC_XRP", "BTC_SC", "BTC_XEM", "BTC_DASH", "BTC-STR", "BTC_LSK",
         "BTC_GNT", "BTC_VTC", "BTC_ETC", "BTC_STRAT", "BTC_DGB"]

def main(coin):
    chart = Chart("bittrex", coin, "fiveMin", start_time=1514044163)

    strategy = BotStrategy(capital=0.01, pair=coin, trading_fee=0.0025)

    for candlestick in chart.get_points():
        strategy.tick(candlestick)

    chart.plot_indicators(bollinger=21, movingaverage=[9, 15])
    strategy.plot_buys()
    strategy.plot_sells()
    plt.show()

    closings = [[i, d.close] for i, d in enumerate(chart.get_points())]
    indicators = chart.get_indicators(bollinger=21, movingaverage=[9, 15])

    result = {'buys': list(strategy.buys), 'sells': list(strategy.sells), 'closingPrices': closings,
              'indicators': indicators}

    print("Total Profit (" + coin + "): " + str(strategy.profit * 0.9975))

    print(json.dumps(result))

def backtest(coin_pair, period_length, capital):
    chart = Chart("bittrex", coin_pair, period_length, start_time=1514044163)

    strategy = BotStrategy(capital=capital, pair=coin_pair, trading_fee=0.0025)

    for candlestick in chart.get_points():
        strategy.tick(candlestick)

    closings = [[i, d.close] for i, d in enumerate(chart.get_points())]
    indicators = chart.get_indicators(bollinger=21, movingaverage=[9, 15])

    result = {'buys': list(strategy.buys), 'sells': list(strategy.sells), 'closingPrices': closings,
              'indicators': indicators, 'profit': strategy.profit}

    return result

if __name__ == "__main__":
    for coin in coins_bttx:
        main(coin)
        #main(sys.argv[1:])