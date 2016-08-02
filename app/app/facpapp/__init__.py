from pyramid.config import Configurator
from pyramid.paster import setup_logging

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    setup_logging(global_config['__file__'])

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('page',        '/guide/{state}/{entity}')
    config.add_route('page_json',   '/guide/{state}/{entity}/json')
    config.scan()
    return config.make_wsgi_app()
