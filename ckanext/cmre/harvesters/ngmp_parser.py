import logging
from lxml import etree

from ckanext.spatial.model import (
    ISODocument,
    ISOElement,
    ISOBrowseGraphic,
    ISOKeyword,
    MappedXmlElement,
    ISOResponsibleParty
)
from ckanext.cmre.harvesters.utils import _my_log


log = logging.getLogger(__name__)

NGMP_GeospatialInformationTypeCode = 'NGMP_GeospatialInformationTypeCode'
NGMP_GeoreferencingLevelCode = 'NGMP_GeoreferencingLevelCode'
NGMP_RepresentationFormCode = 'NGMP_RepresentationFormCode'
NGMP_ThematicCode = 'NGMP_ThematicCode'
NGMP_BaselineLevelCode = 'NGMP_BaselineLevelCode'
NGMP_DesignationTypeCode = 'NGMP_DesignationTypeCode'

NGMP_TYPES = [NGMP_GeoreferencingLevelCode, NGMP_GeospatialInformationTypeCode,
              NGMP_RepresentationFormCode, NGMP_ThematicCode,
              NGMP_BaselineLevelCode, NGMP_DesignationTypeCode]

# Extend/patch the ISODocument definitions by adding some more useful elements
log.info('CMRE EKOE harvester: extending ISODocument')


def _get_iso_elem(source_iso_elem, name):
    for el in source_iso_elem.elements:
        if el.name == name:
            return el
    return None


_get_iso_elem(ISOBrowseGraphic, "file").search_paths.append("gmd:fileName/gmx:Anchor/text()")

for el in (
        ISOElement(
            name="thesaurus_title",
            search_paths=[
                "gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()",
                "gmd:thesaurusName/gmd:CI_Citation/gmd:title/gmx:Anchor/text()",
            ],
            multiplicity="0..1",
            ),
        ISOElement(
            name="thesaurus_href",
            search_paths=[
                "gmd:thesaurusName/gmd:CI_Citation/gmd:title/gmx:Anchor/@xlink:href",
            ],
            multiplicity="0..1",
            ),
        ISOElement(
            name="any",
            search_paths=[
                "gmd:keyword/*/text()",
            ],
            multiplicity="*",
        ),
        ISOElement(
            name="class",
            search_paths=[
                "local-name(gmd:keyword/*)",
            ],
            multiplicity="1",
        )
):
    ISOKeyword.elements.append(el)


# monkey patching MappedXmlElement.get_values bc original one does not support xpath returning plain strings
def MappedXmlElement_get_values(self, elements):
    values = []
    # log.info("MXE === Returning str object ({}) [{}]".format(type(elements), elements))
    if len(elements) == 0:
        pass
    elif type(elements) in [ str, etree._ElementStringResult]:
        # log.info("MXE Returning str object [{}]".format(elements))
        return [ elements ]
    else:
        for element in elements:
            value = self.get_value(element)
            values.append(value)
    return values


MappedXmlElement.get_values = MappedXmlElement_get_values


class NgmpElement(ISOElement):
    namespaces = {
        "gts": "http://www.isotc211.org/2005/gts",
        "gml": "http://www.opengis.net/gml",
        "gml32": "http://www.opengis.net/gml/3.2",
        "gmx": "http://www.isotc211.org/2005/gmx",
        "gsr": "http://www.isotc211.org/2005/gsr",
        "gss": "http://www.isotc211.org/2005/gss",
        "gco": "http://www.isotc211.org/2005/gco",
        "gmd": "http://www.isotc211.org/2005/gmd",
        "srv": "http://www.isotc211.org/2005/srv",
        "xlink": "http://www.w3.org/1999/xlink",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        # NGMP specific namespaces
        "gmi": "http://standards.iso.org/iso/19115/-2/gmi/1.0",  # ISO19115-2:2009 specific
        "ngmp": "urn:int:nato:geometoc:geo:metadata:ngmp:1.0"
    }


class ISOSecurityConstraints(ISOElement):
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


class GMIInstrument(NgmpElement):
    elements = [
        NgmpElement(
            name="code",
            search_paths=[
                "gmi:identifier/gmd:RS_Identifier/gmd:code/*/text()",
            ],
            multiplicity="1",
        ),
        NgmpElement(
            name="codespace",
            search_paths=[
                "gmi:identifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString/text()",
            ],
            multiplicity="1",
        ),
        NgmpElement(
            name="type",
            search_paths=[
                "gmi:type/gco:CharacterString/text()",
            ],
            multiplicity="1",
        ),
        NgmpElement(
            name="description",
            search_paths=[
                "gmi:description/gco:CharacterString/text()",
            ],
            multiplicity="1",
        )
    ]


