import unittest

from pyexchange.exchange import Exchange, ExchangeReporter


class TestExchange(unittest.TestCase):
    def test_transactions_1(self):
        exchange = Exchange()

        exchange.ask(3, 99)
        exchange.ask(8, 101)
        self.assertEqual(len(exchange.bids), 0)
        self.assertEqual(len(exchange.asks), 2)

        exchange.bid(10, 100)
        self.assertEqual(len(exchange.bids), 1)
        self.assertEqual(len(exchange.asks), 1)
        self.assertEqual(len(exchange.transactions), 1)
        self.assertEqual(exchange.bids[0].units, 7)

        exchange.ask(5, 97)
        self.assertEqual(len(exchange.bids), 1)
        self.assertEqual(len(exchange.asks), 1)
        self.assertEqual(len(exchange.transactions), 2)
        self.assertEqual(exchange.bids[0].units, 2)

        exchange.ask(2, 102)
        exchange.ask(3, 98)
        self.assertEqual(len(exchange.bids), 0)
        self.assertEqual(len(exchange.asks), 3)
        self.assertEqual(len(exchange.transactions), 3)
        self.assertEqual(exchange.asks[0].units, 1)

        exchange.bid(6, 97)
        self.assertEqual(len(exchange.bids), 1)
        self.assertEqual(len(exchange.asks), 3)
        self.assertEqual(len(exchange.transactions), 3)

        exchange.ask(2, 96)
        exchange.ask(1, 97)
        self.assertEqual(len(exchange.bids), 1)
        self.assertEqual(len(exchange.asks), 3)
        self.assertEqual(len(exchange.transactions), 5)
        self.assertEqual(exchange.bids[-1].units, 3)


class TestExchangeReporter(unittest.TestCase):
    def test_spread(self):
        exchange = Exchange()

        self.assertEqual(ExchangeReporter.spread(exchange), None)

        exchange.ask(1, 103)
        self.assertEqual(ExchangeReporter.spread(exchange), None)

        exchange.bid(1, 97)
        self.assertEqual(ExchangeReporter.spread(exchange), 6)

        exchange.ask(1, 99)
        self.assertEqual(ExchangeReporter.spread(exchange), 2)

        exchange.bid(1, 98)
        self.assertEqual(ExchangeReporter.spread(exchange), 1)

        exchange.bid(1, 99)
        self.assertEqual(ExchangeReporter.spread(exchange), 5)



if __name__ == '__main__':
    unittest.main()
