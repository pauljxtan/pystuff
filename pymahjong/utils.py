from tile import (ManTile, PinTile, SouTile, WindTile, TILE_TYPES,
                  NUMBERED_TILE_TYPES, Pair, Sequence, Triplet, Quadruplet)

ALL_SEQUENCES = [tuple([tile_type(rank + i) for i in range(3)])
                 for rank in range(1, 8)
                 for tile_type in NUMBERED_TILE_TYPES]

ALL_SEQUENCE_HEADS = [sequence[:2] for sequence in ALL_SEQUENCES]

def are_all_equal(tiles):
    """
    Checks if all tiles are the same.
    """
    return len(set(tiles)) <= 1

def is_pair(tiles):
    """
    Checks if the tiles form a pair.
    """
    return len(tiles) == 2 and tiles[0] == tiles[1]

def is_sequence(tiles):
    """
    Checks if the tiles form a sequence.
    TODO: sort here later when using Tile objects
    """
    return tuple(tiles) in ALL_SEQUENCES

def is_triplet(tiles):
    """
    Checks if the tiles form a triplet.
    """
    return len(tiles) == 3 and are_all_equal(tiles)

def is_quad(tiles):
    """
    Checks if the tile form a quad(ruplet).
    """
    return len(tiles) == 4 and are_all_equal(tiles)

def is_sequence_or_triplet(tiles):
    """
    Checks if the tiles form a sequence or triplet.
    """
    return is_sequence(tiles) or is_triplet(tiles)

def is_sequence_head(tiles):
    """
    Checks if the tiles are the first two in a sequence.
    """
    return tuple(tiles) in ALL_SEQUENCE_HEADS

def is_triplet_head(tiles):
    """
    Checks if the tiles are the first two in a triplet.
    """
    return is_pair(tiles)

def is_sequence_or_triplet_head(tiles):
    """
    Checks if the tiles are the first two in a sequence or triplet.
    """
    return is_sequence_head(tiles) or is_triplet_head(tiles)

def get_sequence_and_triplet_indices(tiles):
    """
    Returns the three tile indices in each sequence and triplet.
    """
    groups = {}
    n_tiles = len(tiles)

    for i in range(n_tiles - 2):
        for j in range(i + 1, n_tiles - 1):
            if is_sequence_or_triplet_head((tiles[i], tiles[j])):
                for k in range(j + 1, n_tiles):
                    group_indices = i, j, k
                    group = [tiles[n] for n in group_indices]
                    if is_sequence_or_triplet(group):
                        groups[tuple(group)] = group_indices

    return sorted(groups.values())

def flatten_groups(groups):
    return [tile for group in groups for tile in group.tiles]

def group_concealed_tiles(tiles):
    """
    Returns all legal groupings for the given concealed tiles, except for
    closed kans (since they must be declared anyway). Does not account for
    chitoitsu or kokushi musou hands; see group_chitoi() and group_kokushi().
    """
    tiles.sort()

    if len(tiles) == 0:
        return [[]]

    #f len(tiles) % 3 == 1:
    #   return []

    types = map(type, tiles)
    type_counts = [types.count(ttype) for ttype in TILE_TYPES]
    if 1 in type_counts:
        return []

    # Every type must be a multiple of 3 except the one containing the pair
    type_counts_not_multiple_of_3 = filter(lambda x: x % 3 != 0, type_counts)
    if len(type_counts_not_multiple_of_3) > 1:
        return []
    if (len(type_counts_not_multiple_of_3) == 1
        and type_counts_not_multiple_of_3[0] % 3 != 2):
        return []

    if len(tiles) == 2:
        if is_pair(tiles):
            # Need to use tuple here for hashability
            return [[tuple(tiles)]]
        return []

    # Using set here to eliminate duplicates
    hands = set()
    for indices in get_sequence_and_triplet_indices(tiles):
        group = tuple([tiles[i] for i in indices])
        remaining = [tile for i, tile in enumerate(tiles) if i not in indices]
        for remaining_groups in group_concealed_tiles(remaining):
            groups = sorted([group] + remaining_groups)
            hands.add(tuple(groups))

    return map(list, hands)

def group_concealed_tiles_and_convert(tiles):
    return convert_groupings(group_concealed_tiles(tiles))

def convert_groupings(tile_groups):
    """
    Converts tile groupings to Group objects.
    """
    return [map(convert_group, tile_group) for tile_group in tile_groups]

def convert_group(tiles):
    """
    Converts a tile group to a Group object.
    """
    if is_pair(group):
        return Pair(group[0])
    elif is_sequence(group):
        return Sequence(group[0])
    elif is_triplet(group):
        return Triplet(group[0])
    elif is_quadruplet(group):
        return Quadruplet(group)[0]
    return None

def all_same_suit(groups):
    return all([type(group.tiles[0]) == type(groups[0].tiles[0])
                for group in groups[1:]])

def get_sequences(groups):
    return filter(lambda g: isinstance(g, Sequence), groups)

def get_triplets(groups):
    return filter(lambda g: isinstance(g, Triplet), groups)

def get_quadruplets(groups):
    return filter(lambda g: isinstance(g, Quadruplet), groups)

def get_plets(groups):
    return get_triplets(groups) + get_quadruplets(groups)

def get_suit_counts_groups(groups):
    group_types = [group.ttype for group in groups]
    return {ttype: group_types.count(ttype) for ttype in TILE_TYPES[:3]}

def get_type_counts_groups(groups):
    group_types = [group.ttype for group in groups]
    return {ttype: group_types.count(ttype) for ttype in TILE_TYPES}

if __name__ == '__main__':
    print get_type_counts_groups(
        [Sequence(ManTile(1)), Triplet(PinTile(5)), Sequence(PinTile(6)),
         Quadruplet(WindTile('east')), Pair(WindTile('south'))])