class GMIPlatform(NgmpElement):
    elements = [
        NgmpElement(
            name="code",
            search_paths=[
                "gmi:identifier/gmd:RS_Identifier/gmd:code/*/text()",
            ],
            multiplicity="1",
        ),
        NgmpElement(
            name="codespace",
            search_paths=[
                "gmi:identifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString/text()",
            ],
            multiplicity="1",
        ),
        NgmpElement(
            name="description",
            search_paths=[
                "gmi:description/gco:CharacterString/text()",
            ],
            multiplicity="1",
        )
    ]


class GMIOperation(NgmpElement):
    elements = [
        NgmpElement(
            name="code",
            search_paths=[
                "gmi:identifier/gmd:MD_Identifier/gmd:code/*/text()",
            ],
            multiplicity="1",
        ),
    ]


class ISOVerticalExtent(ISOElement):
    elements = [
        ISOElement(
            name="min",
            search_paths=[
                "gmd:minimumValue/gco:Real/text()",
            ],
            multiplicity="0..1"
        ),
        ISOElement(
            name="max",
            search_paths=[
                "gmd:maximumValue/gco:Real/text()",
            ],
            multiplicity="0..1"
        ),
        ISOElement(
            name="crs-title",
            search_paths=[
                "gmd:verticalCRS/text()",
            ],
            multiplicity="0..1"
        ),
        ISOElement(
            name="crs-href",
            search_paths=[
                "gmd:verticalCRS/@xlink:href",
            ],
            multiplicity="0..1"
        ),
    ]


class ISOAddress(ISOElement):
    elements = [
       ISOElement(
           name="delivery-point",
           search_paths=[
               "gmd:deliveryPoint/gco:CharacterString/text()",
           ],
           multiplicity="0..1"
       ),
       ISOElement(
           name="city",
           search_paths=[
               "gmd:city/gco:CharacterString/text()",
           ],
           multiplicity="0..1"
       ),
       ISOElement(
           name="postal-code",
           search_paths=[
               "gmd:postalCode/gco:CharacterString/text()",
           ],
           multiplicity="0..1"
       ),
       ISOElement(
           name="country",
           search_paths=[
               "gmd:country/gco:CharacterString/text()",
           ],
           multiplicity="0..1"
       ),
       ISOElement(
           name="mail",
           search_paths=[
               "gmd:electronicMailAddress/gco:CharacterString/text()",
           ],
           multiplicity="0..1"
       ),
    ]


_get_iso_elem(ISOResponsibleParty, "contact-info").elements.append(
    ISOAddress(
        name="address",
        search_paths=[
            "gmd:address/gmd:CI_Address",
        ],
        multiplicity="0..1",
    ))


class ISOLISource(ISOElement):
    elements = [
        ISOElement(
            name="description",
            search_paths=["gmd:description/gco:CharacterString/text()",],
            multiplicity="0..1",
        ),
        ISOElement(
            name="title",
            search_paths=["gmd:sourceCitation/gmd:CI_Citation/gmd:title/*/text()"],
            multiplicity="0..1",
        ),
        ISOElement(
            name="title_href",
            search_paths=["gmd:sourceCitation/gmd:CI_Citation/gmd:title/gmx:Anchor/@xlink:href", ],
            multiplicity="0..1",
        ),
    ]


class ISOLIProcessStep(ISOElement):
    elements = [
        ISOElement(
            name="description",
            search_paths=["gmd:description/gco:CharacterString/text()"],
            multiplicity="1",
        ),
        ISOElement(
            name="date",
            search_paths=["gmd:dateTime/gco:DateTime/text()"],
            multiplicity="0..1",
        ),
        ISOElement(
            name="organization",
            search_paths=["gmd:processor/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString/text()"],
            multiplicity="*",
        ),
    ]


