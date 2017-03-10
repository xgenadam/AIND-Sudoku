from reduce import reduce_puzzle
from utils import (contains_clashes,
                   get_location_with_least_values,
                   serialize_grid,
                   sudoku_solved)


def search(values, already_searched=None):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    if already_searched is None:
        already_searched = set()

    serial_grid = serialize_grid(values)

    if serial_grid in already_searched:
        return None

    already_searched = already_searched | set([serial_grid],)

    values = reduce_puzzle(values)
    if values is False:
        return False

    if sudoku_solved(values):
        return values

    cell, cell_values = get_location_with_least_values(values)

    # Now use recursion to solve each one of the resulting sudokus,
    # and if one returns a value (not False), return that answer!
    for potential_val in cell_values:
        new_values = values.copy()
        new_values[cell] = potential_val

        attempt = search(new_values, already_searched)
        if attempt and not contains_clashes(attempt):
            return attempt
        else:
            continue
