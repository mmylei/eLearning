import json_wrapper


def read(file_name):
    with open(file_name) as infile:
        for line in infile:
            yield json_wrapper.loads(line)
