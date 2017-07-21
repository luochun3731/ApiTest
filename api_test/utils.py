import hashlib
import json
import os
import random
import string

import yaml

from api_test.exception import ParamsError


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


def load_test_cases(test_cases_path):
    file_suffix = os.path.splitext(test_cases_path)[1]
    if file_suffix == '.json':
        return load_json_file(test_cases_path)
    elif file_suffix == '.yaml':
        return load_yaml_file(test_cases_path)
    else:
        raise ParamsError('incorrect test case file name!')


def parse_response(resp):
    return {
        'status_code': resp.status_code,
        'headers': resp.headers,
        'content': resp.content
    }

if __name__ == '__main__':
    # print(gen_random_string(8))
    print(load_yaml_file(r'I:\MyProject\ApiTest\test\data\demo.yaml'))
    print(type(load_yaml_file(r'I:\MyProject\ApiTest\test\data\demo.yaml')))
