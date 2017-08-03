import os

import requests

from api_test import runner
from api_test import utils
from test.test_base import TestBase


class TestRunnerWithAuthentication(TestBase):
    authentication = True

    def setUp(self):
        self.runner = runner.Runner()
        self.clear_users()

    def clear_users(self):
        url = 'http://127.0.0.1:5000/api/users/'
        return requests.delete(url, headers=self.build_headers())

    def test_run_single_test_case_json(self):
        test_case_file = os.path.join(os.getcwd(), 'test/data/demo_with_auth.json')
        test_cases = utils.load_test_cases(test_case_file)
        result, _ = self.runner.run_test(test_cases[0]['test'])
        self.assertTrue(result)

    def test_run_single_test_case_yaml(self):
        test_case_file = os.path.join(os.getcwd(), 'test/data/demo_with_auth.yaml')
        test_cases = utils.load_test_cases(test_case_file)
        result, _ = self.runner.run_test(test_cases[0]['test'])
        self.assertTrue(result)

    def test_run_test_case_suite_success_json(self):
        test_case_file_path = os.path.join(os.getcwd(), 'test/data/demo_with_auth.json')
        test_cases = utils.load_test_cases(test_case_file_path)
        print(test_cases)
        results = self.runner.run_test_case_suite(test_cases)
        self.assertEqual(len(results), 2)
        self.assertEqual(results, [(True, {}), (True, {})])

    def test_run_test_case_suite_success_yaml(self):
        test_case_file_path = os.path.join(os.getcwd(), 'test/data/demo_with_auth.yaml')
        test_cases = utils.load_test_cases(test_case_file_path)
        print(test_cases)
        results = self.runner.run_test_case_suite(test_cases)
        self.assertEqual(len(results), 2)
        self.assertEqual(results, [(True, {}), (True, {})])
