from utils import *


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form aft13456er filling in only choices.
    """
    for unit in unitlist:

        for cell in unit:
            unit_dict = {cell: values[cell] for cell in unit}
            unsolved_values = unit_dict
            if cell not in unsolved_values:
                continue
            num_occurences = Counter(chain(*unsolved_values.values()))
            single_occurences = [val for val, occurence in num_occurences.items() if occurence == 1]
            if len(single_occurences) == 0:
                continue

            cell_vals = values[cell]
            for val in single_occurences:
                if val in cell_vals:
                    values[cell] = val
                    break

    return values
