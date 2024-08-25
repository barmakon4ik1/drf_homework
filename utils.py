import json


def write_to_file(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f)
    except TypeError as e:
        raise e
    except IOError as e:
        raise e


def read_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise e
    except IOError as e:
        raise e

