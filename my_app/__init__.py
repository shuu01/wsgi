from wsgi_framework import App
from wsgi_framework.utils import Response
from .routes import routes

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
