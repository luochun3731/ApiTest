import hashlib
import json
import os
import random
import string

import yaml

from api_test.exception import ParamsError


def handle_req_data(data):

    if isinstance(data, bytes):
        data = data.decode('utf-8')

    if not data:
        return data

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except ValueError:
            pass
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    return data


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
    try:
        resp_body = resp.json()
    except json.decoder.JSONDecodeError:
        resp_body = resp.text
    return {
        'status_code': resp.status_code,
        'headers': resp.headers,
        'body': resp_body
    }


def diff_json(actual_json, exp_json):
    diff_json_content = {}
    for key, exp_value in exp_json.items():
        value = actual_json.get(key, None)
        if str(value) != str(exp_value):
            diff_json_content[key] = {
                'actual value': value,
                'expected value': exp_value
            }
    return diff_json_content


def diff_response(resp, exp_resp_json):
    diff_content = {}
    resp_info = parse_response(resp)

    exp_status_code = exp_resp_json.get('status_code', 200)
    if resp_info['status_code'] != int(exp_status_code):
        diff_content['status_code'] = {
            'actual value': resp_info['status_code'],
            'expected value': exp_status_code
        }

    exp_headers = exp_resp_json.get('headers', {})
    diff_headers = diff_json(resp_info['headers'], exp_headers)
    if diff_headers:
        diff_content['headers'] = diff_headers

    exp_body = exp_resp_json.get('body', None)
    if exp_body is None:
        diff_body = {}
    elif type(exp_body) != type(resp_info['body']):
        diff_body = {
            'actual value': resp_info['body'],
            'expected value': exp_body
        }
    elif isinstance(exp_body, str):
        if exp_body != resp_info['body']:
            diff_body = {
                'actual value': resp_info['body'],
                'expected value': exp_body
            }
    elif isinstance(exp_body, dict):
        diff_body = diff_json(resp_info['body'], exp_body)

    if diff_body:
        diff_content['body'] = diff_body

    return diff_content


if __name__ == '__main__':
    print(gen_md5('debugtalk', handle_req_data({'name': 'user1', 'password': '123456'}), 'A2dEx'))
    print(load_yaml_file(r'I:\MyProject\ApiTest\test\data\demo.yaml'))
    print(type(load_yaml_file(r'I:\MyProject\ApiTest\test\data\demo.yaml')))
