import logging
import json

from ckan.plugins.core import SingletonPlugin

from ckanext.cmre.harvesters.fs import FileSystemHarvester

from ckanext.spatial.model import (ISODocument, ISOElement, ISOResponsibleParty)


from ckan import logic, model
from ckan import plugins as p
from ckan.lib.navl.validators import not_empty
from ckan.lib.search.index import PackageSearchIndex
from ckanext.cmre.harvesters.ngmp_parser import EKOEDocument
from ckanext.harvest.model import HarvestObject
from ckanext.spatial.interfaces import ISpatialHarvester
from ckanext.spatial.validation.validation import (Validators, XsdValidator,
                                                   all_validators)

from ckanext.cmre.harvesters.ngmp_validator import NgmpSchema

log = logging.getLogger(__name__)


class CMREHarvester(FileSystemHarvester, SingletonPlugin):

    def info(self):
        return {
            'name': 'cmre-ekoe',
            'title': 'CMRE EKOE filesystem harvester',
            'description': 'Harvests local documents for EKOE - Based on NGMP(ISO19115-2:2009)',
            'form_config_interface': 'Text'
        }

    def get_package_dict(self, iso_values, harvest_object):
        package_dict = super(CMREHarvester, self).get_package_dict(iso_values, harvest_object)

        try:
            iso_parser = EKOEDocument(harvest_object.content)
            iso_values = iso_parser.read_values()
        except Exception, e:
            self._save_object_error('Error parsing ISO document for object {0}: {1}'.format(harvest_object.id, str(e)),
                                    harvest_object, 'Import')
            return None

        # log.info('CMREHarvester ::::::::::::::::: %r', package_dict)

        # OWNER ORGANIZATION
        if len(iso_values.get('owner_org', [])):
            package_dict['extras'].append({'key': 'ekoe_owner_org', 'value': iso_values['owner_org'][0]})

        # DIMENSIONS NAMES
        if len(iso_values.get('dimension_name', [])):
            package_dict['extras'].append({'key': 'ekoe_dimension', 'value': json.dumps(iso_values['dimension_name'])})

        # LEGAL CONSTRAINTS
        if len(iso_values.get('legal-use-constraints', [])):
            package_dict['extras'].append({'key': 'use-limitation', 'value': iso_values['legal-use-constraints'][0]})

        if len(iso_values.get('extent-free-text', [])):
            package_dict['extras'].append({'key': 'ekoe_identifier', 'value': iso_values['extent-free-text'][0]})

        date_created = iso_values.get('date-created')
        if date_created:
            package_dict['extras'].append({'key': 'date-created', 'value': date_created})

        # VERTICAL ELEMENT
        if len(iso_values.get('vertical-extent-min', [])) and len(iso_values.get('vertical-extent-max', [])):
            crs_title = ''

            if len(iso_values.get('vertical-extent-crs-title', [])):
                crs_title = iso_values['vertical-extent-crs-title'][0]

            vert_ext_min = iso_values['vertical-extent-min'][0]
            vert_ext_max = iso_values['vertical-extent-max'][0]

            if vert_ext_min == vert_ext_max:
                package_dict['extras'].append({'key': 'vertical-extent', 'value': vert_ext_min + ' ' + crs_title})
            else:
                package_dict['extras'].append(
                    {'key': 'vertical-extent', 'value': vert_ext_min + ' / ' + vert_ext_max + ' ' + crs_title})

        # TEMPORAL ELEMENTS
        if len(iso_values.get('temporal-extent-instant', [])):
            tempstr = iso_values['temporal-extent-instant'][0]
            date_str = self.parseDate(tempstr)
            package_dict['extras'].append({'key': 'temporal-extent-instant', 'value': date_str})

        for key in ['temporal-extent-begin', 'temporal-extent-end']:
            if len(iso_values[key]) > 0:
                tempstr = iso_values[key][0]

                for extra in package_dict['extras']:
                    extra_key = extra['key']

                    if key == extra_key:
                        extra['value'] = tempstr

        # SECURITY CLASSIFICATION
        for name in ['ngmp-security-classification-code', 'ngmp-security-classification-system']:
            val = iso_values.get(name)
            if val:
                package_dict['extras'].append({'key': name, 'value': val})

        for name in ['trial', 'platform', 'sensor', 'experiment']:
            val = iso_values.get("keyword-" + name)
            if val:
                package_dict['extras'].append({'key': "ekoe_"+name, 'value': json.dumps(val)})

        classif = iso_values.get("ekoe-classification")
        if classif:
            code = classif.get("code")
            system = classif.get("classification")
            package_dict['extras'].append({
                'key': "ekoe_classification",
                'value': "{system} {code}".format(code=code, system=system).upper()})
        else:
            package_dict['extras'].append({
                'key': "ekoe_classification",
                'value': "PUBLIC RELEASABLE"})


        # ISO 19139 EXTENSION ELEMENTS (MyOcean)
        # for tag in iso_values['keyword-inspire-theme-anchor']:
        #    tag = tag[:50] if len(tag) > 50 else tag
        #    package_dict['tags'].append({'name': tag})

        # End of processing, return the modified package
        return package_dict

    def fix_resource_type(self, resources):
        super(CMREHarvester, self).fix_resource_type(resources)

        for resource in resources:
            if 'MYO:MOTU-SUB' in resource['resource_locator_protocol']:
                resource['format'] = 'HTTP'
            elif 'MYO:MOTU-DGF' in resource['resource_locator_protocol']:
                resource['format'] = 'HTTP'
            elif 'WWW:FTP' in resource['resource_locator_protocol']:
                resource['format'] = 'FTP'
            else:
                url = resource.get('url').lower().strip()

                file_types = self.source_config.get('file_types', {})
                if file_types is None:
                    file_types = {
                        'NetCDF': ['nc', 'ncml'],
                        'log': ['log'],
                        'matlab': ['dat'],
                        'cnv': ['cnv'],
                        'out': ['out'],
                        'asc': ['asc'],
                    }

                for file_type, extensions in file_types.iteritems():
                    if any(url.endswith(extension) for extension in extensions):
                        resource['format'] = file_type

    def _get_validator(self):
        return NgmpSchema
