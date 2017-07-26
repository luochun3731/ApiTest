import multiprocessing
import time
import unittest

import mock_server
from api_test import utils


class TestBase(unittest.TestCase):
    mock_server_process = None
    authentication = False

    @classmethod
    def setUpClass(cls):
        mock_server.AUTHENTICATION = cls.authentication
        cls.mock_server_process = multiprocessing.Process(target=mock_server.start_mock_server)
        cls.mock_server_process.start()
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.mock_server_process.terminate()

    def build_headers(self, data=''):
        token = mock_server.TOKEN
        data = utils.handle_req_data(data)
        random_str = utils.gen_random_string(8)
        authorization = utils.gen_md5(token, data, random_str)
        headers = {
            'authorization': authorization,
            'random': random_str
        }
        return headers
