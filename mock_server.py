import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask import request, make_response

app = Flask(__name__)
users = {}

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


@app.route('/api/users/<int:uid>/', methods=['POST'])
def create_user(uid):
    app.logger.info('before create: ' + str(users))
    user = request.get_json()
    if uid not in users:
        result = {
            'success': True,
            'msg': 'user created successfully!'
        }
        status_code = 205
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
