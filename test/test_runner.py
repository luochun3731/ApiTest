import os

import requests

from api_test import runner
from api_test import utils
from test.test_base import TestBase


class TestRunner(TestBase):
    def setUp(self):
        self.runner = runner.Runner()
        self.clear_users()

    def clear_users(self):
        url = 'http://127.0.0.1:5000/api/users/'
        return requests.delete(url)

    def test_run_single_test_case_success(self):
        test_case = {
            "name": "create user which does not exist",
            "request": {
                "url": "http://127.0.0.1:5000/api/users/495/",
                "method": "POST",
                "headers": {
                    "content-type": "application/json"
                },
                "json": {
                    "name": "test01",
                    "password": "qwe123"
                }
            },
            "response": {
                "status_code": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": {
                    'success': True,
                    'msg': 'user created successfully!'
                }
            }
        }
        result, _ = self.runner.run_single_test_case(test_case)
        self.assertTrue(result)

    def test_run_single_test_case_fail(self):
        test_case = {
            "name": "create user which does not exist",
            "request": {
                "url": "http://127.0.0.1:5000/api/users/496/",
                "method": "POST",
                "headers": {
                    "content-type": "application/json"
                },
                "json": {
                    "name": "test02",
                    "password": "qwer1234"
                }
            },
            "response": {
                "status_code": 208,
                "headers": {
                    "Content-Type": "html/text"
                },
                "body": {
                    'success': False,
                    'msg': "user already existed."
                }
            }
        }
        result, diff_content = self.runner.run_single_test_case(test_case)
        self.assertFalse(result)
        self.assertEqual(
            diff_content['status_code'],
            {'expected value': 208, 'actual value': 200}
        )
        self.assertEqual(diff_content['headers'],
                         {'Content-Type': {'expected value': 'html/text', 'actual value': 'application/json'}}
                         )
        self.assertEqual(diff_content['body'],
                         {
                             'msg': {
                                 'expected value': 'user already existed.',
                                 'actual value': 'user created successfully!'
                             },
                             'success': {
                                 'expected value': False,
                                 'actual value': True
                             }
                         }
                         )

    def test_run_test_case_suite_success_json(self):
        test_case_file_path = os.path.join(os.getcwd(), 'test/data/demo.json')
        test_cases = [tcs['test'] for tcs in utils.load_test_cases(test_case_file_path)]
        print(test_cases)
        result = self.runner.run_test_case_suite(test_cases)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, [(True, {}), (True, {})])

    def test_run_test_case_suite_success_yaml(self):
        test_case_file_path = os.path.join(os.getcwd(), 'test/data/demo.yaml')
        test_cases = [tcs['test'] for tcs in utils.load_test_cases(test_case_file_path)]
        # print(test_cases)
        result = self.runner.run_test_case_suite(test_cases)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, [(True, {}), (True, {})])
