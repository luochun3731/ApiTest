import os
import unittest

from api_test import utils
from api_test.context import Context


class TestContext(unittest.TestCase):
    def setUp(self):
        self.context = Context()
        test_case_file = os.path.join(os.getcwd(), 'test/data/demo_binds.yaml')
        self.test_cases = utils.load_test_cases(test_case_file)

    def test_context_variable_string(self):
        # json format
        test_case_01 = {
            "variable_binds": [
                {"TOKEN": "LKSDJFLKDS"}
            ]
        }
        # yaml format
        test_case_02 = self.test_cases[0]

        for test_case in [test_case_01, test_case_02]:
            variable_binds = test_case['variable_binds']
            self.context.bind_variables(variable_binds)
            context_variables = self.context.variables
            self.assertIn('TOKEN', context_variables)
            self.assertEqual(context_variables['TOKEN'], 'LKSDJFLKDS')

    def test_context_variable_list(self):
        test_case_01 = {
            "variable_binds": [
                {"var": [1, 2, 3]}
            ]
        }
        test_case_02 = self.test_cases[1]
        for test_case in [test_case_01, test_case_02]:
            variable_binds = test_case['variable_binds']
            self.context.bind_variables(variable_binds)
            context_variables = self.context.variables
            self.assertIn('var', context_variables)
            self.assertEqual(context_variables['var'], [1, 2, 3])

    def test_context_variable_json(self):
        test_case_01 = {
            "variable_binds": [
                {"data": {'name': 'user', 'password': 'test'}}
            ]
        }
        test_case_02 = self.test_cases[2]
        for test_case in [test_case_01, test_case_02]:
            variable_binds = test_case['variable_binds']
            self.context.bind_variables(variable_binds)
            context_variables = self.context.variables
            self.assertIn('data', context_variables)
            self.assertEqual(context_variables['data'],
                             {'name': 'user', 'password': 'test'}
                             )

    def test_context_variable_variable(self):
        test_case_01 = {
            "variable_binds": [
                {"GLOBAL_TOKEN": "test"},
                {"token": "$GLOBAL_TOKEN"}
            ]
        }
        test_case_02 = self.test_cases[3]
        for test_case in [test_case_01, test_case_02]:
            variable_binds = test_case['variable_binds']
            self.context.bind_variables(variable_binds)
            context_variable = self.context.variables
            self.assertIn('GLOBAL_TOKEN', context_variable)
            self.assertEqual(context_variable['GLOBAL_TOKEN'], 'test')

    def test_context_variable_function_lambda(self):
        test_case_01 = {
            "function_binds": {
                "add_one": lambda x: x + 1,
                "add_two_nums": lambda x, y: x + y
            },
            "variable_binds": [
                {"add1": {"func": "add_one", "args": [2]}},
                {"sum2nums": {"func": "add_two_nums", "args": [2, 3]}}
            ]
        }
        test_case_02 = self.test_cases[4]
        for test_case in [test_case_01, test_case_02]:
            function_binds = test_case.get('function_binds', {})
            self.context.bind_functions(function_binds)
            variable_binds = test_case['variable_binds']
            self.context.bind_variables(variable_binds)
            context_variables = self.context.variables
            self.assertIn("add1", context_variables)
            self.assertEqual(context_variables["add1"], 3)
            self.assertIn("sum2nums", context_variables)
            self.assertEqual(context_variables["sum2nums"], 5)

    def test_context_variable_function_lambda_with_import(self):
        test_case_01 = {
            "requires": ["random", "string", "hashlib"],
            "function_binds": {
                "gen_random_string": "lambda str_len: ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(str_len))",
                "gen_md5": "lambda *str_args: hashlib.md5(''.join(str_args).encode('utf-8')).hexdigest()"
            },
            "variable_binds": [
                {"TOKEN": "test"},
                {"random": {"func": "gen_random_string", "args": [5]}},
                {"data": "{'name': 'user', 'password': 'test'}"},
                {"md5": {"func": "gen_md5", "args": ["$TOKEN", "$data", "$random"]}}
            ]
        }
        test_case_02 = self.test_cases[5]
        for test_case in [test_case_01, test_case_02]:
            requires = test_case.get('requires', [])
            self.context.import_required_modules(requires)

            function_binds = test_case.get('function_binds', {})
            self.context.bind_functions(function_binds)

            variable_binds = test_case['variable_binds']
            self.context.bind_variables(variable_binds)

            context_variables = self.context.variables
            self.assertIn("random", context_variables)
            self.assertIsInstance(context_variables["random"], str)
            self.assertEqual(len(context_variables["random"]), 5)
            self.assertIn("md5", context_variables)
            self.assertEqual(len(context_variables["md5"]), 32)
