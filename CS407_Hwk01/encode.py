from itertools import groupby


def encode(input_string):
    encoded_string = ""
    for group, group_characters in groupby(iter(input_string)):
        encoded_string += group[0] + str(len(list(group_characters)))
    if len(encoded_string) < len(input_string):
        return encoded_string
    else:
        return input_string
