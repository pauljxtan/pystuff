from tile import (NumberedTile, ManTile, PinTile, SouTile, WindTile,
                  DragonTile, TERMINALS, HONOURS, WIND_TILES, DRAGONS,
                  NUMBERS, Sequence, Pair, Triplet)
from utils import (flatten_groups, group_concealed_tiles_and_convert,
                   get_sequences, get_triplets, get_quadruplets, get_plets,
                   get_suit_counts_groups)

#### Yaku

def is_tanyao(groups):
    """
    Returns True if the hand satisfies tanyao.
    """
    tiles = flatten_groups(groups)
    return all([isinstance(tile, NumberedTile) and tile.number in range(2, 9)
                for tile in tiles])

def is_pinfu(groups, winning_tile):
    if get_plets(groups):
        return False
    return # TODO: get wait type

def is_iipeikou(groups):
    sequences = get_sequences(groups)
    return (not is_ryanpeikou(groups) and
            any([sequences.count(sequence) == 2 for sequence in sequences]))

def is_yakuhai(groups, prevailing_wind, player_wind):
    """
    TODO: need to count multiple yakuhai
    """
    plets = get_plets(groups)
    valid_honours = ((WindTile(prevailing_wind), WindTile(player_wind))
                     + HONOURS[4:])
    return sum([plet.tiles[0] in valid_honours for plet in get_plets(groups)]) >= 1

def is_chanta(groups):
    return all([any([tile in group.tiles for tile in TERMINALS + HONOURS])
                for group in groups])

def is_sanshoku_doujun(groups):
    sequences = get_sequences(groups)
    if len(sequences) < 3:
        return False
    suit_counts = get_suit_counts_groups(sequences)
    if 3 in suit_counts or 4 in suit_counts:
        return False
    heads = [sequence.tiles[0] for sequence in sequences]
    return # TODO

def is_toitoi(groups):
    return len(get_plets(groups)) == 4

def is_sanankou(groups):
    plets = get_plets(groups)
    if len(plets) < 3:
        return False
    return sum([plet.closed for plet in plets]) == 3

def is_sanshoku_doukou(groups):
    plets = get_plets(groups)
    if len(plets) < 3:
        return False
    numbers = [plet.tiles[0].number for plet in plets]
    return any([numbers.count(number) == 3 for number in NUMBERS])

def is_sankantsu(groups):
    return len(get_quadruplets(groups)) == 3

def is_chitoi(tiles):
    """
    Returns True if the hand satisfies chitoitsu.
    """
    unique_tiles = set(tiles)
    return (len(unique_tiles) == 7 and
            all([tiles.count(tile) == 2 for tile in unique_tiles]))

def is_honroutou(groups):
    return

def is_shousangen(groups):
    if len(get_triplets(groups)) < 2:
        return False
    return (any([Pair(dragon) in groups for dragon in DRAGONS]) and
            sum([Triplet(dragon) in groups for dragon in DRAGONS]) == 2)

def is_ittsu(groups):
    sequences = get_sequences(groups)
    if len(sequences) < 3:
        return False
    suit_counts = get_suit_counts_groups(sequences)
    if not (3 in suit_counts.values() or 4 in suit_counts.values()):
        return False
    suit = [suit for suit, count in suit_counts.iteritems() if count >= 3][0]
    return (Sequence(suit(1)) in groups and Sequence(suit(4)) in groups 
            and Sequence(suit(7)) in groups)
    
def is_ryanpeikou(groups):
    """
    Note: Chitoitsu is implicitly excluded since it is checked as individual
          tiles instead of groups; see is_chitoi().
    """
    sequences = get_sequences(groups)
    if len(sequences) < 4:
        return False
    return sum([sequences.count(sequence) == 2
                for sequence in set(sequences)]) == 2

def is_honitsu(groups):
    return

def is_junchan(groups):
    return

def is_chinitsu(groups):
    return

#### Yakuman

def is_kokushi(tiles):
    """
    Returns True if the hand satisfies kokushi musou.
    """
    return set(tiles) == set(TERMINALS) | set(HONOURS)

#### Info

class YakuInfo(object):
    def __init__(self, name, han_closed, han_open, func):
        self.name = name
        self.han_closed = han_closed
        self.han_open = han_open
        self.func = func

# TODO: separate by han values?
YAKU_INFO = {
    # 1 han
    'rch': YakuInfo("Riichi", 1, 0, None),
    'ipp': YakuInfo("Ippatsu", 1, 0, None),
    'smo': YakuInfo("Menzenchin tsumohou", 1, 0, None),
    'pfu': YakuInfo("pinfu", 1, 0, is_pinfu),
    'ipk': YakuInfo("Iipeikou", 1, 0, is_iipeikou),
    'hai': YakuInfo("Haitei raoyue", 1, 1, None),
    'hou': YakuInfo("Houtei raoyui", 1, 1, None),
    'rin': YakuInfo("Rinshan kaihou", 1, 1, None),
    'chk': YakuInfo("Chankan", 1, 1, None),
    'tan': YakuInfo("Tanyao", 1, 1, is_tanyao),
    'yak': YakuInfo("Yakuhai", 1, 1, is_yakuhai),
    
    # 2 han
    'dri': YakuInfo("Double riichi", 2, 0, None),
    'cha': YakuInfo("Honchantaiyaochuu", 2, 1, is_chanta),
    'sdj': YakuInfo("Sanshoku doujun", 2, 1, is_sanshoku_doujun),
    'itt': YakuInfo("Ikkitsuukan", 2, 1, is_ittsu),
    'toi': YakuInfo("Toitoihou", 2, 2, is_toitoi),
    'sna': YakuInfo("Sanankou", 2, 2, is_sanankou),
    'sdo': YakuInfo("Sanshoku doukou", 2, 2, is_sanshoku_doukou),
    'snk': YakuInfo("Sankantsu", 2, 2, is_sankantsu),
    'chi': YakuInfo("Chitoitsu", 2, 0, is_chitoi),
    'hro': YakuInfo("Honroutou", 2, 2, is_honroutou),
    'ssg': YakuInfo("Shousangen", 2, 2, is_shousangen),

    # 3 han
    'hon': YakuInfo("Honitsu", 3, 2, is_honitsu),
    'jun': YakuInfo("Junchantaiyaochuu", 3, 2, is_junchan),
    'rpk': YakuInfo("Ryanpeikou", 3, 0, is_ryanpeikou),

    # 6 han
    'chn': YakuInfo("Chinitsu", 6, 5, is_chinitsu)
}

YAKUMAN_INFO = {}
