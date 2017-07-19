import requests

from test.test_base import TestBase


class TestMockServer(TestBase):
    def setUp(self):
        super(TestMockServer, self).setUp()
        self.host = 'http://127.0.0.1:5000'
        self.client = requests.Session()
        self.clear_users()

    def tearDown(self):
        super(TestMockServer, self).tearDown()

    def clear_users(self):
        url = '%s/api/users/' % self.host
        return self.client.delete(url)

    def test_create_user_not_existing(self):
        self.clear_users()
        url = '%s/api/users/%d/' % (self.host, 200)
        data = {
            'name': 'jack',
            'password': 'xtb147258'
        }
        resp = self.client.post(url, json=data)

        self.assertEqual(205, resp.status_code)
        self.assertEqual(True, resp.json()['success'])
