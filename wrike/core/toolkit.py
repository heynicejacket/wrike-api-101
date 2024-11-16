import pandas as pd
import time


def dataframe_to_json(df, unflatten=False, sep='_', verbose=False):
    """
    Convert a Pandas DataFrame back to a JSON object. If the DataFrame was flattened, optionally unflatten the
    structure based on the separator used during flattening.

    :param df:                  df, required            DataFrame to be converted to JSON
    :param unflatten:           bool, optional          if True, reverse flattening and nest JSON structure
    :param sep:                 str, optional           separator used in flattened df
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    API response in JSON format
    """

    json_data = df.to_dict(orient='records')

    if unflatten:
        print('Unflattening JSON.') if verbose else None
        return [unflatten_json(record, sep=sep) for record in json_data]

    return json_data


def exclude_keys(data, keys_to_ignore):
    """
    Helper function to leave keys intact if they match ignore_keys. Other keys will be removed.

    :param data:                dict, required          input dict to be filtered
    :param keys_to_ignore:      list, required          list of keys to not remove from dict
    :return:                    dict                    output filtered dict
    """

    if isinstance(data, list):
        return [exclude_keys(item, keys_to_ignore) for item in data]

    if isinstance(data, dict):
        return {k: (v if k in keys_to_ignore else exclude_keys(v, keys_to_ignore)) for k, v in data.items()}

    return data


def flatten_json(data, parent_key='', sep='_', ignore_keys=None):
    """
    Helper function to recursively traverse a nested JSON object and flatten it, appending parent keys to child keys
    using the provided separator.

    idx is perhaps less than ideal in creating panda column headers, but is necessary to appropriately handle lists of
    dictionaries, so that:

        'customFields': [
            {'id': 'IEAVJOU5JUAAAACG', 'value': 'foo'},
            {'id': 'IEAVJOU5JUAAAACH', 'value': 'bar'}
        ]

    ...is returned as the following column headers:

        customFields_0_id, customFields_0_value, customFields_1_id, customFields_1_value

    If value is a simple list, the key-value pair is not converted and the value is passed as a list, so that this:

        [{'id': 'IEAAB3DEI5NBKJQW', 'accountId': 'IEAAB3DE', 'sharedIds': ['KUAFMCAH', 'KUALDPDC', 'KUAP3YOD']}, ...]

    ...is returned in as the following DataFrame:

        id                  accountId           sharedIds
        ------------------  ------------------  ----------------------------------------
        IEAAB3DEI5NBKJQW    IEAAB3DE            ['KUAFMCAH', 'KUALDPDC', 'KUAP3YOD']

    :param data:                dict, required          JSON object to be flattened
    :param parent_key:          str, optional           prefix for flattened keys
    :param sep:                 str, optional           separator for concatenating keys
    :param ignore_keys:         list, optional          list of keys to ignore for flattening
    :return:                    JSON                    flattened JSON object
    """

    flattened = {}
    ignore_keys = ignore_keys or []

    for key, value in data.items():
        new_key = f'{parent_key}{sep}{key}' if parent_key else key

        if key in ignore_keys:
            flattened[new_key] = value

        elif isinstance(value, dict):
            flattened.update(flatten_json(value, new_key, sep=sep, ignore_keys=ignore_keys))

        elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
            for idx, item in enumerate(value):
                flattened.update(flatten_json(item, parent_key=f'{new_key}{sep}{idx}', sep=sep, ignore_keys=ignore_keys))

        elif isinstance(value, list):
            flattened[new_key] = value

        else:
            flattened[new_key] = value

    return flattened


def get_all_ids(data, verbose=False):
    """
    Extracts the 'id' field at 0th level from every dict in the provided list.

    Given a list of dicts, containing at least the key 'id', as follows:

        [
            {'id': 'IEAAB3DEI5M4RE5R', 'accountId': 'IEAAB3DE', 'title': 'folder_a', ..., 'level': 0},
            {'id': 'IEAAB3DEI5M4RE6S', 'accountId': 'IEAAB3DE', 'title': 'folder_b', ..., 'level': 0},
            ...
        ]

    Returns a list as follows:

        ['IEAAB3DEI5M4RE5R', 'IEAAB3DEI5M4RE6S', ... 'IEAAB3DEID4K1F4R']

    :param data:                list, required          list of dicts
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    list                    all 'id' values as list
    """

    ids = [item['id'] for item in data if 'id' in item]
    print(ids) if verbose else None

    return ids


def get_ordinal_suffix(i):
    """
    Returns ordinal suffix ('st', 'nd', 'rd', 'th') for given integer.

    :param i:                   int, required           integer to determine suffix
    :return:                    str                     correct ordinal suffix
    """

    if 10 <= i % 100 <= 13:                                                 # handle numbers ending in 11, 12, 13
        return 'th'

    last_digit = i % 10                                                     # handle last digit cases
    if last_digit == 1:
        return 'st'
    elif last_digit == 2:
        return 'nd'
    elif last_digit == 3:
        return 'rd'
    else:
        return 'th'


