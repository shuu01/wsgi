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

    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        return Response(body=f'welcome home {name} {surname}')
    else:
        body = '''
        <form method="post">
            <label>Hello</label>
            <input type="text" name="name">
            <input type="text" name="surname">
            <input type="submit" value="Go">
        </form>
        '''
        code = 200
        return Response(body=body, code=code)
