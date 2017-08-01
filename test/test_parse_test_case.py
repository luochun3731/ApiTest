import unittest

from api_test import exception
from api_test.parse_test_case import TestCaseParser


class TestParseTestCase(unittest.TestCase):
    def setUp(self):
        self.variable_binds = {
            'uid': '888',
            'random': '5Bq3jZk4',
            'authorization': 'fd2ac95bc96d37bab4ad897c7fc44740',
            'json': {
                'name': 'test001',
                'password': 'qwe123'
            },
            'expected_status_code': 200,
            'expected_success': True
        }

        self.test_case_parser = TestCaseParser(self.variable_binds)

    def test_parse_test_case_template(self):
        test_case = {
            "request": {
                "url": "http://127.0.0.1:5000/api/users/${uid}/",
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json",
                    "authorization": "${authorization}",
                    "random": "${random}"
                },
                "body": "${json}"
            },
            "response": {
                "status_code": "${expected_status_code}",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": {
                    "success": "${expected_success}",
                    "msg": "user created successfully."
                }
            }
        }

        parsed_test_case = self.test_case_parser.parse(test_case)

        self.assertEqual(parsed_test_case['request']['url'],
                         'http://127.0.0.1:5000/api/users/%s/' % self.variable_binds['uid'])
        self.assertEqual(parsed_test_case['request']['headers']['authorization'], self.variable_binds['authorization'])
        self.assertEqual(parsed_test_case['request']['headers']['random'], self.variable_binds['random'])
        self.assertEqual(parsed_test_case['request']['body'], self.variable_binds['json'])
        self.assertEqual(parsed_test_case['response']['status_code'], self.variable_binds['expected_status_code'])
        self.assertEqual(parsed_test_case['response']['body']['success'], self.variable_binds['expected_success'])

    def test_parse_test_case_template_miss_bind_variable(self):
        test_case = {
            "request": {
                "url": "http://127.0.0.1:5000/api/users/${uid}/",
                "method": "${method}"
            }
        }
        with self.assertRaises(exception.ParamsError):
            self.test_case_parser.parse(test_case)

    def test_parse_test_case_with_new_variable_binds(self):
        test_case = {
            "request": {
                "url": "http://127.0.0.1:5000/api/users/${uid}/",
                "method": "${method}"
            }
        }
        new_variable_binds = {
            "method": "GET"
        }
        parsed_test_case = self.test_case_parser.parse(test_case, new_variable_binds)
        self.assertIn('method', self.test_case_parser.variable_binds)
        self.assertEqual(parsed_test_case['request']['method'],
                         new_variable_binds['method'])