def insert(d, keys, value):
    """
    Recursively insert value into the nested dictionary or list.

    :param d:                   dict or list, required  dict or list to insert value into
    :param keys:                list, required          list of keys or indices representing the path to value
    :param value:               any, required           value to be inserted
    """

    key = int(keys[0]) if keys[0].isdigit() else keys[0]

    if len(keys) == 1:
        if isinstance(key, int):                                            # list insertion
            while len(d) <= key:
                d.append(None)
            d[key] = value
        else:                                                               # dict insertion
            d[key] = value
    else:
        next_key_is_digit = keys[1].isdigit()

        if isinstance(key, int):                                            # if current key is int (list index)
            while len(d) <= key:
                d.append([] if next_key_is_digit else {})
            insert(d[key], keys[1:], value)
        else:                                                               # if current key is not int (dictionary key)
            d[key] = d.get(key, [] if next_key_is_digit else {})
            insert(d[key], keys[1:], value)


def is_dict_list(data):
    """
    Helper function to determine if the data is a list of dictionaries.

    :param data:                list, required          data to check if list of dicts
    :return:                    bool                    True if list of dicts, else False
    """

    return isinstance(data, list) and all(isinstance(i, dict) for i in data)


def json_to_dataframe(json_data, flatten=False, sep='_', ignore_keys=None, verbose=False):
    """
    Given a JSON object, converts into a pandas DataFrame.

    Optionally, this function flattens nested structures; this option should not be used if the dataframe will be used
    to create or update another space, folder, project, task, etc. of the same type, as this will cause errors.

    Given JSON as follows:

    {
        'id': 'IEAAB3DEI5M5NKRM',
        'title': 'Project Title',
        'customFields': [
            {
                'id': 'IEAVJOU5JUAAAACG',
                'value': 'updatedValue'
            }
        ]
    }

    ...an unflattened dataframe will return:

        id                      title               customFields
        ----------------------  ------------------  --------------------------------------------------------
        IEAAB3DEI5M5NKRM        Project Title       { 'id': 'IEAVJOU5JUAAAACG', 'value': 'updatedValue' }

    ...and a flattened dataframe will return:

        id                      title               customFields_id         customFields_value
        ----------------------  ------------------  ----------------------  --------------------------------
        IEAAB3DEI5M5NKRM        Project Title       IEAVJOU5JUAAAACG        updatedValue

    If value is a simple list, the key-value pair is not converted and the value is passed as a list, so that this:

        [{'id': 'IEAAB3DEI5NBKJQW', 'accountId': 'IEAAB3DE', 'sharedIds': ['KUAFMCAH', 'KUALDPDC', 'KUAP3YOD']}, ...]

    ...is returned in as the following DataFrame:

        id                  accountId           sharedIds
        ------------------  ------------------  ----------------------------------------
        IEAAB3DEI5NBKJQW    IEAAB3DE            ['KUAFMCAH', 'KUALDPDC', 'KUAP3YOD']

    :param json_data:           list or dict, required  JSON data to be converted to a DataFrame
    :param flatten:             bool, optional          if True, flatten nested structures
    :param sep:                 str, optional           separator for flattening keys; default is '_'
    :param ignore_keys:         list, optional          list of keys to ignore for flattening
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    df                      DataFrame from JSON
    """

    # convert to DataFrame and flatten data, optionally excluding specific keys from being flattened
    if flatten:
        if isinstance(json_data, list):
            flat_data = [flatten_json(data=item, sep=sep, verbose=verbose) for item in json_data]
        else:
            flat_data = [flatten_json(data=json_data, sep=sep, verbose=verbose)]
        return pd.DataFrame(flat_data)

    # convert to DataFrame without flattening
    else:
        if ignore_keys:
            json_data = exclude_keys(data=json_data, keys_to_ignore=ignore_keys, verbose=verbose)

        return pd.DataFrame(json_data)


def the_time_keeper(t=0.0, float_out=False):
    """
    This function provides the duration of a given task when called twice, once to initiate before task begins, and
    again, after task has completed, to return duration of task.

    Example usage is as follows:

        start_time = the_time_keeper()      # init with no value passed to t; time script begins
        # do stuff
        the_time_keeper(start_time)         # pass value to t; print duration of task

    Returned value is returned as follows:

        if t==0.0                           float value of the current time
        if t!=0.0 and float_out=True        task duration as float in seconds
        if t!=0.0 and float_out=False       task duration as formatted str

    :param t:                   float, optional     time previously returned by the Time Keeper
    :param float_out:           str, optional       if True, returns seconds as float; if False, returns as string
    :return:                    float or str        duration as seconds or formatted string
    """

    if t == 0.0:
        return time.time()
    else:
        tk = time.time() - t
        if float_out:
            return round(tk, 2)
        else:
            if tk < 60:
                tk = 'Duration: ' + str(round(tk, 2)) + ' seconds.'
            elif 60 < tk < 3600:
                tk = 'Duration: ' + str(round(tk / 60, 2)) + ' minutes.'
            else:
                tk = 'Duration: ' + str(round(tk / 60 / 60, 2)) + ' hours.'
            return tk


def unflatten_json(flat_dict, sep='_'):
    """
    Helper function to unflatten a dictionary, reversing the flattening done by _flatten_json.

    Handles cases where lists were flattened with indices (e.g., 'key_0', 'key_1') and restores them as lists.

    :param flat_dict:           dict, required          flat dict where nested keys are joined by a separator
    :param sep:                 str, optional           separator used to flatten keys
    :return:                    dict                    unflattened dict, with list structures restored
    """

    unflattened = {}
    for k, v in flat_dict.items():
        insert(unflattened, k.split(sep), v)

    return unflattened
