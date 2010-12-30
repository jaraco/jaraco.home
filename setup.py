
from setuptools import setup, find_packages
setup_params = dict(
	name='jaraco.home',
	version='1.0',
	packages=find_packages(),
	namespace_packages=['jaraco'],
	zip_safe=False,
)
if __name__ == '__main__':
	setup(**setup_params)
