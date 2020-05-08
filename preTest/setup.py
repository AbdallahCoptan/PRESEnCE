from setuptools import setup

setup(
	name= 'presence',
	version='1.0',
	py_modules=['presence'],
	install_requires=[
		'Click',
	],
	entry_points='''
		[console_scripts]
		presence=presence:presence
	''',
	)