import hashlib
import json
import random
import string

import yaml


def gen_random_string(str_len):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(str_len)])


def gen_md5(*str_args):
    return hashlib.md5(''.join(str_args).encode('utf-8')).hexdigest()


def load_json_file(json_file):
    with open(json_file) as file:
        return json.load(file)


def load_yaml_file(yaml_file):
    with open(yaml_file) as file:
        return yaml.load(file)


if __name__ == '__main__':
    # print(gen_random_string(8))
    print(load_yaml_file(r'I:\MyProject\ApiTest\test\data\demo.yaml'))
    print(type(load_yaml_file(r'I:\MyProject\ApiTest\test\data\demo.yaml')))
