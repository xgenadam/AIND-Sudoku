from utils import *
from reduce import reduce_puzzle as reduce
from only_choice import only_choice
from tree_search import search

assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don11't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        unsolved_values_dict = {cell: values[cell] for cell in unit if len(values[cell]) == 2}

        twin_values = set()

        values_cell_dict = {}

        for idx_0, (location, vals) in enumerate(unsolved_values_dict.items()):
            combs = [[tuple(sorted([val_1, val_2])) for val_2 in vals[idx_1:] if val_1 != val_2] for idx_1, val_1 in enumerate(vals)]
            current_cell_twin_values = set(chain(*combs))
            twin_values.update(current_cell_twin_values)

            for twins in current_cell_twin_values:
                location_list = values_cell_dict.get(twins, [])
                location_list.append(location)
                values_cell_dict[twins] = location_list

        # import pdb; pdb.set_trace()

        for twin_values, twin_value_locations in values_cell_dict.items():
            if len(twin_value_locations) >= 2:
                # print(twin_values, twin_value_locations)
                for peer in [cell for cell in unit if cell not in twin_value_locations]:
                    peer_values = values[peer]
                    if set(twin_values) & set(peer_values):
                        for value in twin_values:
                            peer_values = peer_values.replace(value, '')
                        values[peer] = peer_values

    return values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    pass

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
