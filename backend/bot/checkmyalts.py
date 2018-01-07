import sys, getopt
from chart import Chart
from strategy import BotStrategy
from logger import Logger


def main():
    LTC = Chart("bittrex", "BTC-LTC", "fiveMin", False)
    DASH = Chart("bittrex", "BTC-DASH", "fiveMin", False)
    LSK = Chart("bittrex", "BTC-LSK", "fiveMin", False)
    VTC = Chart("bittrex", "BTC-VTC", "fiveMin", False)

    logger = Logger

    myltc, prevltc = 1.8935, 0.01660036
    mydash, prevdash = 0.35, 0.074
    mylsk, prevlsk = 17.0, 0.001488
    myvtc, prevvtc = 49.49, 0.0004736

    ltc = LTC.get_current_price()
    dash = DASH.get_current_price()
    lsk = LSK.get_current_price()
    vtc = VTC.get_current_price()

    print("LTC: " + str(myltc * ltc - myltc * prevltc))
    print("DASH: " + str(mydash * dash - mydash * prevdash))
    print("LSK: " + str(mylsk * lsk - mylsk * prevlsk))
    print("VTC: " + str(myvtc * vtc - myvtc * prevvtc))


if __name__ == "__main__":
    main()