import traceback
import json

import cherrypy

from . import thermostat

"""
A relay for publically-exposed interfaces.
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
				'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
				'tools.decode.on': True,
				'tools.trailing_slash.on': True,
			},
		}

		return cherrypy.tree.mount(cls(), root, config)

	@classmethod
	def factory(cls):
		"The entry point for when the ISAPIDLL is triggered"
		try:
			import isapi_wsgi
			return isapi_wsgi.ISAPISimpleHandler(cls.setup_application('/home'))
		except Exception:
			traceback.print_exc()


__ExtensionFactory__ = Site.factory


def handle_isapi():
	"Install or remove the extension to the virtual directory"
	import isapi.install
	params = isapi.install.ISAPIParameters()
	# Setup the virtual directories - this is a list of directories our
	# extension uses - in this case only 1.
	# Each extension has a "script map" - this is the mapping of ISAPI
	# extensions.
	sm = [
		isapi.install.ScriptMapParams(Extension="*", Flags=0)
	]
	vd = isapi.install.VirtualDirParameters(
		Server="Default Web Site",
		Name="/home",
		Description="Media Index",
		ScriptMaps=sm,
		ScriptMapUpdate="end",
	)
	params.VirtualDirs = [vd]
	isapi.install.HandleCommandLine(params)
