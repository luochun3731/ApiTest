import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask import request, make_response

app = Flask(__name__)
users = {
    'uid1': {
        'name': 'name1',
        'password': 'pwd1'
    },
    'uid2': {
        'name': 'name2',
        'password': 'pwd2'
    }
}

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log/server.log')
# log_file = os.path.join(os.getcwd(), 'log/server.log')
log_format = '[%(asctime)s] - [%(levelname)s] - %(message)s'
# logging.basicConfig(format=log_format, filename=log_file, filemode='w', level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_format)
console.setFormatter(formatter)

server_log = TimedRotatingFileHandler(log_file, 'D')
server_log.setLevel(logging.DEBUG)
server_log.setFormatter(logging.Formatter(log_format))

'''
error_log = TimedRotatingFileHandler('log/error.log', 'D')
error_log.setLevel(logging.ERROR)
error_log.setFormatter(log_format)
app.logger.addHandler(error_log)
'''

app.logger.addHandler(server_log)
app.logger.addHandler(console)


def start_mock_server():
    app.run()


@app.route('/')
def index():
    return 'Hello Python!'


@app.route('/status_code/<int:status_code>/')
def get_response_with_status_code(status_code):
    return 'Status Code: %d' % status_code, status_code


@app.route('/response_headers/', methods=['POST'])
def get_response_with_headers():
    headers_dict = request.get_json()
    content = 'Response headers: %s' % json.dumps(headers_dict)
    response = make_response(content)
    for header_key, header_value in headers_dict.items():
        response.headers[header_key] = header_value
    return response


@app.route('/custom_response/', methods=['POST'])
def get_custom_response():
    exp_resp_json = request.get_json()
    status_code = exp_resp_json.get('status_code', 200)
    headers_dict = exp_resp_json.get('headers', {})
    body = exp_resp_json.get('body', {})
    response = make_response(json.dumps(body), status_code)
    for header_key, header_value in headers_dict.items():
        response.headers[header_key] = header_value
    return response


@app.route('/api/users/')
def get_all_users():
    user_list = [user for uid, user in users.items()]
    result = {
        'success': True,
        'count': len(user_list),
        'items': user_list
    }
    status_code = 200
    response = make_response(json.dumps(result), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/users/<int:uid>/')
def get_user(uid):
    user = users.get(uid, {})
    if user:
        result = {
            'success': True,
            'data': user
        }
        status_code = 200
    else:
        result = {
            'success': False,
            'data': user
        }
        status_code = 404

    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/users/<int:uid>/', methods=['POST'])
def create_user(uid):
    app.logger.info('before create: ' + str(users))
    user = request.get_json()
    if uid not in users:
        result = {
            'success': True,
            'msg': 'user created successfully!'
        }
        status_code = 200
        users[uid] = user
    else:
        result = {
            'success': False,
            'msg': 'user already existed!'
        }
        status_code = 500
    app.logger.info('after create: ' + str(users))
    response = make_response(json.dumps(result), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/users/<int:uid>/', methods=['PUT'])
def update_user(uid):
    user = users.get(uid, {})
    if user:
        user = request.get_json()
        success = True
        status_code = 200
    else:
        success = False
        status_code = 404

    result = {
        'success': success,
        'data': user
    }
    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/users/<int:uid>/', methods=['DELETE'])
def delete_user(uid):
    user = users.pop(uid, {})
    if user:
        success = True
        status_code = 200
    else:
        success = False
        status_code = 404

    result = {
        'success': success,
        'data': user
    }
    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/users/', methods=['DELETE'])
def clear_users():
    users.clear()
    result = {
        'success': True
    }
    response = make_response(json.dumps(result))
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    # live_server = Server(app.wsgi_app)
    # live_server.watch('**/*.*')
    # live_server.serve(port='8000', open_url=False, debug=True)
    app.run(debug=True)
