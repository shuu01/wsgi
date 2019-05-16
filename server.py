#!/usr/bin/env python3

from wsgi_server import make_server
from my_app import app

SERVER_ADDRESS = (HOST, PORT) = '', 8888

if __name__ == '__main__':

    httpd = make_server(SERVER_ADDRESS, app)
    print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
    httpd.serve_forever()
