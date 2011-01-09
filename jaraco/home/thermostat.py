import optparse
import json
import urlparse
import urllib
import urllib2
from pprint import pprint

thermostat = 'http://10.0.11.20'

def request(path, **params):
	"""
	Path is something like
	/sys/info
	/sys/network
	/tstat/info
	"""
	data = urllib.urlencode(params) if params else None
	url = urlparse.urljoin(thermostat, path)
	req = urllib2.urlopen(url, data)
	res = json.load(req)
	return res

def simple_request():
	parser = optparse.OptionParser()
	options, args = parser.parse_args()
	path = args.pop(0)
	pprint(request(path))

def reboot():
	# from http://thermostat/update.shtml
	pprint(request('/sys/cmd', command='reboot'))
