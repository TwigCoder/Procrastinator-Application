# Imports
import csv

# Define a function to pull data from a CSV file.
def pull_csv_data(file_name, desc_loc, item_desc, item_loc):
    """Pulls data from a csv file.

    Args:
        file_name (str): Name of the file with the extension (must be a csv file).
        desc_loc (int): Place on line where the item description is located; starts at 0.
        item_desc (str): Description of the item.
        item_loc (int): Location of the item itself.

    Returns:
        str: Value that you seek. Remember to convert to an int, etc. if needed.
    """

    # Placeholder value.
    value = 'PLACEHOLDER'

    #  Open the CSV file.
    with open(file_name, mode='r') as f:

        # Read the CSV file.
        csvFile = csv.reader(f)

        # Find the content in the CSV file.
        for lines in csvFile:
            if lines[desc_loc] == item_desc:
                value = lines[item_loc]

    # Return the value.
    return value


# Define a function to rewrite a CSV file.
def rewrite_csv_data(file_name, item_list, separator):
    """Rewrite the CSV file with the new data on one line, separated with semicolons.

    Args:
        file_name (str): Name of the CSV file.
        item_list (list): List of items that should be printed separately.
        separator (str): The separator to use in the CSV file.
    """

    # Check the file_name variable.
    if file_name[-4::] != '.csv':
        file_name = file_name + '.csv'

    # Read the CSV file.
    f = open(file_name, "r+")
    lines = f.readlines()

    # Ensure the file is not empty before deleting lines.
    if len(lines) >= 1:
        lines.pop()

    # Rewrite the CSV file with all the required data.
    f = open(file_name, "w+")
    lines = [f"{item}{separator}" for item in item_list]
    f.writelines(lines)

    # Repeat once again.
    f = open(file_name, "w+")
    lines = [f"{item}{separator}" for item in item_list]
    f.writelines(lines)
