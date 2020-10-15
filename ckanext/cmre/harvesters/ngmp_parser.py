import logging

from ckanext.spatial.model import (ISODocument, ISOElement, ISOBrowseGraphic)

log = logging.getLogger(__name__)

# Extend/patch the ISODocument definitions by adding some more useful elements
log.info('CMRE EKOE harvester: extending ISODocument')

for el in ISOBrowseGraphic.elements:
    if el.name == "file":
        el.search_paths.append("gmd:fileName/gmx:Anchor/text()")


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


class NGMPClassification(ISOElement):
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


def create_keyword_xpath(thesaurus_title):
    return "gmd:identificationInfo/*/gmd:descriptiveKeywords/gmd:MD_Keywords" \
           "[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()='{}']" \
           "/gmd:keyword/gco:CharacterString/text()".format(thesaurus_title)


class EKOEDocument(ISODocument):
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
        ISOElement(
            name="keyword-sensor",
            search_paths=[
                create_keyword_xpath("CMRE Sensors")
            ],
            multiplicity="*"
        ),
        ISOElement(
            name="keyword-experiment",
            search_paths=[
                create_keyword_xpath("CMRE Experiment Types")
            ],
            multiplicity="*"
        ),
        ISOElement(
            name="keyword-platform",
            search_paths=[
                create_keyword_xpath("CMRE Platforms")
            ],
            multiplicity="*"
        ),
        ISOElement(
            name="keyword-trial",
            search_paths=[
                create_keyword_xpath("CMRE Trials")
            ],
            multiplicity="*"
        ),
        ISOElement(
            name="dimension_name",
            search_paths=[
                'gmd:contentInfo/gmd:MD_CoverageDescription/gmd:dimension/'
                'gmd:MD_Band/gmd:descriptor/gco:CharacterString/text()',
            ],
            multiplicity="*"
        ),
        NGMPClassification(
            name="ekoe-classification",
            search_paths=[
                "gmd:identificationInfo/*/gmd:resourceConstraints/gmd:MD_SecurityConstraints"
                "[gmd:classification/gmd:MD_ClassificationCode/@codeList="
                "'http://eden.ign.fr/xsd/ngmp/20110916/resources/codelist/ngmpCodelists.xml#MD_ClassificationCode']",
            ],
            multiplicity="0..1"
        ),
        ISOElement(
            name="vertical-extent-min",
            search_paths=[
                "gmd:identificationInfo/*/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:minimumValue/gco:Real/text()",
            ],
            multiplicity="*"
        ),
        ISOElement(
            name="vertical-extent-max",
            search_paths=[
                "gmd:identificationInfo/*/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:maximumValue/gco:Real/text()",
            ],
            multiplicity="*"
        ),
        ISOElement(
            name="vertical-extent-crs-title",
            search_paths=[
                "gmd:identificationInfo/*/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent/gmd:verticalCRS/@xlink:title",
            ],
            multiplicity="*"
        )

    ]:
        elements.append(e)
