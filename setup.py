from setuptools import setup, find_packages
import os

version = '1.0'

setup(
	name='ckanext-cmre',
	version=version,
	description="CKAN CMRE EKOE extension",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Emanuele Tajariol',
	author_email='etj@geo-solutions.it',
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
	cmre_test_harvester=ckanext.cmre.harvesters.iso19115_2016_harvester:ISO19115_3Harvester
	cmre_harvester=ckanext.cmre.harvesters.cmre:CMREHarvester
	cmre_facets=ckanext.cmre.plugin:CMREFacetsPlugin
	""",
)
