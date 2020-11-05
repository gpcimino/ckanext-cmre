import logging
import json

from ckan.plugins.core import SingletonPlugin

from ckanext.cmre.ekoe_const import EKOE_TRIAL, EKOE_EXPERIMENT
from ckanext.cmre.harvesters.fs import FileSystemHarvester
from ckanext.cmre.ekoe_const import *

from ckanext.cmre.harvesters.ngmp_parser import EKOEDocument, NGMP_TYPES

from ckanext.cmre.harvesters.ngmp_validator import NgmpSchema

log = logging.getLogger(__name__)

CMRE_WK_THESAURI_HREF = {
    'http://datacatalog-dev/cruisedb' : EKOE_TRIAL,
    'http://datacatalog-dev/experimenttype' : EKOE_EXPERIMENT,
    'http://cfconventions.org/Data/cf-standard-names/current/src/cf-standard-name-table.xml': EKOE_VARIABLE,
}


class CMREHarvester(FileSystemHarvester, SingletonPlugin):

    def info(self):
        return {
            'name': 'cmre-ekoe',
            'title': 'CMRE EKOE filesystem harvester',
            'description': 'Harvests local documents for EKOE - Based on NGMP(ISO19115-2:2009)',
            'form_config_interface': 'Text'
        }

    def get_package_dict(self, super_iso_values, harvest_object):
        package_dict = super(CMREHarvester, self).get_package_dict(super_iso_values, harvest_object)

        try:
            iso_parser = EKOEDocument(harvest_object.content)
            iso_values = iso_parser.read_values()
        except Exception, e:
            log.warn('Error parsing EKOE document ')
            self._save_object_error('Error parsing ISO document for object {0}: {1}'.format(harvest_object.id, str(e)),
                                    harvest_object, 'Import')
            return None

        # log.info('CMREHarvester ::::::::::::::::: %r', package_dict)

        # OWNER ORGANIZATION
        owner_org = iso_values.get('owner_org', [])
        owner_org = owner_org[0] if len(owner_org) else 'Unknown organization'
        package_dict['extras'].append({'key': EKOE_OWNER_ORG, 'value': owner_org})

        # LEGAL CONSTRAINTS
        if len(iso_values.get('legal-use-constraints', [])):
            package_dict['extras'].append({'key': 'use-limitation', 'value': iso_values['legal-use-constraints'][0]})

        date_created = iso_values.get('date-created')
        if date_created:
            package_dict['extras'].append({'key': 'date-created', 'value': date_created})

        # VERTICAL ELEMENT
        if len(iso_values.get('vertical-extent-min', [])) or len(iso_values.get('vertical-extent-max', [])):
            crs_title = ''

            if len(iso_values.get('vertical-extent-crs-title', [])):
                crs_title = iso_values['vertical-extent-crs-title'][0]

            vert_ext_min = iso_values.get('vertical-extent-min', ['-'])[0]
            vert_ext_max = iso_values.get('vertical-extent-max', ['-'])[0]

            if vert_ext_min == vert_ext_max:
                package_dict['extras'].append(
                    {'key': 'vertical-extent', 'value': vert_ext_min + ' ' + crs_title})
            else:
                package_dict['extras'].append(
                    {'key': 'vertical-extent', 'value': '{} to {} {}'.format(vert_ext_min, vert_ext_max, crs_title)})

        # TEMPORAL ELEMENTS
        if len(iso_values.get('temporal-extent-instant', [])):
            tempstr = iso_values['temporal-extent-instant'][0]
            date_str = self.parseDate(tempstr)
            package_dict['extras'].append({'key': 'temporal-extent-instant', 'value': date_str})

        temp_begin = iso_values.get('temporal-extent-begin', [])
        temp_end = iso_values.get('temporal-extent-end', [])
        if len(temp_begin) + len(temp_end):
            temp_begin = temp_begin[0] if len(temp_begin) else '-'
            temp_end = temp_end[0] if len(temp_end) else '-'
            package_dict['extras'].append(
                {'key': 'temporal-extent', 'value': '{} to {}'.format(temp_begin, temp_end)})

        # SECURITY CLASSIFICATION
        sec_constraints = iso_values.get('resource-security', None)
        classification = "Unknown"
        if sec_constraints:
            classification = '{} {}'.format(sec_constraints['classification'], sec_constraints['code'])
        else:
            classification = iso_values.get('ngmp-resource-releasibility', classification)
        package_dict['extras'].append({'key': EKOE_DATA_CLASSIFICATION, 'value': classification})

        # METADATA CLASSIFICATION
        sec_constraints = iso_values.get('metadata-security', None)
        classification = "Unknown"
        if sec_constraints:
            classification = '{} {}'.format(sec_constraints['classification'], sec_constraints['code'])
        package_dict['extras'].append({'key': 'ekoe_metadata_classification', 'value': classification})

        # Copy and encode strings and full complex objects
        for name in [
                'lineage',
                'topic-category',
                ('extent-free-text', EKOE_GEO_IDENTIFIER),
                'metadata-standard-name',
                'metadata-standard-version',
                'fileid',
                'filehref',
                'parentid',
                'parenthref',
                # 'spatial-reference-system'
        ]:
            name, rename = name if type(name) == tuple else (name, name)
            val = iso_values.get(name)

            if val:
                val = json.dumps(val) if type(val) not in (str, unicode) else val
                package_dict['extras'].append({'key': rename, 'value': val})

        # responsible parties
        for resp_key in ("data-resp-party", "metadata-resp-party"):
            resp_values = iso_values.get(resp_key)
            if resp_values:
                resp_by_role = {}  # role: list of resppary
                for resp_value in resp_values:
                    role = resp_value['role']
                    resp_list = resp_by_role.get(role, [])
                    resp_list.append(resp_value)
                    resp_by_role[role] = resp_list
                package_dict['extras'].append({'key': resp_key, 'value': json.dumps(resp_by_role)})

        # extract and encode sub dicts
        for isokey, subfields in [
                ('gmi-platform', ('code', 'description')),
        ]:
            isodict = iso_values.get(isokey)
            if isodict:
                extra_dict = {k: isodict[k] for k in subfields if isodict.get(k, None)}
                # log.info("Adding key {} --> {}".format(isokey, extra_dict))
                package_dict['extras'].append({'key': isokey, 'value': json.dumps(extra_dict)})

        # extract info for index
        if iso_values.get('gmi-platform', None):
            package_dict['extras'].append({'key': EKOE_PLATFORM, 'value': iso_values['gmi-platform']['code']})

        # extract and encode list of sub dicts
        for isokey, subfields in [
                ('gmi-instrument', ('code', 'type', 'description')),
        ]:
            isolist = iso_values.get(isokey)
            if isolist:
                extracted_list = []
                for isodict in isolist:
                    extracted_dict = {k: isodict[k] for k in subfields if isodict.get(k, None)}
                    extracted_list.append(extracted_dict)
                    # log.info("Adding key {} --> {}".format(isokey, extra_dict))
                package_dict['extras'].append({'key': isokey, 'value': json.dumps(extracted_list)})

        # extract list of info for index
        for isokey, isodictkey, extrakey in [
                ('gmi-instrument', 'code', EKOE_INSTRUMENT),
        ]:
            if isokey in iso_values:
                isolist = iso_values[isokey]
                extracted_list = [isodict[isodictkey] for isodict in isolist]
                package_dict['extras'].append({'key': extrakey, 'value': json.dumps(extracted_list)})

        # Map keywords
        tags = []
        wk_thesauri = {}
        other_thesauri = {}
        for keyword in iso_values.get('keywords', []):
            # log.info("KEYWORD {}".format(keyword))
            if keyword['class'] in NGMP_TYPES:
                # There may be multiple gmd:keyword nodes inside a gmd:descriptiveKeywords/gmd:MD_Keywords node,
                # but the local-name will take the first one; we're assuming all of them have the same class
                k = keyword['class']
                wk_thesauri[k] = wk_thesauri.get(k, []) + keyword['any']
            elif keyword.get('thesaurus_href',None) in CMRE_WK_THESAURI_HREF.keys():
                k = CMRE_WK_THESAURI_HREF[keyword['thesaurus_href']]
                wk_thesauri[k] = wk_thesauri.get(k, []) + keyword['any']
            elif keyword['thesaurus_title']:
                k = keyword['thesaurus_title']
                other_thesauri[k] = other_thesauri.get(k, []) + keyword['any']
            else:
                # save as tags free keywords only
                tags += keyword['any']

        package_dict['tags'] = tags

        for wkt, kwlist in wk_thesauri.items():
            # log.info("Creating WK extras '{}':{}".format(wkt, kwlist))
            package_dict['extras'].append({'key': wkt, 'value': json.dumps(kwlist)})

        # log.info("Creating OT extras {}".format(other_thesauri))
        package_dict['extras'].append({'key': 'controlled_keywords', 'value': json.dumps(other_thesauri)})

        if len(iso_values['bbox']) > 0:
            bbox = iso_values['bbox'][0]
            box_dict = {
                'n':bbox['north'],
                's':bbox['south'],
                'e':bbox['east'],
                'w':bbox['west']
            }
            package_dict['extras'].append({'key': 'bbox-string', 'value': json.dumps(box_dict)})

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
