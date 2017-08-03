import os
import random

import requests

from api_test import exception, utils
from test.test_base import TestBase


class TestUtils(TestBase):
    def test_load_json_file(self):
        file_name = os.path.join(os.getcwd(), 'test/data/demo_with_no_auth.json')
        cases = utils.load_json_file(file_name)
        self.assertEqual(len(cases), 2)
        self.assertEqual('create user which does not exist', cases[0]['test']['name'])
        self.assertIn('headers', cases[0]['test']['request'])
        self.assertIn('url', cases[0]['test']['request'])
        self.assertIn('method', cases[0]['test']['request'])
        self.assertEqual('create user which existed', cases[1]['test']['name'])

    def test_load_yaml_file(self):
        file_name = os.path.join(os.getcwd(), 'test/data/demo_with_no_auth.yaml')
        cases = utils.load_yaml_file(file_name)
        self.assertEqual(len(cases), 2)
        self.assertEqual('create user which does not exist', cases[0]['test']['name'])
        self.assertIn('headers', cases[0]['test']['request'])
        self.assertIn('url', cases[0]['test']['request'])
        self.assertIn('method', cases[0]['test']['request'])
        self.assertEqual('create user which does exist', cases[1]['test']['name'])

    def test_load_cases_with_bad_path(self):
        test_case_path = os.path.join(os.getcwd(), 'test/data/demo')
        with self.assertRaises(exception.ParamsError):
            utils.load_test_cases(test_case_path)

    def test_load_json_cases(self):
        test_case_path = os.path.join(os.getcwd(), 'test/data/demo_with_no_auth.json')
        cases = utils.load_test_cases(test_case_path)
        self.assertEqual(len(cases), 2)
        self.assertEqual('create user which does not exist', cases[0]['test']['name'])
        self.assertIn('headers', cases[0]['test']['request'])
        self.assertIn('url', cases[0]['test']['request'])
        self.assertIn('method', cases[0]['test']['request'])
        self.assertEqual('create user which existed', cases[1]['test']['name'])

    def test_load_yaml_cases(self):
        test_case_path = os.path.join(os.getcwd(), 'test/data/demo_with_no_auth.yaml')
        cases = utils.load_test_cases(test_case_path)
        self.assertEqual(len(cases), 2)
        self.assertEqual('create user which does not exist', cases[0]['test']['name'])
        self.assertIn('headers', cases[0]['test']['request'])
        self.assertIn('url', cases[0]['test']['request'])
        self.assertIn('method', cases[0]['test']['request'])
        self.assertEqual('create user which does exist', cases[1]['test']['name'])

    def test_gen_random_string(self):
        random_string = utils.gen_random_string(6)
        self.assertIsInstance(random_string, str)
        self.assertEqual(6, len(random_string))

    def test_gen_md5_with_one_param(self):
        md5 = utils.gen_md5('test')
        self.assertEqual(32, len(md5))
        self.assertIsInstance(md5, str)

    def test_gen_md5_with_two_params(self):
        md5 = utils.gen_md5('param1', 'param2')
        self.assertEqual(32, len(md5))
        self.assertIsInstance(md5, str)

    def test_parse_response_json(self):
        url = "http://127.0.0.1:5000/api/users"
        resp = requests.get(url)
        parse_result = utils.parse_response(resp)
        self.assertIn('status_code', parse_result)
        self.assertIn('headers', parse_result)
        self.assertIn('body', parse_result)
        self.assertIn('Content-Type', parse_result['headers'])
        self.assertIn('Content-Length', parse_result['headers'])
        self.assertIn('success', parse_result['body'])

    def test_parse_response_text(self):
        url = "http://127.0.0.1:5000/"
        resp = requests.get(url)
        parse_result = utils.parse_response(resp)
        self.assertIn('status_code', parse_result)
        self.assertIn('headers', parse_result)
        self.assertIn('body', parse_result)
        self.assertIn('Content-Type', parse_result['headers'])
        self.assertIn('Content-Length', parse_result['headers'])
        self.assertTrue(str, type(parse_result['body']))

    def test_diff_response_status_code_equal(self):
        status_code = random.randint(200, 520)
        url = 'http://127.0.0.1:5000/status_code/%d/' % status_code
        resp = requests.get(url)
        exp_resp = {
            'status_code': status_code
        }
        diff_content = utils.diff_response(resp, exp_resp)
        self.assertFalse(diff_content)

    def test_diff_response_status_code_not_equal(self):
        status_code = random.randint(200, 520)
        url = 'http://127.0.0.1:5000/status_code/%d/' % status_code
        resp = requests.get(url)
        exp_resp = {
            'status_code': 512
        }
        diff_content = utils.diff_response(resp, exp_resp)
        print('diff_content: ', diff_content)
        self.assertIn('actual value', diff_content['status_code'])
        self.assertIn('expected value', diff_content['status_code'])
        self.assertEqual(diff_content['status_code']['actual value'], status_code)
        self.assertEqual(diff_content['status_code']['expected value'], 512)

    def test_diff_response_headers_equal(self):
        resp = requests.post(
            url='http://127.0.0.1:5000/custom_response/',
            json={
                'headers': {
                    'test01': 123,
                    'test02': 456
                }
            }
        )
        exp_resp_json = {
            'headers': {
                'test01': 123,
                'test02': '456'
            }
        }
        diff_content = utils.diff_response(resp, exp_resp_json)
        self.assertFalse(diff_content)

    def test_diff_response_headers_not_equal(self):
        resp = requests.post(
            url="http://127.0.0.1:5000/custom_response/",
            json={
                'headers': {
                    'test01': 123,
                    'test02': '456',
                    'test03': '789'
                }
            }
        )

        exp_resp_json = {
            'headers': {
                'test01': '123',
                'test02': '457',
                'test04': 890
            }
        }
        diff_content = utils.diff_response(resp, exp_resp_json)
        self.assertEqual(
            diff_content['headers'],
            {
                'test02': {'expected value': '457', 'actual value': '456'},
                'test04': {'expected value': 890, 'actual value': None}
            }
        )

    def test_diff_response_body_equal(self):
        resp = requests.post(
            url='http://127.0.0.1:5000/custom_response/',
            json={
                'body': {
                    'success': True,
                    'count': 10
                }
            }
        )

        exp_resp_json = {}
        diff_content = utils.diff_response(resp, exp_resp_json)
        self.assertFalse(diff_content)

        exp_resp_json = {
            'body': {
                'success': True,
                'count': '10'
            }
        }
        diff_content = utils.diff_response(resp, exp_resp_json)
        self.assertFalse(diff_content)

    def test_diff_response_body_not_equal_type_unmatch(self):
        resp = requests.post(
            url='http://127.0.0.1:5000/custom_response/',
            json={
                'body': {
                    'success': True,
                    'count': 10
                }
            }
        )

        exp_resp_json = {
            'body': "ok"
        }
        diff_content = utils.diff_response(resp, exp_resp_json)
        self.assertEqual(
            diff_content['body'],
            {
                'actual value': {'success': True, 'count': 10},
                'expected value': 'ok'
            }
        )

    def test_diff_response_body_not_equal_string_unmatch(self):
        resp = requests.post(
            url='http://127.0.0.1:5000/custom_response/',
            json={
                'body': "success"
            }
        )

        exp_resp_json = {
            'body': "ok"
        }
        diff_content = utils.diff_response(resp, exp_resp_json)
        self.assertEqual(
            diff_content['body'],
            {
                'actual value': 'success',
                'expected value': 'ok'
            }
        )

    def test_diff_response_body_not_equal_json_unmatch(self):
        resp = requests.post(
            url='http://127.0.0.1:5000/custom_response/',
            json={
                'body': {
                    'success': False
                }
            }
        )

        exp_resp_json = {
            'body': {
                'success': True,
                'count': 10
            }
        }
        diff_content = utils.diff_response(resp, exp_resp_json)
        self.assertEqual(
            diff_content['body'],
            {
                'success': {
                    'actual value': False,
                    'expected value': True
                },
                'count': {
                    'actual value': None,
                    'expected value': 10
                }
            }
        )
