from copy import deepcopy

NUMBERS = tuple(range(1, 10))
SUITS = ('man', 'pin', 'sou')
WINDS = ('east', 'south', 'west', 'north')
COLOURS = ('white', 'green', 'red')

#### Tiles

class Tile(object):
    """
    Ordering:
        manzu (1-9) < pinzu (1-9) < souzu (1-9) < winds (eswn) < dragons (wgr)
    """
    def __init__(self):
        pass

class NumberedTile(Tile):
    def __init__(self, number):
        Tile.__init__(self)
        self.number = number

class ManTile(NumberedTile):
    def __eq__(self, other):
        return isinstance(other, ManTile) and self.number == other.number

    def __cmp__(self, other):
        if not isinstance(other, ManTile):
            return -1
        return self.number - other.number

    def __hash__(self):
        return hash(("man", self.number))

    def __str__(self):
        return str(self.number) + "-man"
    def __repr__(self):
        return self.__str__()

    def __init__(self, number):
        NumberedTile.__init__(self, number)

class PinTile(NumberedTile):
    def __eq__(self, other):
        return isinstance(other, PinTile) and self.number == other.number

    def __cmp__(self, other):
        if not isinstance(other, PinTile):
            if isinstance(other, ManTile):
                return 1
            return -1
        return self.number - other.number

    def __hash__(self):
        return hash(("pin", self.number))

    def __str__(self):
        return str(self.number) + "-pin"
    def __repr__(self):
        return self.__str__()

    def __init__(self, number):
        NumberedTile.__init__(self, number)

class SouTile(NumberedTile):
    def __eq__(self, other):
        return isinstance(other, SouTile) and self.number == other.number

    def __cmp__(self, other):
        if not isinstance(other, SouTile):
            if isinstance(other, ManTile) or isinstance(other, PinTile):
                return 1
            return -1
        return self.number - other.number

    def __hash__(self):
        return hash(("sou", self.number))

    def __str__(self):
        return str(self.number) + "-sou"
    def __repr__(self):
        return self.__str__()

    def __init__(self, number):
        NumberedTile.__init__(self, number)

class HonourTile(Tile):
    def __init__(self):
        Tile.__init__(self)

class WindTile(HonourTile):
    def __eq__(self, other):
        return isinstance(other, WindTile) and self.wind == other.wind

    def __cmp__(self, other):
        if not isinstance(other, WindTile):
            if isinstance(other, DragonTile):
                return -1
            return 1
        return WINDS.index(self.wind) - WINDS.index(other.wind)

    def __hash__(self):
        return hash((self.wind))

    def __str__(self):
        return self.wind
    def __repr__(self):
        return self.__str__()

    def __init__(self, wind):
        HonourTile.__init__(self)
        self.wind = wind

class DragonTile(HonourTile):
    def __eq__(self, other):
        return isinstance(other, DragonTile) and self.colour == other.colour

    def __cmp__(self, other):
        if not isinstance(other, DragonTile):
            return 1
        return COLOURS.index(self.colour) - COLOURS.index(other.colour)

    def __hash__(self):
        return hash((self.colour))

    def __str__(self):
        return self.colour
    def __repr__(self):
        return self.__str__()

    def __init__(self, colour):
        HonourTile.__init__(self)
        self.colour = colour

NUMBERED_TILE_TYPES = (ManTile, PinTile, SouTile)
HONOUR_TILE_TYPES = (WindTile, DragonTile)
TILE_TYPES = NUMBERED_TILE_TYPES + HONOUR_TILE_TYPES

TERMINALS = tuple([tile_type(number) for tile_type in NUMBERED_TILE_TYPES
                   for number in (NUMBERS[0], NUMBERS[-1])])
WIND_TILES = tuple([WindTile(wind) for wind in WINDS])
DRAGONS = tuple([DragonTile(colour) for colour in COLOURS])
HONOURS = WIND_TILES + DRAGONS

#### Groups

class Group(object):
    """
    Represents a tile group (mentsu): pair (jantou), sequence (shuntsu),
    triplet (koutsu) or quadruplet (kantsu).
    """
    def __cmp__(self, other):
        return self.tiles[0].__cmp__(other.tiles[0])

    def __init__(self, head, closed):
        self.tiles = [head]
        self.closed = closed
        self.ttype = type(head)

class Pair(Group):
    def __eq__(self, other):
        return isinstance(other, Pair) and self.tiles == other.tiles

    def __hash__(self):
        return hash(("pair", tuple(self.tiles)))

    def __str__(self):
        return "pair(%s, %s)" % (self.tiles[0], self.tiles[1])
    def __repr__(self):
        return self.__str__()

    def __init__(self, head):
        Group.__init__(self, head, True)
        self.tiles += [deepcopy(self.tiles[0])]

class Sequence(Group):
    def __eq__(self, other):
        return isinstance(other, Sequence) and self.tiles == other.tiles

    def __hash__(self):
        return hash(("sequence", tuple(self.tiles)))

    def __str__(self):
        return "sequence(%s, %s, %s)" % (self.tiles[0], self.tiles[1],
                                         self.tiles[2])
    def __repr__(self):
        return self.__str__()

    def __init__(self, head, closed=True):
        Group.__init__(self, head, closed)
        if len(self.tiles) == 1:
            self.tiles += [deepcopy(self.tiles[0]) for n in range(2)]
            self.tiles[1].number += 1
            self.tiles[2].number += 2

class Triplet(Group):
    def __eq__(self, other):
        return isinstance(other, Triplet) and self.tiles == other.tiles

    def __hash__(self):
        return hash(("triplet", tuple(self.tiles)))

    def __str__(self):
        return "triplet(%s, %s, %s)" % (self.tiles[0], self.tiles[1],
                                        self.tiles[2])
    def __repr__(self):
        return self.__str__()

    def __init__(self, head, closed=True):
        Group.__init__(self, head, closed)
        self.tiles += [deepcopy(self.tiles[0]) for n in range(2)]

class Quadruplet(Group):
    def __eq__(self, other):
        return isinstance(other, Quadruplet) and self.tiles == other.tiles

    def __hash__(self):
        return hash(("triplet", tuple(self.tiles)))

    def __str__(self):
        return "quadruplet(%s, %s, %s)" % (self.tiles[0], self.tiles[1],
                                           self.tiles[2], self.tiles[3])
    def __repr__(self):
        return self.__str__()

    def __init__(self, head, closed=True):
        Group.__init__(self, head, closed)
        self.tiles += [deepcopy(self.tiles[0]) for n in range(3)]
