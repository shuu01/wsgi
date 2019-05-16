from my_app import Response

def index_handler(request):
    code = 200
    body = 'index'
    headers = {}
    response = Response(body=body, headers=headers, code=code)
    return response
