import setuptools

setup_params = dict(
	name='jaraco.home',
	use_hg_version={'increment':'0.1'},
	packages=setuptools.find_packages(),
	namespace_packages=['jaraco'],
	install_requires=[
		'requests',
		'lxml',
	],
	setup_requires=[
		'hgtools',
	],
)

if __name__ == '__main__':
	setuptools.setup(**setup_params)
