import logging
import datetime
import json
from pylons import config
from dateutil.parser import parse

from ckan.plugins.core import SingletonPlugin

from ckanext.cmre.harvesters.fs import FileSystemHarvester

from ckanext.spatial.model import (ISODocument, ISOElement, ISOResponsibleParty)


log = logging.getLogger(__name__)

# Extend the ISODocument definitions by adding some more useful elements

log.info('CMRE EKOE harvester: extending ISODocument')

# ISODocument.elements.append(
#     ISOElement(
#         name="legal-use-constraints",
#         search_paths=[
#             "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString/text()",
#             "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString/text()"
#         ],
#         multiplicity="*"
#     )
# )
#
# ISODocument.elements.append(
#     ISOElement(
#         name="ngmp-security-classification-code",
#         search_paths=[
#            "gmd:metadataConstraints/gmd:MD_SecurityConstraints/gmd:classification/gmd:MD_ClassificationCode[@codeList='http://eden.ign.fr/xsd/ngmp/20110916/resources/codelist/ngmpCodelists.xml#MD_ClassificationCode']/text()"
#         ],
#         multiplicity="0..1"
#     )
# )

class EKOEClassification(ISOElement):
    elements = [
        ISOElement(
            name="code",
            search_paths=[
                "gmd:classification/gmd:MD_ClassificationCode/@codeListValue",
            ],
            multiplicity="1",
        ),
        ISOElement(
            name="name",
            search_paths=[
                "gmd:classification/gmd:MD_ClassificationCode/text()",
            ],
            multiplicity="0..1",
        ),
        ISOElement(
            name="classification",
            search_paths=[
                "gmd:classificationSystem/gco:CharacterString/text()",
            ],
            multiplicity="1",
        )
    ]

ISODocument.elements.append(
    EKOEClassification(
        name="ekoe-classification",
        search_paths=[
           "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_SecurityConstraints[gmd:classification/gmd:MD_ClassificationCode/@codeList='http://eden.ign.fr/xsd/ngmp/20110916/resources/codelist/ngmpCodelists.xml#MD_ClassificationCode']"
        ],
        multiplicity="0..1"
    )
)

ISODocument.elements.append(
    ISOElement(
        name="vertical-extent-min",
        search_paths=[
            "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:minimumValue/gco:Real/text()",
            "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:minimumValue/gco:Real/text()"
        ],
        multiplicity="*"
    )
)

ISODocument.elements.append(
    ISOElement(
        name="vertical-extent-max",
        search_paths=[
            "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:maximumValue/gco:Real/text()",
            "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:maximumValue/gco:Real/text()"
        ],
        multiplicity="*"
    )
)

ISODocument.elements.append(
    ISOElement(
        name="vertical-extent-crs-title",
        search_paths=[
            "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:verticalCRS/@xlink:title",
            "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:verticalCRS/@xlink:title"
        ],
        multiplicity="*"
    )
)

ISODocument.elements.append(
    ISOElement(
        name="owner_org",
        search_paths=[
            'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty[gmd:role/gmd:CI_RoleCode/@codeListValue="owner"]/gmd:organisationName/gco:CharacterString/text()',
            'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty[gmd:role/gmd:CI_RoleCode/@codeListValue="owner"]/gmd:organisationName/gco:CharacterString/text()',
        ],
        multiplicity="*"
    )
),

ISODocument.elements.append(
    ISOElement(
        name="keyword-trial",
        search_paths=[
            'gmd:identificationInfo/*/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()="CMRE Trials"]/gmd:keyword/gco:CharacterString/text()'
        ],
        multiplicity="*"
    )
)

ISODocument.elements.append(
    ISOElement(
        name="keyword-platform",
        search_paths=[
            'gmd:identificationInfo/*/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()="CMRE Platforms"]/gmd:keyword/gco:CharacterString/text()',
            'gmd:identificationInfo/*/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()="CMRE Platforms"]/ngmp:NGMP_GeospatialInformationTypeCode/text()'
        ],
        multiplicity="*"
    )
)

ISODocument.elements.append(
    ISOElement(
        name="keyword-sensor",
        search_paths=[
            'gmd:identificationInfo/*/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()="CMRE Sensors"]/gmd:keyword/gco:CharacterString/text()'
        ],
        multiplicity="*"
    )
)

ISODocument.elements.append(
    ISOElement(
        name="keyword-experiment",
        search_paths=[
            'gmd:identificationInfo/*/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()="CMRE Experiment Types"]/gmd:keyword/gco:CharacterString/text()'
        ],
        multiplicity="*"
    )
)

ISODocument.elements.append(
    ISOElement(
        name="dimension_name",
        search_paths=[
            'gmd:contentInfo/gmd:MD_CoverageDescription/gmd:dimension/gmd:MD_Band/gmd:descriptor/gco:CharacterString/text()'
        ],
        multiplicity="*"
    )
)

class CMREHarvester(FileSystemHarvester, SingletonPlugin):

    def info(self):
        return {
            'name': 'cmre-ekoe',
            'title': 'CMRE EKOE filesystem harvester',
            'description': 'Harvests local documents',
            'form_config_interface': 'Text'
        }

    def get_package_dict(self, iso_values, harvest_object):
        package_dict = super(CMREHarvester, self).get_package_dict(iso_values, harvest_object)

        # log.info('::::::::::::::::: %r', package_dict)

        # OWNER ORGANIZATION
        print("hahah", iso_values.get("owner_org"))
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
            package_dict['extras'].append({'key': "ekoe_classification", 'value': "{system} {code}".format(code=code, system=system).upper()})
        else:
            package_dict['extras'].append({'key': "ekoe_classification", 'value': "PUBLIC RELEASABLE"})


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
