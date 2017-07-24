import random

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

    def get_all_users(self):
        url = "%s/api/users/" % self.host
        return self.client.get(url)

    def create_user(self, uid, name, password):
        url = "%s/api/users/%d/" % (self.host, uid)
        data = {
            'name': name,
            'password': password
        }
        return self.client.post(url, json=data)

    def get_user(self, uid):
        url = "%s/api/users/%d/" % (self.host, uid)
        return self.client.get(url)

    def update_user(self, uid, name, password):
        url = "%s/api/users/%d/" % (self.host, uid)
        data = {
            'name': name,
            'password': password
        }
        return self.client.put(url, json=data)

    def delete_user(self, uid):
        url = "%s/api/users/%d/" % (self.host, uid)
        return self.client.delete(url)

    def test_clear_users(self):
        resp = self.clear_users()
        self.assertEqual(200, resp.status_code)
        self.assertEqual(True, resp.json()['success'])

    def test_create_user_not_existing(self):
        resp = self.create_user(505, 'test01', 'qwe123')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(True, resp.json()['success'])

    def test_create_user_existing(self):
        self.create_user(1, 'test01', 'qwe123')
        resp = self.create_user(1, 'test01', 'qwe123')
        self.assertEqual(500, resp.status_code)
        self.assertEqual(False, resp.json()['success'])

    def test_get_all_users_empty(self):
        self.clear_users()
        resp = self.get_all_users()
        self.assertEqual(200, resp.status_code)
        self.assertEqual(0, resp.json()['count'])

    def test_get_all_users_not_empty(self):
        self.create_user(0, 'user00', 'password00')
        self.create_user(1, 'user01', 'password01')
        resp = self.get_all_users()
        self.assertEqual(200, resp.status_code)
        self.assertEqual(2, resp.json()['count'])

    def test_update_user_existing(self):
        self.create_user(505, 'user01', 'user01')
        resp = self.update_user(505, 'user02', 'qwer1234')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(True, resp.json()['success'])
        self.assertEqual('user02', resp.json()['data']['name'])

    def test_update_user_not_existing(self):
        resp = self.update_user(5000, 'test5000', 'qwer5000')
        self.assertEqual(404, resp.status_code)
        self.assertEqual(False, resp.json()['success'])

    def test_delete_user_existing(self):
        self.create_user(505, 'user01', 'password01')
        resp = self.delete_user(505)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(True, resp.json()['success'])

    def test_delete_user_not_existing(self):
        resp = self.delete_user(7788)
        self.assertEqual(404, resp.status_code)
        self.assertEqual(False, resp.json()['success'])

    def test_get_response_with_status_code(self):
        status_code = random.randint(200, 520)
        url = '%s/status_code/%d/' % (self.host, status_code)
        resp = self.client.get(url)
        self.assertEqual(status_code, resp.status_code)

    def test_get_response_with_headers(self):
        headers = {
            'test01': 123,
            'test02': 456
        }
        url = '%s/response_headers/' % self.host
        resp = self.client.post(url, json=headers)
        self.assertIn('test01', resp.headers)
        self.assertEqual('456', resp.headers['test02'])

    def test_get_custom_response(self):
        exp_resp = {
            'headers': {
                'test01': 123,
                'test02': 456
            }
        }
        url = '%s/custom_response/' % self.host
        resp = self.client.post(url, json=exp_resp)
        self.assertIn('test01', resp.headers)
        self.assertEqual('456', resp.headers['test02'])
