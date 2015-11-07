
import json

import logging

from ckan.plugins.core import SingletonPlugin

from ckanext.spatial.model import ISODocument
from ckanext.spatial.model import ISOElement
from ckanext.spatial.model import ISOResponsibleParty
from ckanext.spatial.model import ISOKeyword

from ckan.logic import ValidationError, NotFound, get_action

from pylons import config
from datetime import datetime

log = logging.getLogger(__name__)

# Extend the ISODocument definitions by adding some more useful elements

log.info('GeoNetwork CSW (CMRE) harvester: extending ISODocument')

ISODocument.elements.append(
    ISOElement(
        name="legal-use-constraints",
        search_paths=[
            "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString/text()",
            "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString/text()",
        ],
        multiplicity="*",
    ),
    ISOElement(
        name="ngmp-security-classification-code",
        search_paths=[
           "gmd:metadataConstraints/gmd:MD_SecurityConstraints/gmd:classification/gmd:MD_ClassificationCode[@codeList='http://eden.ign.fr/xsd/ngmp/20110916/resources/codelist/ngmpCodelists.xml#MD_ClassificationCode']/text()",
        ],
        multiplicity="0..1",
    ),
    ISOElement(
        name="ngmp-security-classification-system",
        search_paths=[
           "gmd:metadataConstraints/gmd:MD_SecurityConstraints[gmd:classification/gmd:MD_ClassificationCode/@codeList='http://eden.ign.fr/xsd/ngmp/20110916/resources/codelist/ngmpCodelists.xml#MD_ClassificationCode']/gmd:classificationSystem/gco:CharacterString/text()",
        ],
        multiplicity="0..1",
    ),

    ## Already added by the base CSW harvester
    #ISOElement(
    #    name="temporal-extent-begin",
    #    search_paths=[
    #        "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition/text()",
    #        "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition/text()",
    #    ],
    #    multiplicity="*",
    #),

    ## Already added by the GeoNetwork harvester
    #ISOElement(
    #    name="temporal-extent-end",
    #    search_paths=[
    #        "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition/text()",
    #        "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition/text()",
    #    ],
    #    multiplicity="*",
    #),
    #ISOElement(
    #    name="temporal-extent-instant",
    #    search_paths=[
    #        "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimeInstant/gml:timePosition/text()",
    #        "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimeInstant/gml:timePosition/text()",
    #    ],
    #    multiplicity="*",
    #),
    ISOElement(
        name="vertical-extent-min",
        search_paths=[
            "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:minimumValue/gco:Real/text()",
            "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:minimumValue/gco:Real/text()",
        ],
        multiplicity="*",
    ),
    ISOElement(
        name="vertical-extent-max",
        search_paths=[
            "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:maximumValue/gco:Real/text()",
            "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:maximumValue/gco:Real/text()",
        ],
        multiplicity="*",
    ),
    ISOElement(
        name="vertical-extent-crs-title",
        search_paths=[
            "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:verticalCRS/@xlink:title",
            "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:verticalCRS/@xlink:title",
        ],
        multiplicity="*",
    )
)


class CMREHarvester(GeoNetworkHarvester, SingletonPlugin):

    def info(self):
        return {
            'name': 'cmre',
            'title': 'GeoNetwork CSW server (CMRE)',
            'description': 'Harvests CWS from CMRE GeoNetwork',
            'form_config_interface': 'Text'
        }

    def get_package_dict(self, iso_values, harvest_object):
        package_dict = super(CMREHarvester, self).get_package_dict(iso_values, harvest_object)        
        
        # LEGAL CONSTRAINTS
        if len(iso_values.get('legal-use-constraints', [])):
            package_dict['extras'].append({'key': 'use-limitation', 'value': iso_values['legal-use-constraints'][0]})
        
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
                package_dict['extras'].append({'key': 'vertical-extent', 'value': vert_ext_min + ' / ' + vert_ext_max + ' ' + crs_title})

        # TEMPORAL ELEMENTS
        if len(iso_values.get('temporal-extent-instant', [])):
            tempstr = iso_values['temporal-extent-instant'][0]

            if 'Z' not in tempstr:
                package_dict['extras'].append({'key': 'temporal-extent-instant', 'value': iso_values['temporal-extent-instant'][0] + 'Z'})
            else:
                package_dict['extras'].append({'key': 'temporal-extent-instant', 'value': iso_values['temporal-extent-instant'][0]})

        for key in ['temporal-extent-begin', 'temporal-extent-end']:
            if len(iso_values[key]) > 0:
                tempstr = iso_values[key][0]
        if 'Z' not in tempstr:
            package_dict['extras'][key] = iso_values[key][0] + 'Z'
        else:
            package_dict['extras'][key] = iso_values[key][0]        
            
        # SECURITY CLASSIFICATION
        for name in ['ngmp-security-classification-code', 'ngmp-security-classification-system']:
           val = iso_values.get(name)
           if val:
              package_dict['extras'].append({'key': name, 'value': val})

        # End of processing, return the modified package
        return package_dict