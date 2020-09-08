from ckanext.cmre.harvesters.fs import FileSystemHarvester
from ckanext.spatial.model.harvested_metadata import MappedXmlDocument
from ckanext.spatial.model import ISOElement


class ISO19115_3Document(MappedXmlDocument):
    elements = []


ISO19115_3Document.elements.append(
    ISOElement(
        name="example-value",
        search_paths=[
            'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty[gmd:role/gmd:CI_RoleCode/@codeListValue="owner"]/gmd:organisationName/gco:CharacterString/text()',
            'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty[gmd:role/gmd:CI_RoleCode/@codeListValue="owner"]/gmd:organisationName/gco:CharacterString/text()',
            "gmd:contact/gmd:CI_ResponsibleParty",
        ],
        multiplicity="*"
    )
),


class ISO19115_3Harvester(FileSystemHarvester):
    '''
    A Harvester for local filesystem directory containing spatial metadata documents.
    '''

    def info(self):
        return {
            'name': 'iso19115-3-harvester',
            'title': 'iso19115-3 Spatial metadata on Local Filesystem',
            'description': 'A local filesystem directory containing a list of spatial metadata documents'
            }

    def import_stage(self, harvest_object):
        iso_parser = ISO19115_3Document(harvest_object.content)
        iso_values = iso_parser.read_values()
        print('iso values', iso_values.get('example-value'))
