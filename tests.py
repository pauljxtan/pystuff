import random
import unittest
from tile import (ManTile, PinTile, SouTile, WindTile, DragonTile, TERMINALS,
                  HONOURS, NUMBERS, NUMBERED_TILE_TYPES, WINDS, COLOURS,
                  Pair, Sequence, Triplet, Quadruplet)
import yaku

class TypeTests(unittest.TestCase):

    def test_tile_eq(self):
        """
        Tests Tile equality magic methods.
        """
        self.assertTrue(all([tile_type(number) == tile_type(number)
                             for tile_type in NUMBERED_TILE_TYPES
                             for number in NUMBERS]))
        self.assertTrue(all([WindTile(wind) == WindTile(wind)
                             for wind in WINDS]))
        self.assertTrue(all([DragonTile(colour) == DragonTile(colour)
                             for colour in COLOURS]))

    def test_tile_cmp(self):
        """
        Tests Tile comparison magic methods.
        """
        # Within own type
        self.assertTrue(all([tile_type(number1) < tile_type(number2)
                             for tile_type in NUMBERED_TILE_TYPES
                             for number1 in NUMBERS for number2 in NUMBERS
                             if number1 < number2]))
        self.assertTrue(all([WindTile(wind1) < WindTile(wind2)
                             for wind1 in WINDS for wind2 in WINDS
                             if WINDS.index(wind1) < WINDS.index(wind2)]))
        self.assertTrue(all([DragonTile(colour1) < DragonTile(colour2)
                             for colour1 in COLOURS for colour2 in COLOURS
                             if COLOURS.index(colour1) < COLOURS.index(colour2)]))

        # Between types
        # TODO

    def test_group_init(self):
        """
        Tests initializing Group objects with the head (first) tile.
        """
        self.assertEqual(Pair(ManTile(1)).tiles, [ManTile(1), ManTile(1)])
        self.assertEqual(Sequence(PinTile(2)).tiles,
                         [PinTile(2), PinTile(3), PinTile(4)])
        self.assertEqual(Triplet(SouTile(5)).tiles,
                         [SouTile(5), SouTile(5), SouTile(5)])
        self.assertEqual(Quadruplet(WindTile('east')).tiles,
                         [WindTile('east'), WindTile('east'),
                          WindTile('east'), WindTile('east')])

