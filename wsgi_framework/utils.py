class Request(object):
    ''' Simple request object '''

    def __init__(self):
        self.method = None # request method
        self.path = None # request path
        self._args = {} # the key:value pairs in the URL query string
        self._form = {} #  the key:value pairs in the body, from a HTML post form
        self.headers = {} # request headers
        self.finished = False

    @property
    def args(self):
        ret = {}
        for key, value in self._args.items():
            ret[key] = value[0]
        return ret

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def form(self):
        ret = {}
        for key, value in self._form.items():
            ret[key] = value[0]
        return ret

    @form.setter
    def form(self, args):
        self._form = args

    @property
    def data(self):
        ''' combined args and form '''
        return {**self._form, **self._args}

class Response(object):
    ''' Simple response object '''

    reason_phrases = {
        200: 'OK',
        204: 'No Content',
        301: 'Moved Permanently',
        302: 'Found',
        304: 'Not Modified',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        451: 'Unavailable for Legal Reasons',
        500: 'Internal Server Error',
    }

    def __init__(self, code=200, body='', headers={}):
        self.code = code
        self._body = body
        self._headers = headers
        self._headers['Content-Length'] = len(self._body)

    @property
    def status(self):
        _status = 'HTTP/1.1 {0} {1}'.format(
            self.code,
            self.reason_phrases[self.code],
        )
        return _status

    @property
    def body(self):
        return iter([self._body])

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def headers(self):
        return [(key.upper(), value) for key, value in self._headers.items()]

    @headers.setter
    def headers(self, value):
        self._headers = value

    def set_header(self, header, value=''):
        """
        Helper method to set a HTTP header.
        :param header: A string with the headername.
        :param value: A string - value of the header.
        """
        self._headers[header] = value

