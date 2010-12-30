
from setuptools import setup, find_packages
setup_params = dict(
	name='jaraco.home',
	use_hg_version={'increment':'0.1'},
	packages=find_packages(),
	namespace_packages=['jaraco'],
	zip_safe=False,
	entry_points = dict(
		console_scripts=[
			'thermostat=jaraco.home.thermostat:simple_request',
			]
		),
	setup_requires=[
		'hgtools',
	],
)
if __name__ == '__main__':
	setup(**setup_params)
