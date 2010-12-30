import optparse
import json
import urlparse
import urllib2
from pprint import pprint

thermostat = 'http://10.0.11.20'

def request(path):
	"""
	Path is something like
	/sys/info
	/sys/network
	/tstat/info
	"""
	url = urlparse.urljoin(thermostat, path)
	req = urllib2.urlopen(url)
	res = json.load(req)
	return res

def simple_request():
	parser = optparse.OptionParser()
	options, args = parser.parse_args()
	path = args.pop(0)
	pprint(request(path))

	