class EKOEDocument(ISODocument):
    _my_log("EKOEDocument")
    elements = [e for e in ISODocument.elements]

    for element in [
        ISOElement(
            name="owner_org",
            search_paths=[
                'gmd:identificationInfo/*/gmd:pointOfContact/gmd:CI_ResponsibleParty'
                '[gmd:role/gmd:CI_RoleCode/@codeListValue="owner"]/gmd:organisationName/gco:CharacterString/text()',
            ],
            multiplicity="*"
        ),
        ISOSecurityConstraints(
            name="resource-security",
            search_paths=[
                "gmd:identificationInfo/*/gmd:resourceConstraints/gmd:MD_SecurityConstraints"
            ],
            multiplicity="0..1"
        ),
        ISOSecurityConstraints(
            name="metadata-security",
            search_paths=[
                "gmd:metadataConstraints/gmd:MD_SecurityConstraints"
            ],
            multiplicity="0..1"
        ),
        NgmpElement(
            name="ngmp-resource-releasibility",
            search_paths=[
                "gmd:identificationInfo/*/gmd:resourceConstraints/ngmp:NGMP_Constraints/ngmp:releasibility/ngmp:NGMP_Releasibility/ngmp:statement/gco:CharacterString/text()",
            ],
            multiplicity="1"
        ),
        ISOVerticalExtent(
            name="vertical-extent",
            search_paths=[
                "gmd:identificationInfo/*/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent",
            ],
            multiplicity="*"
        ),
        GMIInstrument(
            name="gmi-instrument",
            search_paths=[
                "gmi:acquisitionInformation/gmi:MI_AcquisitionInformation/gmi:instrument/gmi:MI_Instrument",
            ],
            multiplicity="*"
        ),
        GMIPlatform(
            name="gmi-platform",
            search_paths=[
                "gmi:acquisitionInformation/gmi:MI_AcquisitionInformation/gmi:platform/gmi:MI_Platform",
            ],
            multiplicity="1"
        ),
        GMIOperation(
            name="gmi-operation",
            search_paths=[
                "gmi:acquisitionInformation/gmi:MI_AcquisitionInformation/gmi:operation/gmi:MI_Operation",
            ],
            multiplicity="*"
        ),
        ISOResponsibleParty(
            name="data-resp-party",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty",
            ],
            multiplicity="1..*",
        ),
        ISOResponsibleParty(
            name="metadata-resp-party",
            search_paths=[
                "gmd:contact/gmd:CI_ResponsibleParty",
            ],
            multiplicity="1..*",
        ),
        ISOElement(
            name="fileid",
            search_paths="gmd:fileIdentifier/*/text()",
            multiplicity="0..1",
        ),
        ISOElement(
            name="filehref",
            search_paths="gmd:fileIdentifier/gmx:Anchor/@xlink:href",
            multiplicity="0..1",
        ),
        ISOElement(
            name="parentid",
            search_paths="gmd:parentIdentifier/*/text()",
            multiplicity="0..1",
        ),
        ISOElement(
            name="parenthref",
            search_paths="gmd:parentIdentifier/gmx:Anchor/@xlink:href",
            multiplicity="0..1",
        ),
        ISOLISource(
            name="sources",
            search_paths=[
                "gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:source/gmd:LI_Source",
            ],
            multiplicity="*",
        ),
        ISOLIProcessStep(
            name="process-step",
            search_paths=[
                "gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:processStep/gmd:LI_ProcessStep",
            ],
            multiplicity="*",
        ),

    ]:
        log.info('Adding NGMP element {}'.format(element.name))
        elements.append(element)

    for element in elements:
        # minor workaround from EKOE bad data
        if element.name == "extent-free-text":
            element.search_paths = [
                "gmd:identificationInfo/*/*[local-name()='extent']/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicDescription/gmd:geographicIdentifier/*/gmd:code/gco:CharacterString/text()",
            ]
        elif element.name == "temporal-extent-begin":
            element.search_paths= [
                "gmd:identificationInfo/*/*[local-name()='extent']/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/*[local-name()='TimePeriod']/*[local-name()='beginPosition']/text()",
                "gmd:identificationInfo/*/*[local-name()='extent']/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/*[local-name()='TimePeriod']/*[local-name()='begin']/*[local-name()='TimeInstant']/*[local-name()='timePosition']/text()",
            ]
        elif element.name == "temporal-extent-end":
            element.search_paths= [
                "gmd:identificationInfo/*/*[local-name()='extent']/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/*[local-name()='TimePeriod']/*[local-name()='endPosition']/text()",
                "gmd:identificationInfo/*/*[local-name()='extent']/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/*[local-name()='TimePeriod']/*[local-name()='end']/*[local-name()='TimeInstant']/*[local-name()='timePosition']/text()",
            ]




    def get_xml_tree(self):
        _my_log("call get_xml_tree")
        import six
        if self.xml_tree is None:
            _my_log("xml_tree is none")
            # parser = etree.XMLParser(remove_blank_text=True)
            # xml_str = six.ensure_str(self.xml_str)
            # self.xml_tree = etree.fromstring(xml_str, parser=parser)
            parser = etree.XMLParser(remove_blank_text=True, encoding='utf-8')
            xml_str = six.ensure_str(self.xml_str)
            self.xml_tree = etree.fromstring(xml_str.encode('utf-8'), parser=parser)
            _my_log("if done")


        return self.xml_tree