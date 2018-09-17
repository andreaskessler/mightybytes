import json
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def flonar_planzabstand(canton, distance, height):
    return json.dumps('Not yet implemented')

def flonar_usage(request):
    return Response('Flonar usage: /flonar/pa/{canton}/{distance}/{height}')

def flonarpa_engine(request):
    canton = '%(canton)s' % request.matchdict
    distanceStr = '%(distance)s' % request.matchdict
    heightStr = '%(height)s' % request.matchdict
    return Response('Flonar Planzabstand fuer %s: d=%s, h=%s' % (
        canton, distanceStr, heightStr))

if __name__ == '__main__':
    with Configurator() as config:
        # Pflanzabstand engine.
        config.add_route('flonarpa', '/flonar/pa/{canton}/{distance}/{height}')
        config.add_view(flonarpa_engine, route_name='flonarpa')
        # Usage help.
        config.add_route('flonar_usage1', '/flonar/')
        config.add_route('flonar_usage2', '/flonar/{name}')
        config.add_view(flonar_usage, route_name='flonar_usage1')
        config.add_view(flonar_usage, route_name='flonar_usage2')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 80, app)
    server.serve_forever()
