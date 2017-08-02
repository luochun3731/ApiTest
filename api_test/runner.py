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
        test_case = self.prepare(test_case)
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
        return [self.run_test(test_case) for test_case in test_case_sets]
