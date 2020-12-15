import json

import cherrypy

from . import thermostat

"""
A relay to expose internal-only resources to public.
"""


class Site:
    @cherrypy.expose
    def temp(self):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(thermostat.request('/tstat/temp'))

    @classmethod
    def setup_application(cls, root):
        config = {
            'global': {
                'tools.encode.on': True,
                'tools.encode.encoding': 'utf-8',
                'tools.decode.on': True,
                'tools.trailing_slash.on': True,
            },
        }

        return cherrypy.tree.mount(cls(), root, config)
