def print_table(data):
    """
    The objective of the "print_table" function is to print a table of data in a formatted manner.
    The function takes a list of dictionaries as input and prints a table for each dictionary in the list.

    :param data: a list of dictionaries containing the data to be printed in a table format.
    :return: the function prints a formatted table for each dictionary in the "data" list.
    """

    for dictionary in data:
        # find the length of the longest key
        max_key_length = max([len(str(key)) for key in dictionary.keys()])

        # print the table headers
        print("{:<{}}\t{}".format("Key", max_key_length, "Value"))
        print("-" * (max_key_length + 10))

        # print the table rows
        for key, value in dictionary.items():
            print("{:<{}}\t{}".format(key, max_key_length, value))
        print("\n")