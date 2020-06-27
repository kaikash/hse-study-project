from flask import Flask, Response, request


class ServerError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def to_json(self):
        return {
            'message': self.msg,
            'code': self.code
        }


class EndpointAction:
    def __init__(self, action):
        self.action = action
        self.response = None

    def __call__(self, *args):
        try:
            return self.action(request)
        except ServerError as err:
            return err.to_json(), err.code


class Server:
    def __init__(self, name, host='0.0.0.0', port=3000):
        self.port = port
        self.host = host
        self.app = Flask(name, static_folder='data', static_url_path='/data')

    def run(self):
        self.app.run(host=self.host, port=self.port)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)
