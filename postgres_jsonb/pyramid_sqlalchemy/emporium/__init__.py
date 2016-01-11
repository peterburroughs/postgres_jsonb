import os

from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import SignedCookieSessionFactory

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    connect_string = settings['sqlalchemy.url']\
        .replace('DBUser', os.environ['DBUSER'])\
        .replace('DBPassword', os.environ['DBPASSWORD'])
    settings['sqlalchemy.url'] = connect_string
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    session_factory = SignedCookieSessionFactory('thisissecret')
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