class YakuTests(unittest.TestCase):

    def test_is_tanyao(self):
        groups = [Pair(SouTile(2)), Sequence(ManTile(2)), Triplet(PinTile(5)),
                  Sequence(SouTile(5)), Quadruplet(ManTile(8))]
        random.shuffle(groups)
        self.assertTrue(yaku.is_tanyao(groups))

        groups = [Pair(SouTile(2)), Sequence(ManTile(2)), Triplet(PinTile(5)),
                  Sequence(SouTile(7)), Quadruplet(ManTile(8))]
        random.shuffle(groups)
        self.assertFalse(yaku.is_tanyao(groups))

    def test_is_iipeikou(self):
        groups = [Pair(WindTile('south')), Sequence(SouTile(3)),
                  Sequence(SouTile(3)), Sequence(PinTile(5)),
                  Sequence(ManTile(5))]
        random.shuffle(groups)
        self.assertTrue(yaku.is_iipeikou(groups))
        self.assertFalse(yaku.is_ryanpeikou(groups))

    def test_is_yakuhai(self):
        prevailing_wind = 'east'
        player_wind = 'west'

        groups = [Pair(ManTile(5)), Sequence(PinTile(6)),
                  Triplet(WindTile(player_wind)), Triplet(SouTile(3)),
                  Sequence(ManTile(2))]
        self.assertTrue(yaku.is_yakuhai(groups, prevailing_wind, player_wind))

        groups = [Pair(ManTile(5)), Sequence(PinTile(6)),
                  Triplet(DragonTile('red')), Triplet(SouTile(3)),
                  Sequence(ManTile(2))]
        self.assertTrue(yaku.is_yakuhai(groups, prevailing_wind, player_wind))

        groups = [Pair(WindTile(prevailing_wind)), Sequence(PinTile(6)),
                  Triplet(WindTile('north')), Triplet(SouTile(3)),
                  Sequence(ManTile(2))]
        self.assertFalse(yaku.is_yakuhai(groups, prevailing_wind, player_wind))

    def test_is_chanta(self):
        groups = [Pair(WindTile('south')), Sequence(SouTile(1)),
                  Sequence(PinTile(7)), Triplet(DragonTile('green')),
                  Triplet(ManTile(9))]
        random.shuffle(groups)
        self.assertTrue(yaku.is_chanta(groups))

        groups = [Pair(WindTile('south')), Sequence(SouTile(1)),
                  Sequence(PinTile(6)), Triplet(DragonTile('green')),
                  Triplet(ManTile(9))]
        random.shuffle(groups)
        self.assertFalse(yaku.is_chanta(groups))

    def is_sanshoku_doujun(self):
        return

    def test_is_toitoi(self):
        groups = [Pair(SouTile(8)), Triplet(ManTile(3)), Triplet(SouTile(7)),
                  Quadruplet(WindTile('west')), Triplet(DragonTile('green'))]
        self.assertTrue(yaku.is_toitoi(groups))

        groups = [Pair(SouTile(8)), Triplet(ManTile(3)), Sequence(SouTile(7)),
                  Quadruplet(WindTile('west')), Triplet(DragonTile('green'))]
        self.assertFalse(yaku.is_toitoi(groups))

    def test_is_sanankou(self):
        groups = [Pair(DragonTile('red')), Triplet(ManTile(5)),
                  Triplet(PinTile(2)), Triplet(WindTile('east')),
                  Sequence(SouTile(6))]
        random.shuffle(groups)
        self.assertTrue(yaku.is_sanankou(groups))

        # 2 closed, 1 open
        groups = [Pair(DragonTile('red')), Triplet(ManTile(5), False),
                  Triplet(PinTile(2)), Triplet(WindTile('east')),
                  Sequence(SouTile(6))]
        random.shuffle(groups)
        self.assertFalse(yaku.is_sanankou(groups))

        # 3 closed, 1 open
        groups = [Pair(DragonTile('red')), Triplet(ManTile(5), False),
                  Triplet(PinTile(2)), Triplet(WindTile('east')),
                  Triplet(SouTile(6))]
        random.shuffle(groups)
        self.assertTrue(yaku.is_sanankou(groups))

    def test_is_sanshoku_doukou(self):
        groups = [Pair(DragonTile('white')), Triplet(ManTile(7)),
                  Triplet(PinTile(7)), Triplet(SouTile(7)),
                  Sequence(ManTile(1))]
        self.assertTrue(yaku.is_sanshoku_doukou(groups))

    def test_is_sankantsu(self):
        groups = [Pair(PinTile(8)), Sequence(ManTile(3)),
                  Quadruplet(SouTile(2)), Quadruplet(WindTile('north')),
                  Quadruplet(DragonTile('green'))]
        self.assertTrue(yaku.is_sankantsu(groups))

    def test_is_chitoi(self):
        tiles = (2 * [ManTile(2)] + 2 * [PinTile(5)] + 2 * [SouTile(8)] +
                 2 * [WindTile('east')] + 2 * [WindTile('north')] +
                 2 * [DragonTile('white')] + 2 * [DragonTile('red')])
        random.shuffle(tiles)
        self.assertTrue(yaku.is_chitoi(tiles))

        tiles = (2 * [ManTile(2)] + 1 * [PinTile(5)] + 2 * [SouTile(8)] +
                 2 * [WindTile('east')] + 3 * [WindTile('north')] +
                 2 * [DragonTile('white')] + 2 * [DragonTile('red')])
        random.shuffle(tiles)
        self.assertFalse(yaku.is_chitoi(tiles))

    def test_is_ittsu(self):
        groups = [Pair(ManTile(6)), Sequence(PinTile(1)), Sequence(PinTile(4)),
                  Sequence(PinTile(7)), Sequence(SouTile(7))]
        random.shuffle(groups)
        self.assertTrue(yaku.is_ittsu(groups))

        groups = [Pair(ManTile(6)), Sequence(PinTile(1)), Sequence(SouTile(4)),
                  Sequence(PinTile(7)), Sequence(SouTile(7))]
        random.shuffle(groups)
        self.assertFalse(yaku.is_ittsu(groups))

    def test_is_shousangen(self):
        groups = [Pair(DragonTile('green')), Sequence(SouTile(6)),
                  Triplet(WindTile('south')), Triplet(DragonTile('red')),
                  Triplet(DragonTile('white'))]
        random.shuffle(groups)
        self.assertTrue(yaku.is_shousangen(groups))

        groups = [Pair(WindTile('north')), Sequence(SouTile(6)),
                  Triplet(WindTile('south')), Triplet(DragonTile('red')),
                  Triplet(DragonTile('white'))]
        random.shuffle(groups)
        self.assertFalse(yaku.is_shousangen(groups))

        groups = [Pair(DragonTile('green')), Sequence(SouTile(6)),
                  Triplet(WindTile('south')), Triplet(PinTile(2)),
                  Triplet(DragonTile('white'))]
        random.shuffle(groups)
        self.assertFalse(yaku.is_shousangen(groups))

    def test_is_ryanpeikou(self):
        groups = [Pair(WindTile('south')), Sequence(SouTile(3)),
                  Sequence(SouTile(3)), Sequence(PinTile(5)),
                  Sequence(PinTile(5))]
        random.shuffle(groups)
        self.assertFalse(yaku.is_iipeikou(groups))
        self.assertTrue(yaku.is_ryanpeikou(groups))

    def test_is_kokushi(self):
        tiles = list(TERMINALS + HONOURS) + [WindTile('east')]
        random.shuffle(tiles)
        self.assertTrue(yaku.is_kokushi(tiles))

        tiles = list(TERMINALS + HONOURS) + [ManTile(2)]
        random.shuffle(tiles)
        self.assertFalse(yaku.is_kokushi(tiles))

TEST_CASES = (TypeTests, YakuTests)

def suite():
    return unittest.TestSuite(
        [unittest.TestLoader().loadTestsFromTestCase(test_case)
         for test_case in TEST_CASES]
    )

if __name__ == '__main__':
    #unittest.main(verbosity=2)
    unittest.TextTestRunner(verbosity=2).run(suite())
