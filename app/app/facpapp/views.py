from pyramid.view import view_config
from pyramid.view import notfound_view_config
from pyramid.httpexceptions import HTTPSeeOther

import time
from lxml import etree

from config import Config

import logging
log = logging.getLogger('eacdatasource')

@notfound_view_config()
def notfound(req):
    return HTTPSeeOther(location='/error/')
