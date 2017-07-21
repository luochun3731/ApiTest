import os

import requests

from api_test import exception, utils
from test.test_base import TestBase


class TestUtils(TestBase):
    def test_load_json_file(self):
        file_name = os.path.join(os.getcwd(), 'test/data/demo.json')
        cases = utils.load_json_file(file_name)
        self.assertEqual(len(cases), 2)
        self.assertEqual('create user which does not exist', cases[0]['test']['name'])
        self.assertIn('headers', cases[0]['test']['request'])
        self.assertIn('url', cases[0]['test']['request'])
        self.assertIn('method', cases[0]['test']['request'])
        self.assertEqual('create user which existed', cases[1]['test']['name'])

    def test_load_yaml_file(self):
        file_name = os.path.join(os.getcwd(), 'test/data/demo.yaml')
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
        test_case_path = os.path.join(os.getcwd(), 'test/data/demo.json')
        cases = utils.load_test_cases(test_case_path)
        self.assertEqual(len(cases), 2)
        self.assertEqual('create user which does not exist', cases[0]['test']['name'])
        self.assertIn('headers', cases[0]['test']['request'])
        self.assertIn('url', cases[0]['test']['request'])
        self.assertIn('method', cases[0]['test']['request'])
        self.assertEqual('create user which existed', cases[1]['test']['name'])

    def test_load_yaml_cases(self):
        test_case_path = os.path.join(os.getcwd(), 'test/data/demo.yaml')
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

    def test_parse_response(self):
        url = "http://127.0.0.1:5000/api/users"
        resp = requests.get(url)
        parse_result = utils.parse_response(resp)
        self.assertIn('status_code', parse_result)
        self.assertIn('headers', parse_result)
        self.assertIn('content', parse_result)
