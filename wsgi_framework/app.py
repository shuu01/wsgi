from urllib.parse import parse_qs
from .utils import Response, Request

class App(object):

    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, start_response):
        ''' According to pep333 App class must be callable '''
        # get request path and find request handler for this path
        handler = self.routes.get(environ.get('PATH_INFO')) or self.not_found
        # return response body from this handler
        return self.handler_wrapper(handler, environ, start_response)

    def handler_wrapper(self, handler, environ, start_response):
        # parse environment and put variables into request object
        request = self.parse_request(environ)
        # get response object from handler
        response = handler(request)
        start_response(response.status, response.headers)
        return response.body

    def not_found(self, request):
        ''' Simple builtin 404 page '''
        code = 404
        body = '''
            <!DOCTYPE html>
            <html>
              <body>
                <h1>404 page</h1>
                <br>
                oops, something got wrong
              </body>
            </html>
        '''
        headers = {}
        response = Response(code=code, body=body, headers=headers)
        return response

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def parse_request(self, environ):
        ''' Simple request parser '''
        request = Request()

        request.method = environ.get('REQUEST_METHOD')
        request.path = environ.get('PATH_INFO')
        request.args = parse_qs(environ.get('QUERY_STRING'))

        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size).decode()
        request.form = parse_qs(request_body)

        return request

    def render_template(self, template):
        pass

    def redirect(self, url):
        pass

    def url_for(self, handler):
        pass
