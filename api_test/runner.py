import requests

from api_test import exception
from api_test import utils


class Runner:
    def __init__(self):
        self.client = requests.Session()

    def run_single_test_case(self, test_case):
        req_kwargs = test_case['request']

        try:
            url = req_kwargs.pop('url')
            method = req_kwargs.pop('method')
        except KeyError:
            raise exception.ParamsError('Params Error!')

        resp = self.client.request(url=url, method=method, **req_kwargs)
        diff_content = utils.diff_response(resp, test_case['response'])
        print(diff_content)
        result = False if diff_content else True
        return result, diff_content

    def run_test_case_suite(self, test_case_sets):
        return [self.run_single_test_case(test_case) for test_case in test_case_sets]
