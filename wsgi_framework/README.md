# wsgi_framework

Simple wsgi framework written for educational purpose  

## usage

    from wsgi_framework import App
    from wsgi_framework.utils import Response
  
    def index_handler(request):
        response = Response(body='index', headers={}, code=200)
        return response

    routes = {
        '/': index_handler,
    }
  
    app = App(routes)

    @app.route('/home')
    def home_handler(request):
        return Response(body='home)