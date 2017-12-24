import urllib
import urllib2
import json
import time
import hmac,hashlib

def create_time_stamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

class Poloniex:
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def post_process(self, before):
        after = before

        # Add timestamps if there isnt one but is a datetime
        if 'return' in after:
            if isinstance(after['return'], list):
                for x in xrange(0, len(after['return'])):
                    if isinstance(after['return'][x], dict):
                        if 'datetime' in after['return'][x] and 'timestamp' not in after['return'][x]:
                            after['return'][x]['timestamp'] = float(create_time_stamp(after['return'][x]['datetime']))
                            
        return after

    def api_query(self, command, req={}):

        if command == "get_ticker" or command == "get_24hr_volume":
            ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=' + command))
            return json.loads(ret.read())
        elif command == "get_order_book":
            ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        elif command == "get_market_trade_history":
            ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=' + "get_trade_history" + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        elif command == "get_chart_data":
            ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=returnChartData&currencyPair=' + str(req['currencyPair']) + '&start=' + str(req['start']) + '&end=' + str(req['end']) + '&period=' + str(req['period'])))
            return json.loads(ret.read())
        else:
            req['command'] = command
            req['nonce'] = int(time.time()*1000)
            post_data = urllib.urlencode(req)

            sign = hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest()
            headers = {
                'Sign': sign,
                'Key': self.APIKey
            }

            ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
            jsonRet = json.loads(ret.read())
            return self.post_process(jsonRet)

    def get_ticker(self):
        return self.api_query("get_ticker")

    def get_24hr_volume(self):
        return self.api_query("get_24hr_volume")

    def get_order_book (self, currency_pair):
        return self.api_query("get_order_book", {'currency_pair': currency_pair})

    def get_market_trade_history (self, currency_pair):
        return self.api_query("get_market_trade_history", {'currency_pair': currency_pair})


    # Returns all of your balances.
    # Outputs: 
    # {"BTC":"0.59098578","LTC":"3.31117268", ... }
    def get_balances(self):
        return self.api_query('get_balances')

    # Returns your open orders for a given market, specified by the "currencyPair" POST parameter, e.g. "BTC_XCP"
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs: 
    # orderNumber   The order number
    # type          sell or buy
    # rate          Price the order is selling or buying at
    # Amount        Quantity of order
    # total         Total value of order (price * quantity)
    def get_open_orders(self, currency_pair):
        return self.api_query('get_open_orders', {"currency_pair": currency_pair})


    # Returns your trade history for a given market, specified by the "currencyPair" POST parameter
    # Inputs:
    # currency_pair  The currency pair e.g. "BTC_XCP"
    # Outputs: 
    # date          Date in the form: "2014-02-19 03:44:59"
    # rate          Price the order is selling or buying at
    # amount        Quantity of order
    # total         Total value of order (price * quantity)
    # type          sell or buy
    def get_trade_history(self, currency_pair):
        return self.api_query('get_trade_history', {"currency_pair": currency_pair})

    # Places a buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currency_pair  The currency pair
    # rate          price the order is buying at
    # amount        Amount of coins to buy
    # Outputs: 
    # orderNumber   The order number
    def buy(self, currency_pair, rate, amount):
        return self.api_query('buy', {"currency_pair": currency_pair, "rate": rate, "amount": amount})

    # Places a sell order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currency_pair  The currency pair
    # rate          price the order is selling at
    # amount        Amount of coins to sell
    # Outputs: 
    # orderNumber   The order number
    def sell(self, currency_pair, rate, amount):
        return self.api_query('sell', {"currency_pair": currency_pair, "rate": rate, "amount": amount})

    # Cancels an order you have placed in a given market. Required POST parameters are "currencyPair" and "orderNumber".
    # Inputs:
    # currency_pair  The currency pair
    # order_number   The order number to cancel
    # Outputs: 
    # succes        1 or 0
    def cancel(self, currency_pair, order_number):
        return self.api_query('cancel_order', {"currency_pair": currency_pair, "order_number": order_number})

    # Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method, the withdrawal privilege must be enabled for your API key. Required POST parameters are "currency", "amount", and "address". Sample output: {"response":"Withdrew 2398 NXT."} 
    # Inputs:
    # currency      The currency to withdraw
    # amount        The amount of this coin to withdraw
    # address       The withdrawal address
    # Outputs: 
    # response      Text containing message about the withdrawal
    def withdraw(self, currency, amount, address):
        return self.api_query('withdraw', {"currency": currency, "amount": amount, "address": address})