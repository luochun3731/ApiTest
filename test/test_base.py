import multiprocessing
import time
import unittest

import mock_server


class TestBase(unittest.TestCase):
    mock_server_process = None

    @classmethod
    def setUpClass(cls):
        cls.mock_server_process = multiprocessing.Process(target=mock_server.start_mock_server)
        cls.mock_server_process.start()
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.mock_server_process.terminate()
