import requests

from api_test import exception
from api_test import utils
from api_test.context import Context
from api_test.parse_test_case import TestCaseParser


class Runner:
    def __init__(self):
        self.client = requests.Session()
        self.context = Context()
        self.test_case_parser = TestCaseParser()

    def pre_config(self, config_dict):
        """ create/update variables binds
        @param config_dict
            {
                "requires": ["random", "hashlib"],
                "function_binds": {
                    "gen_random_string": \
                        "lambda str_len: ''.join(random.choice(string.ascii_letters + \
                        string.digits) for _ in range(str_len))",
                    "gen_md5": \
                        "lambda *str_args: hashlib.md5(''.join(str_args).\
                        encode('utf-8')).hexdigest()"
                },
                "variable_binds": [
                    {"TOKEN": "debugtalk"},
                    {"random": {"func": "gen_random_string", "args": [5]}},
                ]
            }
        @return variables binds mapping
            {
                "TOKEN": "debugtalk",
                "random": "A2dEx"
            }
        """
        requires = config_dict.get('requires', [])
        self.context.import_required_modules(requires)

        function_binds = config_dict.get('function_binds', {})
        self.context.bind_functions(function_binds)

        variable_binds = config_dict.get('variable_binds', [])
        self.context.bind_variables(variable_binds)

        self.test_case_parser.update_variables_binds(self.context.variables)

    def parse_test_case(self, test_case):
        """ parse test case with variables binds if it is a template.
        """
        self.pre_config(test_case)

        parsed_test_case = self.test_case_parser.parse(test_case)
        return parsed_test_case

    def prepare(self, test_case):
        """
        prepare work before runnint test.
        parse test case with variables binds if it's a template
        :param test_case:
        :return:
        """
        required_modules = test_case.get('requires', [])
        self.context.import_required_modules(required_modules)

        function_binds = test_case.get('function_binds', {})
        self.context.bind_functions(function_binds)

        variable_binds = test_case.get('variable_binds', {})
        self.context.bind_variables(variable_binds)

        parsed_test_case = self.test_case_parser.parse(test_case, variable_binds=self.context.variables)
        return parsed_test_case

    def run_test(self, test_case):
        """
        run single test case.
        :param test_case:
        :return:
        """
        test_case = self.parse_test_case(test_case)

        req_kwargs = test_case['request']
        try:
            url = req_kwargs.pop('url')
            method = req_kwargs.pop('method')
        except KeyError:
            raise exception.ParamsError('URL or METHOD missed!')

        resp = self.client.request(url=url, method=method, **req_kwargs)
        diff_content = utils.diff_response(resp, test_case['response'])
        print(diff_content)
        result = False if diff_content else True
        return result, diff_content

    def run_test_case_suite(self, test_case_sets):
        """
        run test case suite.
        :param test_case_sets:
        [
                {
                    "config": {
                        "requires": [],
                        "function_binds": {},
                        "variable_binds": []
                    }
                },
                {
                    "test": {
                        "variable_binds": {}, # override
                        "request": {},
                        "response": {}
                    }
                }
        ]
        :return:
        """
        results = []
        for item in test_case_sets:
            for key in item:
                if key == 'config':
                    config_dict = item[key]
                    self.pre_config(config_dict)
                elif key == 'test':
                    test_case = item[key]
                    result = self.run_test(test_case)
                    results.append(result)
        return results
