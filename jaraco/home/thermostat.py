import argparse
import json
from six.moves import urllib
from pprint import pprint

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
	data = urllib.urlencode(params) if params else None
	url = urllib.parse.urljoin(thermostat, path)
	req = urllib.request.urlopen(url, data)
	res = json.load(req)
	return res

def simple_request():
	parser = argparse.ArgumentParser()
	parser.add_argument('command')
	args = parser.parse_args()
	pprint(request(args.command))

def reboot():
	# from http://thermostat/update.shtml
	pprint(request('/sys/cmd', command='reboot'))
