import numpy as np


class BotIndicators(object):
    def __init__(self):
        pass

    @staticmethod
    def moving_average(data_points, period):
        if len(data_points) > 1:
            return sum(data_points[-period:]) / float(len(data_points[-period:]))
        return 0

    @staticmethod
    def momentum(data_points, period=14):
        if len(data_points) > period - 1:
            return data_points[-1] * 100 / data_points[-period]

    @staticmethod
    def ema(prices, period):
        x = np.asarray(prices)
        weights = np.exp(np.linspace(-1., 0., period))
        weights /= weights.sum()

        a = np.convolve(x, weights, mode='full')[:len(x)]
        if len(a) <= period:
            return 0
        a[:period] = a[period]
        return a

    @staticmethod
    def macd(prices, nslow=26, nfast=12):
        emaslow = BotIndicators.ema(prices, nslow)
        emafast = BotIndicators.ema(prices, nfast)
        return emaslow, emafast, emafast - emaslow        

    @staticmethod
    def rsi(prices, period=14):
        deltas = np.diff(prices)
        seed = deltas[:period + 1]
        rsi_up = seed[seed >= 0].sum() / period
        rsi_down = -seed[seed < 0].sum() / period

        rsi = np.zeros_like(prices)
        rs = rsi_up / rsi_down
        rsi[:period] = 100. - 100./(1. + rs)
 
        for i in range(period, len(prices)):
            delta = deltas[i - 1]  # cause the diff is 1 shorter
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
 
            rsi_up = (rsi_up * (period - 1) + upval) / period
            rsi_down = (rsi_down * (period - 1) + downval) / period
            rs = rsi_up/rsi_down
            rsi[i] = 100. - 100./(1. + rs)

        if len(prices) > period:
            return rsi[-1]
        else:
            return 50 # output a neutral amount until enough prices in list to calculate rsi

    @staticmethod
    def bollinger_bands(prices, period=21, k=2):
        sma = BotIndicators.moving_average(prices, period)
        std_dev = np.std(prices)

        return sma + k * std_dev, sma - k * std_dev
