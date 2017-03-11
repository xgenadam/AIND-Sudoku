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
        potential_twin_dict = {cell: values[cell] for cell in unit if len(values[cell]) >= 2}
        values_cell_dict = {}
        for potential_twin_cell, potential_twin_values in potential_twin_dict.items():
            location_list = values_cell_dict.get(potential_twin_values, [])
            location_list.append(potential_twin_cell)
            values_cell_dict[potential_twin_values] = location_list

        for twin_values, twin_value_locations in values_cell_dict.items():
            if len(twin_value_locations) >= 2:
                # values_cell_dict.pop(twin_values)
                # print('twin values {}, locations {}'.format(twin_values, twin_value_locations))
                for peer in [cell for cell in unit if cell not in twin_value_locations]:
                    peer_values = values[peer]
                    for value in twin_values:
                        peer_values.replace(value, '')

                    values[peer] = peer_values

    return values

# def cross(A, B):
#     "Cross product of elements in A and elements in B."
#     pass

# def grid_values(grid):
#     """
#     Convert grid into a dict of {square: char} with '123456789' for empties.
#     Args:
#         grid(string) - A grid in string form.
#     Returns:
#         A grid in dictionary form
#             Keys: The boxes, e.g., 'A1'
#             Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
#     """
#     pass
#
# def display(values):
#     """
#     Display the values as a 2-D grid.
#     Args:
#         values(dict): The sudoku in dictionary form
#     """
#     pass

# def eliminate(values):
#     pass

# def only_choice(values):
#     pass

# def reduce_puzzle(values):
#     pass

# def search(values):
#     pass


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
