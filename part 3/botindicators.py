import numpy as np


class BotIndicators(object):
    def __init__(self):
        self.rsi = []
        self.rsi_up = 0
        self.rsi_down = 0
        pass

    @staticmethod
    def moving_average(data_points, period):
        if len(data_points) > 1:
            return sum(data_points[-period:]) / float(len(data_points[-period:]))

    @staticmethod
    def momentum(dataPoints, period=14):
        if len(dataPoints) > period -1:
            return dataPoints[-1] * 100 / dataPoints[-period]

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

    def rsi(self, prices, period=14):
        deltas = np.diff(prices)
        seed = deltas[:period + 1]
        self.rsi_up = seed[seed >= 0].sum() / period
        self.rsi_down = -seed[seed < 0].sum() / period

        if False and len(self.rsi) > period:
            n = len(prices) - 1
            delta = deltas[n - 1]  # cause the diff is 1 shorter
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            self.rsi_up = (self.rsi_up * (period - 1) + upval) / period
            self.rsi_down = (self.rsi_down * (period - 1) + downval) / period
            rs = self.rsi_up / self.rsi_down
            self.rsi = np.append(self.rsi, (100. - 100. / (1. + rs)))
        else:
            rsi = np.zeros_like(prices)
            rs = self.rsi_up / self.rsi_down
            rsi[:period] = 100. - 100./(1. + rs)
 
            for i in range(period, len(prices)):
                delta = deltas[i - 1]  # cause the diff is 1 shorter
                if delta > 0:
                    upval = delta
                    downval = 0.
                else:
                    upval = 0.
                    downval = -delta
 
                self.rsi_up = (self.rsi_up*(period - 1) + upval)/period
                self.rsi_down = (self.rsi_down*(period - 1) + downval)/period
                rs = self.rsi_up/self.rsi_down
                rsi[i] = 100. - 100./(1. + rs)

            self.rsi = rsi

        if len(prices) > period:
            return self.rsi[-1]
        else:
            return 50 # output a neutral amount until enough prices in list to calculate rsi
