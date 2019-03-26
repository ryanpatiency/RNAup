from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('json', '/json')
        config.add_static_view(name='', path='.')
        config.scan('views')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()
