from .wsgi_server import WSGIServer


def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server
