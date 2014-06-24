import argparse
from pprint import pprint

from six.moves import urllib
import requests
import lxml.html

"""
API wiki: http://central.isaroach.com/wiki/index.php/Main_Page
"""

thermostat = 'http://192.168.14.20'

def request(path, **params):
	"""
	Path is something like
	/sys/info
	/sys/network
	/tstat/info
	"""
	url = urllib.parse.urljoin(thermostat, path)
	return requests.get(url, data=params).json()

def simple_request():
	parser = argparse.ArgumentParser()
	parser.add_argument('command')
	args = parser.parse_args()
	pprint(request(args.command))

def reboot():
	# from http://thermostat/update.shtml
	pprint(request('/sys/cmd', command='reboot'))


class RadioThermostat:
	"""
	Class for authenticating with the publically-hosted radiothermostat
	thermostats.
	"""
	root = 'https://my.radiothermostat.com/filtrete/rest/'
	session = requests.session()

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def api(self, path):
		return urllib.parse.urljoin(self.root, path)

	@classmethod
	def open_for_lxml(cls, method, url, values):
		"""
		Open a request for lxml using the class' session
		"""
		return cls.session.request(url=url, method=method, data=dict(values))

	@classmethod
	def submit(cls, form):
		return lxml.html.submit_form(form, open_http=cls.open_for_lxml)

	def login(self):
		resp = self.session.get(self.root)
		if 'login' not in resp.url:
			return
		page = lxml.html.fromstring(resp.text, base_url=resp.url)
		form = page.forms[0]
		form.fields['j_username'] = self.username
		form.fields['j_password'] = self.password
		resp = self.submit(form)
		assert 'login' not in resp.url, "Login failed"

	def get_locations(self):
		self.login()
		return map(Location, self.session.get(self.api('locations')).json())

	def get_first_temp(self):
		"""
		Get the temperature from the first location registered for the
		account.
		"""
		loc = next(iter(self.get_locations()))
		url = self.api('gateways?location={id}'.format(**loc))
		resp = self.session.get(url)
		return resp.json()[0]['settings']['temp']

class Location(dict):
	def get_link(self, name):
		links_by_name = {
			link['rel']: link['uri']
			for link in self['links']
		}
		return links_by_name[name]
