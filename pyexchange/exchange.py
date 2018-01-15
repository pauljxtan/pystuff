# TODO:
# -- Report spread, volume, moving average, etc.
# -- Add buyer/seller objects
# -- Add multiprocessing
# -- Order expiry

from datetime import datetime


class Exchange(object):
    """A simple toy exchange on which a commodity is bought and sold."""

    def __init__(self):
        self.bids = []
        self.asks = []
        self.transactions = []

    def bid(self, units, price):
        """Places an order to buy a number of units at the given price per unit."""
        self.bids.append(Bid(units, price))
        # Sort the bids in decreasing price
        self.bids.sort(key=lambda bid: -bid.price)
        self._fill_asks()

    def ask(self, units, price):
        """Places an order to sell a number of units at the given price per unit."""
        self.asks.append(Ask(units, price))
        # Sort the asks in increasing price
        self.asks.sort(key=lambda ask: ask.price)
        self._fill_bids()

    def _fill_bids(self):
        """Fills as many bids as possible. (Orders may be partially filled.)"""
        for i, bid in enumerate(self.bids):
            units_filled = 0
            for j, ask in enumerate(self.asks):
                if units_filled == bid.units:
                    break
                if ask.price <= bid.price:
                    remaining_units = bid.units - units_filled
                    if ask.units > remaining_units:
                        self.asks[j].units -= remaining_units
                        units_filled += remaining_units
                    else:
                        units_filled += ask.units
                        self.asks[j].units = 0
                    self.transactions.append(Transaction("TODO", "TODO", units_filled, ask.price))
                    # TODO: in an actual exchange we would also charge/pay the buyer/seller, etc.
            self.bids[i].units -= units_filled

        self._remove_filled_orders()

    def _fill_asks(self):
        """Fills as many asks as possible. (Orders may be partially filled.)"""
        for i, ask in enumerate(self.asks):
            units_filled = 0
            for j, bid in enumerate(self.bids):
                if units_filled == ask.units:
                    break
                if bid.price >= ask.price:
                    remaining_units = ask.units - units_filled
                    if bid.units > remaining_units:
                        self.bids[j].units -= remaining_units
                        units_filled += remaining_units
                    else:
                        units_filled += bid.units
                        self.bids[j].units = 0
                    self.transactions.append(Transaction("TODO", "TODO", units_filled, bid.price))
                    # TODO: in an actual exchange we would also charge/pay the buyer/seller, etc.
            self.asks[i].units -= units_filled

        self._remove_filled_orders()

    def _remove_filled_orders(self):
        self.bids = list(filter(lambda bid: bid.units > 0, self.bids))
        self.asks = list(filter(lambda ask: ask.units > 0, self.asks))


class ExchangeReporter(object):
    @classmethod
    def spread(cls, exchange):
        """Returns the spread between the highest bid and lowest ask."""
        if len(exchange.asks) == 0 or len(exchange.bids) == 0:
            return None
        return exchange.asks[0].price - exchange.bids[0].price


class Order(object):
    def __init__(self, units, price):
        self.units = units
        self.price = price
        self.timestamp = datetime.now()


class Bid(Order):
    def __init__(self, units, price):
        super(Bid, self).__init__(units, price)

    def __repr__(self):
        return "[Bid: units={}, price={}]".format(self.units, self.price)


class Ask(Order):
    def __init__(self, units, price):
        super(Ask, self).__init__(units, price)

    def __repr__(self):
        return "[Ask: units={}, price={}]".format(self.units, self.price)


class Transaction(object):
    def __init__(self, buyer, seller, units, price):
        self.buyer = buyer
        self.seller = seller
        self.units = units
        self.price = price
        self.timestamp = datetime.now()

    def __repr__(self):
        return "[Transaction: buyer={}, seller={}, units={}, price={}]".format(
            self.buyer, self.seller, self.units, self.price
        )
