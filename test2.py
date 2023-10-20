
def resort_key(some_dict):
    """
    resort the dict (keys: str), if key is missing, assign following keys to it
    e.g {'1': 1, '3': 3, '4': 4, '5': 5} -> {'1': 1, '2': 3, '3': 4, '4': 5}

    :param some_dict:
    :return:
    """
    # get missing key
    keys = some_dict.keys()
    mi_ma = set(range(int(min(keys)), int(max(keys)) + 1))
    missing_key = list(mi_ma - mi_ma.intersection(set([int(key) for key in keys])))
    # sort again
    if not missing_key and min(keys) != '1':

        return dict(sorted(some_dict.items()))
    else:
        missing_key = '0' if min(keys) == '1' else missing_key[0]
        next_key, last_key = int(missing_key) + 1, max([int(key) for key in keys])
        for key in  range(next_key, last_key + 1):
            some_dict[str(key-1)] = some_dict[str(key)]
        del some_dict[str(key)]

        return dict(sorted(some_dict.items()))

some_dict = {'1': 1}
print(len(some_dict))