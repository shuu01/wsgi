import socket
import sys
from datetime import datetime

try:
    from BytesIO import BytesIO
except:
    from io import BytesIO

class WSGIServer(object):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1
    version = '0.2'
    CRLF = '\r\n'

    def __init__(self, server_address):
        # Create a listening socket
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind
        listen_socket.bind(server_address)
        # Activate
        listen_socket.listen(self.request_queue_size)
        # Get server host name and port
        host, port = listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        # Return headers set by Web framework/Web application
        self.headers_set = []

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        listen_socket = self.listen_socket
        while True:
            # New client connection
            self.client_connection, client_address = listen_socket.accept()
            print('connection: {}\n'.format(self.client_connection))
            # Handle one request and close the client connection. Then
            # loop over to wait for another client connection
            self.handle_one_request()

    def handle_one_request(self):
        self.request_data = self.client_connection.recv(1024)
        # Print formatted request data a la 'curl -v'
        print(''.join(
            '< {}\n'.format(line)
            for line in self.request_data.splitlines()
        ))

        self.parse_request(self.request_data)

        # Construct environment dictionary using request data
        env = self.get_environ()

        # It's time to call our application callable and get
        # back a result that will become HTTP response body
        result = self.application(env, self.start_response)

        # Construct a response and send it back to the client
        self.finish_response(result)

    def parse_request(self, text):

        request = text.decode().split(self.CRLF*2)
        self.request_body = request[1]
        self.content_length = len(self.request_body)

        request_line = request[0].splitlines()[0]
        # Break down the request line into components
        (
            self.request_method,  # GET or POST
            self.path,            # /hello?a=1&b=2
            self.request_version,  # HTTP/1.1
        ) = request_line.split()
        # Break down path line into path and query
        if '?' in self.path:
            self.path, self.query = self.path.split('?')
        else:
            self.query = ''

    def get_environ(self):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = BytesIO(self.request_body.encode())
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = self.request_method    # GET or POST
        env['PATH_INFO']         = self.path              # /hello
        env['QUERY_STRING']      = self.query             # a=1&b=2
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        env['CONTENT_LENGTH']    = str(self.content_length)
        return env

    def start_response(self, status, response_headers):
        # Add necessary server headers
        server_headers = [
            ('Date', datetime.now().ctime()),
            ('Server', f'WSGIServer {self.version}'),
        ]
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = f'{status}\r\n'
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data
            # Print formatted response data a la 'curl -v'
            print('\n'.join(f'> {line}' for line in response.splitlines()))
            self.client_connection.sendall(response.encode())
        finally:
            self.client_connection.close()

SERVER_ADDRESS = (HOST, PORT) = '', 8888

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
    httpd.serve_forever()
