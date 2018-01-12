

class Decision(object):
    def __init__(self, indicators):
        self.indicators = indicators

    def should_buy(self, buy_strategy):
        for indicator in buy_strategy:
            comparator, value = indicator['comparator'], indicator['value']

            if comparator == 'LT':
                if self.indicators[indicator] >= value:
                    return False

            elif comparator == 'EQ':
                if self.indicators[indicator] != value:
                    return False

            elif comparator == 'GT':
                if self.indicators[indicator] <= value:
                    return False

        return True

    def should_sell(self, sell_strategy):
        for indicator in sell_strategy:
            comparator, value = indicator['comparator'], indicator['value']

            if comparator == 'LT':
                if self.indicators[indicator] >= value:
                    return False

            elif comparator == 'EQ':
                if self.indicators[indicator] != value:
                    return False

            elif comparator == 'GT':
                if self.indicators[indicator] <= value:
                    return False

        return True
