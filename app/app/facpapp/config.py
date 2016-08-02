
import ConfigParser
import os

from pyramid.httpexceptions import HTTPBadRequest

import collections
import logging
log = logging.getLogger(__name__)


class ConfigBase:
    def __init__(self):
        pass

    def get(self, section, param, aslist=False):
        data = self.cfg.get(section, param) if (self.cfg.has_section(section) and self.cfg.has_option(section, param)) else None
        if data == None:
            log.error("Missing parameter %s in section %s" % (param, section))
        if aslist:
            return [ d.strip() for d in data.split(',') ]
        return data

class Config(ConfigBase):

    def __init__(self, request, code):
        """
        Expects to be called with a pyramid request object.

        The path to the configs will be extracted from the pyramid
        configuration and a config object will be returned.

        The params from the config will be available as instance
        variables.

        @params:
        request: a pyramid request object
        code: the code of the site whose config we want to read
        item: (optional) the item of concern
        series: (optional) the series of concern
        """
        settings = request.registry.settings
        config_file = "%s/%s" % ( settings['eac.configs'], code )

        self.cfg = ConfigParser.SafeConfigParser()
        try:
            self.cfg.read(config_file)
        except ConfigParser.ParsingError:
            log.error('Config file parsing errors')
            log.error(sys.exc_info()[1])
            sys.exit()

    def load(self):
        conf = collections.namedtuple('siteconf',
            [ 'eac', 'map' ]
        )
        return conf(
                    self.get('General', 'eac'),
                    self.get('General', 'map', aslist=True),
                   )
