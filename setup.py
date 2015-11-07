from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(
	name='ckanext-cmre',
	version=version,
	description="Ckan cmre extension",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Tobia Di Pisa',
	author_email='tobia.dipisa@geo-solutions.it',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.cmre'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points="""
        [ckan.plugins]
	# Add plugins here, eg
	cmre=ckanext.cmre.plugin:CMREThemePlugin
	cmre_harvester=ckanext.cmre.harvesters.cmre:CMREHarvester
	""",
)
