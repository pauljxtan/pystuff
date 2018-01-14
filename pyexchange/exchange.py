"""A simple toy exchange on which a commodity is bought and sold."""

# TODO:
# -- Add buyer/seller objects
# -- Add multiprocessing
# -- Order expiry

from datetime import datetime


class Exchange(object):
    def __init__(self):
        self.bids = []
        self.asks = []
        self.transactions = []

    def bid(self, units, price):
        """Places an order to buy a number of units at the given price per unit."""
        self.bids.append(Bid(units, price))
        # Sort the bids in decreasing price
        self.bids.sort(key=lambda bid: -bid.price)
        self.fill_orders()

    def ask(self, units, price):
        """Places an order to sell a number of units at the given price per unit."""
        self.asks.append(Ask(units, price))
        # Sort the asks in increasing price
        self.asks.sort(key=lambda ask: ask.price)
        self.fill_orders()

    def fill_orders(self):
        """Fills as many orders as possible. (Orders may be partially filled.)"""
        # TODO: Does it make sense to always start with bids? (And in descending price?)
        for i, bid in enumerate(self.bids):
            units_filled = 0
            while units_filled < bid.units:
                for j, ask in enumerate(self.asks):
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
                break
            self.bids[i].units -= units_filled

        # Remove filled orders
        self.bids = list(filter(lambda bid: bid.units > 0, self.bids))
        self.asks = list(filter(lambda ask: ask.units > 0, self.asks))


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
