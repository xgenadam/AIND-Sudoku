from itertools import chain
from collections import Counter, OrderedDict

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]

box = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.


column_units = [cross(rows, c) for c in cols]
# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.


square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def display(values):
    """
    code snippet from udacity nanodegree
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def display_mini_grid(mini_grid_values_dict):
    s = []
    for r in rows:
        s = ''.join(mini_grid_values_dict[r+c].center(3)+('|' if c in '36' else '')
                      for c in cols if mini_grid_values_dict.get(r+c, False) and r+c in mini_grid_values_dict.keys())
        if r in map(lambda x: x[0], mini_grid_values_dict.keys()):
            print(s)
    return


def grid_values(serial_sudoku):
    return OrderedDict([(grid_location, grid_value)
                        for grid_location, grid_value
                        in zip(chain(*row_units), serial_sudoku)])


def print_sudoku(ordered_grid_dict):
    l = []
    for k, v in ordered_grid_dict:
        l.append(v)
        if len(l) == 9:
            print(' '.join(str(item) for item in l))
            l = []

    return


def serialize_grid(sudoku_dict):
    serial = []
    for r in rows:
        s = ''.join(sudoku_dict[r + c].center(3) + ('|' if c in '36' else '')
                    for c in cols if
                    sudoku_dict.get(r + c, False) and r + c in sudoku_dict.keys())
        if r in map(lambda x: x[0], sudoku_dict.keys()):
            serial.append(s)

    return ''.join(serial)


def potential_grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """

    values_list = {}
    for grid_value, cell in zip(grid, chain(*row_units)):
        cell_value = grid_value if grid_value != '.' else ''.join(str(item) for item in range(1, 10))
        values_list[cell] = cell_value

    return values_list


def eliminate(values):
    """

    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.1

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = {k:v for k, v in values.items() if len(v) == 1}
    for location, value in solved_values.items():
        col_peers = [location[0] + str(x) for x in cols if location[0] + str(x) != location]
        row_peers = [str(x) + location[1] for x in rows if str(x) + location[1] != location]
        for grid in square_units:
            if location in grid:
                grid_peers = grid.copy()
                grid_peers.pop(grid_peers.index(location))
                break

        peers = set(col_peers) | set(row_peers) | set(grid_peers)

        # print(peers)

        for peer in peers:
            if peer not in solved_values:
                values[peer] = values[peer].replace(value, '')

    return values


def contains_clashes(values):
    for unit in unitlist:
        try:
            solved_values = [values[cell] for cell in unit if len(values[cell]) == 1]
        except Exception as e:
            import pdb; pdb.set_trace()
            raise e
        for num_occurence in Counter(solved_values).values():
            if num_occurence > 1:
                return True

    return False


def sudoku_solved(values):
    return all(len(cell_val) == 1 for cell_val in values.values())


def get_mini_grid_locations(location):
    for grid in square_units:
        if location in grid:
            return grid


def get_mini_grid_dict(location, values):
    mini_grid_locations = get_mini_grid_locations(location)

    return {other_location: values[other_location] for other_location in mini_grid_locations}


def get_unsolved_values(values):
    return {k: v for k, v in values.items() if len(v) > 1}


def get_peer_locations(location):
    col_peers = [location[0] + str(x) for x in cols if location[0] + str(x) != location]
    row_peers = [str(x) + location[1] for x in rows if str(x) + location[1] != location]
    for grid in square_units:
        if location in grid:
            grid_peers = [x for x in grid if x != location]
            break

    for l in chain(col_peers, row_peers, grid_peers):
        yield l


def location_values_filter(location, vals):
    if len(vals) > 1:
        return True

    return False


def get_location_with_least_values(values):
    sorted_values = sorted(values.items(), key=lambda x: len(x[1]))
    ordered_values = filter(lambda location_val: location_values_filter(location_val[0], location_val[1]),
                            sorted_values)

    return next(ordered_values, (None, None))
