from ckanext.spatial.model import (ISOAggregationInfo,
                                   ISODocument, ISOElement,
                                   ISOUsage)


class ISO19115_3Element(ISOElement):
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
        "mdb": "http://standards.iso.org/iso/19115/-3/mdb/1.0",
        "gco": "http://standards.iso.org/iso/19115/-3/gco/1.0",
        "mcc": "http://standards.iso.org/iso/19115/-3/mcc/1.0",
        "lan": "http://standards.iso.org/iso/19115/-3/lan/1.0",
        "cit": "http://standards.iso.org/iso/19115/-3/cit/1.0",
        "gex": "http://standards.iso.org/iso/19115/-3/gex/1.0",
        "mco": "http://standards.iso.org/iso/19115/-3/mco/1.0",
        "mri": "http://standards.iso.org/iso/19115/-3/mri/1.0",
        "mrc": "http://standards.iso.org/iso/19115/-3/mrc/1.0",
        "mrd": "http://standards.iso.org/iso/19115/-3/mrd/1.0",
        "mda": "http://standards.iso.org/iso/19115/-3/mda/1.0",
        "mrl": "http://standards.iso.org/iso/19115/-3/mrl/1.0",
        "mrs": "http://standards.iso.org/iso/19115/-3/mrs/1.0",
        "msr": "http://standards.iso.org/iso/19115/-3/msr/1.0",
        "mmi": "http://standards.iso.org/iso/19115/-3/mmi/1.0",
        "srv": "http://standards.iso.org/iso/19115/-3/srv/2.0",
        "gfc": "http://standards.iso.org/iso/19110/gfc/1.1",
        "fcc": "http://standards.iso.org/iso/19110/fcc/1.0",
        "gml":  "http://www.opengis.net/gml/3.2",
    }

class EKOEClassification(ISO19115_3Element):
    elements = [
        ISO19115_3Element(
            name="code",
            search_paths=[
                "gmd:classification/gmd:MD_ClassificationCode/@codeListValue",
                "mco:classification/mco:MD_ClassificationCode/@codeListValue"
            ],
            multiplicity="1",
        ),
        ISO19115_3Element(
            name="name",
            search_paths=[
                "gmd:classification/gmd:MD_ClassificationCode/text()",
                "mco:classification/mco:MD_ClassificationCode/text()"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="classification",
            search_paths=[
                "gmd:classificationSystem/gco:CharacterString/text()",
            ],
            multiplicity="1",
        )
    ]

class ISOBoundingBox(ISO19115_3Element):
    elements = [
        ISO19115_3Element(
            name="west",
            search_paths=[
                "gmd:westBoundLongitude/gco:Decimal/text()",
                "gex:westBoundLongitude/gco:Decimal/text()"
            ],
            multiplicity="1",
        ),
        ISO19115_3Element(
            name="east",
            search_paths=[
                "gmd:eastBoundLongitude/gco:Decimal/text()",
                "gex:eastBoundLongitude/gco:Decimal/text()"
            ],
            multiplicity="1",
        ),
        ISO19115_3Element(
            name="north",
            search_paths=[
                "gmd:northBoundLatitude/gco:Decimal/text()",
                "gex:northBoundLatitude/gco:Decimal/text()"
            ],
            multiplicity="1",
        ),
        ISO19115_3Element(
            name="south",
            search_paths=[
                "gmd:southBoundLatitude/gco:Decimal/text()",
                "gex:southBoundLatitude/gco:Decimal/text()"
            ],
            multiplicity="1",
        ),
    ]

class ISODataFormat(ISO19115_3Element):

    elements = [
        ISO19115_3Element(
            name="name",
            search_paths=[
                "gmd:name/gco:CharacterString/text()",
                "cit:title/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="version",
            search_paths=[
                "gmd:version/gco:CharacterString/text()",
                "cit:edition/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
    ]

class ISOBrowseGraphic(ISO19115_3Element):

    elements = [
        ISO19115_3Element(
            name="file",
            search_paths=[
                "gmd:fileName/gco:CharacterString/text()",
                "mcc:fileName/gco:CharacterString/text()"
            ],
            multiplicity="1",
        ),
        ISO19115_3Element(
            name="description",
            search_paths=[
                "gmd:fileDescription/gco:CharacterString/text()",
                "mcc:fileDescription/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="type",
            search_paths=[
                "gmd:fileType/gco:CharacterString/text()",
                "mcc:fileType/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
    ]

class ISOKeyword(ISO19115_3Element):

    elements = [
        ISO19115_3Element(
            name="keyword",
            search_paths=[
                "gmd:keyword/gco:CharacterString/text()",
                "mri:keyword/gco:CharacterString/text()"
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="type",
            search_paths=[
                "gmd:type/gmd:MD_KeywordTypeCode/@codeListValue",
                "gmd:type/gmd:MD_KeywordTypeCode/text()",
                "mri:type/mri:MD_KeywordTypeCode/text()"
            ],
            multiplicity="0..1",
        ),
        # If Thesaurus information is needed at some point, this is the
        # place to add it
   ]

class ISOResourceLocator(ISO19115_3Element):

    elements = [
        ISO19115_3Element(
            name="url",
            search_paths=[
                "gmd:linkage/gmd:URL/text()",
                "cit:linkage/gco:CharacterString/text()"
            ],
            multiplicity="1",
        ),
        ISO19115_3Element(
            name="function",
            search_paths=[
                "gmd:function/gmd:CI_OnLineFunctionCode/@codeListValue",
                "cit:function/cit:CI_OnLineFunctionCode/@codeListValue"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="name",
            search_paths=[
                "gmd:name/gco:CharacterString/text()",
                "gmd:name/gmx:MimeFileType/text()",
                "cit:name/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="description",
            search_paths=[
                "gmd:description/gco:CharacterString/text()",
                "cit:description/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="protocol",
            search_paths=[
                "gmd:protocol/gco:CharacterString/text()",
                "cit:protocol/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
    ]

class ISOReferenceDate(ISO19115_3Element):

    elements = [
        ISO19115_3Element(
            name="type",
            search_paths=[
                "gmd:dateType/gmd:CI_DateTypeCode/@codeListValue",
                "gmd:dateType/gmd:CI_DateTypeCode/text()",
                "cit:dateType/cit:CI_DateTypeCode/@codeListValue"
            ],
            multiplicity="1",
        ),
        ISO19115_3Element(
            name="value",
            search_paths=[
                "gmd:date/gco:Date/text()",
                "gmd:date/gco:DateTime/text()",
                "cit:date/gco:DateTime/text()"
            ],
            multiplicity="1",
        ),
    ]

class ISOCoupledResources(ISO19115_3Element):

    elements = [
        ISO19115_3Element(
            name="title",
            search_paths=[
                "@xlink:title",
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="href",
            search_paths=[
                "@xlink:href",
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="uuid",
            search_paths=[
                "@uuidref",
            ],
            multiplicity="*",
        ),

    ]


class ISOResponsibleParty(ISO19115_3Element):
    elements = [
        ISO19115_3Element(
            name="individual-name",
            search_paths=[
                "gmd:individualName/gco:CharacterString/text()",
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="organisation-name",
            search_paths=[
                "gmd:organisationName/gco:CharacterString/text()",
                "cit:party/cit:CI_Organisation/cit:name/gco:CharacterString/text()",
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="position-name",
            search_paths=[
                "gmd:positionName/gco:CharacterString/text()",
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="contact-info",
            search_paths=[
                "gmd:contactInfo/gmd:CI_Contact",
                "cit:party/cit:CI_Organisation/cit:contactInfo/cit:CI_Contact"
            ],
            multiplicity="0..1",
            elements = [
                ISO19115_3Element(
                    name="email",
                    search_paths=[
                        "gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString/text()",
                        "cit:address/cit:CI_Address/cit:electronicMailAddress/gco:CharacterString/text()"
                    ],
                    multiplicity="0..1",
                ),
                ISOResourceLocator(
                    name="online-resource",
                    search_paths=[
                        "gmd:onlineResource/gmd:CI_OnlineResource",
                    ],
                    multiplicity="0..1",
                ),
            ]
        ),
        ISO19115_3Element(
            name="role",
            search_paths=[
                "gmd:role/gmd:CI_RoleCode/@codeListValue",
                "cit:role/cit:CI_RoleCode/@codeListValue"
            ],
            multiplicity="0..1",
        ),
    ]


class ISO19115_3Document(ISODocument):
    elements = [
        ISO19115_3Element(
            name="guid",
            search_paths=[
                "gmd:fileIdentifier/gco:CharacterString/text()",
                "mdb:metadataIdentifier/mcc:MD_Identifier/mcc:codeSpace/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="metadata-language",
            search_paths=[
                "gmd:language/gmd:LanguageCode/@codeListValue",
                "gmd:language/gmd:LanguageCode/text()",
                "gmd:language/gco:CharacterString/text()",
                "mdb:defaultLocale/lan:PT_Locale/lan:language/lan:LanguageCode/@codeListValue"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="metadata-standard-name",
            search_paths="gmd:metadataStandardName/gco:CharacterString/text()",
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="metadata-standard-version",
            search_paths="gmd:metadataStandardVersion/gco:CharacterString/text()",
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="resource-type",
            search_paths=[
                "gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue",
                "gmd:hierarchyLevel/gmd:MD_ScopeCode/text()",
                "mdb:resourceLineage/mrl:LI_Lineage/mrl:scope/mcc:MD_Scope/mcc:level/mcc:MD_ScopeCode/@codeListValue"
            ],
            multiplicity="*",
        ),
        ISOResponsibleParty(
            name="metadata-point-of-contact",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty",
                "mdb:contact/cit:CI_Responsibility"
            ],
            multiplicity="1..*",
        ),
        ISO19115_3Element(
            name="metadata-date",
            search_paths=[
                "gmd:dateStamp/gco:DateTime/text()",
                "mdb:dateInfo/cit:CI_Date/cit:date/gco:DateTime/text()",
                "gmd:dateStamp/gco:Date/text()",
            ],
            multiplicity="1",
        ),
        ISO19115_3Element(
            name="spatial-reference-system",
            search_paths=[
                "gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString/text()",
                "mdb:referenceSystemInfo/mrs:MD_ReferenceSystem/mrs:referenceSystemType/mrs:MD_ReferenceSystemTypeCode/@codeListValue"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="title",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString/text()",
                "mdb:metadataIdentifier/mcc:MD_Identifier/mcc:authority/cit:CI_Citation/cit:title/gco:CharacterString/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString/text()",
            ],
            multiplicity="1",
        ),
        ISO19115_3Element(
            name="alternate-title",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:alternateTitle/gco:CharacterString/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:alternateTitle/gco:CharacterString/text()",
                "mdb:alternativeMetadataReference/cit:CI_Citation/cit:title/gco:CharacterString/text()",
                "mdb:metadataStandard/cit:CI_Citation/cit:title/gco:CharacterString/text()",
            ],
            multiplicity="*",
        ),
        ISOReferenceDate(
            name="dataset-reference-date",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:citation/cit:CI_Citation/cit:date/cit:CI_Date"
            ],
            multiplicity="1..*",
        ),
        ISO19115_3Element(
            name="unique-resource-identifier",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()",
                "gmd:identificationInfo/gmd:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:citation/cit:CI_Citation/cit:identifier/mcc:MD_Identifier/mcc:code/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="presentation-form",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode/text()",
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode/@codeListValue",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:presentationForm/gmd:CI_PresentationFormCode/@codeListValue",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/cit:presentationForm/cit:CI_PresentationFormCode/@codeListValue"

            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="abstract",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:abstract/gco:CharacterString/text()",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:abstract/gco:CharacterString/text()"
            ],
            multiplicity="1",
        ),
        ISO19115_3Element(
            name="purpose",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:purpose/gco:CharacterString/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:purpose/gco:CharacterString/text()",
            ],
            multiplicity="0..1",
        ),
        ISOResponsibleParty(
            name="responsible-organisation",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty",
                "gmd:contact/gmd:CI_ResponsibleParty",
                "mdb:contact/cit:CI_Responsibility"
            ],
            multiplicity="1..*",
        ),
        ISO19115_3Element(
            name="frequency-of-update",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode/@codeListValue",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode/@codeListValue",
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceAndUpdateFrequency/gmd:MD_MaintenanceFrequencyCode/text()",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:resourceMaintenance/mmi:MD_MaintenanceInformation/mmi:maintenanceAndUpdateFrequency/mmi:MD_MaintenanceFrequencyCode/text()"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="maintenance-note",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceNote/gco:CharacterString/text()",
                "gmd:identificationInfo/gmd:SV_ServiceIdentification/gmd:resourceMaintenance/gmd:MD_MaintenanceInformation/gmd:maintenanceNote/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="progress",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status/gmd:MD_ProgressCode/@codeListValue",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:status/gmd:MD_ProgressCode/@codeListValue",
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:status/gmd:MD_ProgressCode/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:status/gmd:MD_ProgressCode/text()",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:status/mcc:MD_ProgressCode/@codeListValue"
            ],
            multiplicity="*",
        ),
        ISOKeyword(
            name="keywords",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:descriptiveKeywords/mri:MD_Keywords"
            ],
            multiplicity="*"
        ),
        ISO19115_3Element(
            name="keyword-inspire-theme",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString/text()",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:descriptiveKeywords/mri:MD_Keywords/mri:keyword/gco:CharacterString/text()"
            ],
            multiplicity="*",
        ),
        # Deprecated: kept for backwards compatibilty
        ISO19115_3Element(
            name="keyword-controlled-other",
            search_paths=[
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:keywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString/text()",
            ],
            multiplicity="*",
        ),
        ISOUsage(
            name="usage",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceSpecificUsage/gmd:MD_Usage",
            ],
            multiplicity="*"
        ),
        ISO19115_3Element(
            name="limitations-on-public-access",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:otherConstraints/gco:CharacterString/text()",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:resourceConstraints/mco:MD_LegalConstraints/mco:otherConstraints/gco:CharacterString/text()"
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="access-constraints",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode/@codeListValue",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode/@codeListValue",
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:accessConstraints/gmd:MD_RestrictionCode/text()",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:resourceConstraints/mco:MD_LegalConstraints/mco:accessConstraints/mco:MD_RestrictionCode/@codeListValue"
            ],
            multiplicity="*",
        ),

        ISO19115_3Element(
            name="use-constraints",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation/gco:CharacterString/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:resourceConstraints/gmd:MD_Constraints/gmd:useLimitation/gco:CharacterString/text()",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:resourceConstraints/mco:MD_LegalConstraints/mco:useConstraints/mco:MD_RestrictionCode/text()"
            ],
            multiplicity="*",
        ),
        ISOAggregationInfo(
            name="aggregation-info",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:aggregationInfo/gmd:MD_AggregateInformation",
                "gmd:identificationInfo/gmd:SV_ServiceIdentification/gmd:aggregationInfo/gmd:MD_AggregateInformation",
            ],
            multiplicity="*"
        ),
        ISO19115_3Element(
            name="spatial-data-service-type",
            search_paths=[
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:serviceType/gco:LocalName/text()",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/srv:serviceType/gco:ScopedName/text()"
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="spatial-resolution",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance/text()",
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="spatial-resolution-units",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance/@uom",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance/@uom",
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="equivalent-scale",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer/text()",
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="dataset-language",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode/@codeListValue",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:language/gmd:LanguageCode/@codeListValue",
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:language/gmd:LanguageCode/text()",
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="topic-category",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode/text()",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:topicCategory/mri:MD_TopicCategoryCode/text()"
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="extent-controlled",
            search_paths=[
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="extent-free-text",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicDescription/gmd:geographicIdentifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicDescription/gmd:geographicIdentifier/gmd:MD_Identifier/gmd:code/gco:CharacterString/text()",
            ],
            multiplicity="*",
        ),
        ISOBoundingBox(
            name="bbox",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:extent/gex:EX_Extent/gex:geographicElement/gex:EX_GeographicBoundingBox"
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="temporal-extent-begin",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition/text()",
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml32:TimePeriod/gml32:beginPosition/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:beginPosition/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml32:TimePeriod/gml32:beginPosition/text()",
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="temporal-extent-end",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition/text()",
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml32:TimePeriod/gml32:endPosition/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod/gml:endPosition/text()",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml32:TimePeriod/gml32:endPosition/text()",
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="vertical-extent",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:extent/gmd:EX_Extent/gmd:verticalElement/gmd:EX_VerticalExtent",
            ],
            multiplicity="*",
        ),
        ISOCoupledResources(
            name="coupled-resource",
            search_paths=[
                "gmd:identificationInfo/srv:SV_ServiceIdentification/srv:operatesOn",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/srv:operatesOn"
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="additional-information-source",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:supplementalInformation/gco:CharacterString/text()",
            ],
            multiplicity="0..1",
        ),
        ISODataFormat(
            name="data-format",
            search_paths=[
                "gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format",
                "mdb:distributionInfo/mrd:MD_Distribution/mrd:distributionFormat/mrd:MD_Format/mrd:formatSpecificationCitation/cit:CI_Citation"
            ],
            multiplicity="*",
        ),
        ISOResponsibleParty(
            name="distributor",
            search_paths=[
                "gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty",
                "mdb:distributionInfo/mrd:MD_Distribution/mrd:distributor/mrd:MD_Distributor/mrd:distributorContact/cit:CI_Responsibility",
            ],
            multiplicity="*",
        ),
        ISOResourceLocator(
            name="resource-locator",
            search_paths=[
                "gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource",
                "gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorTransferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource",
                "mdb:distributionInfo/mrd:MD_Distribution/mrd:transferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource"
            ],
            multiplicity="*",
        ),
        ISOResourceLocator(
            name="resource-locator-identification",
            search_paths=[
                "gmd:identificationInfo//gmd:CI_OnlineResource",
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="conformity-specification",
            search_paths=[
                "gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:specification",
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="conformity-pass",
            search_paths=[
                "gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:pass/gco:Boolean/text()",
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="conformity-explanation",
            search_paths=[
                "gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:report/gmd:DQ_DomainConsistency/gmd:result/gmd:DQ_ConformanceResult/gmd:explanation/gco:CharacterString/text()",
            ],
            multiplicity="0..1",
        ),
        ISO19115_3Element(
            name="lineage",
            search_paths=[
                "gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString/text()",
                "mdb:resourceLineage/mrl:LI_Lineage/mrl:statement/gco:CharacterString/text()"
            ],
            multiplicity="0..1",
        ),
        ISOBrowseGraphic(
            name="browse-graphic",
            search_paths=[
                "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:graphicOverview/gmd:MD_BrowseGraphic",
                "gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:graphicOverview/gmd:MD_BrowseGraphic",
                "mdb:identificationInfo/srv:SV_ServiceIdentification/mri:graphicOverview/mcc:MD_BrowseGraphic"
            ],
            multiplicity="*",
        ),
        ISO19115_3Element(
            name="owner_org",
            search_paths=[
                'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty[gmd:role/gmd:CI_RoleCode/@codeListValue="owner"]/gmd:organisationName/gco:CharacterString/text()',
                'gmd:identificationInfo/srv:SV_ServiceIdentification/gmd:pointOfContact/gmd:CI_ResponsibleParty[gmd:role/gmd:CI_RoleCode/@codeListValue="owner"]/gmd:organisationName/gco:CharacterString/text()',
                "gmd:contact/gmd:CI_ResponsibleParty",
                'mdb:identificationInfo/srv:SV_ServiceIdentification/mri:descriptiveKeywords/mri:MD_Keywords/mri:thesaurusName/cit:CI_Citation/cit:citedResponsibleParty/cit:CI_Responsibility[cit:role/cit:CI_RoleCode/@codeListValue="owner"]/cit:party/cit:CI_Organisation/cit:name/gco:CharacterString/text()'
            ],
            multiplicity="*"
        ),
        ISO19115_3Element(
            name="keyword-sensor",
            search_paths=[
                'gmd:identificationInfo/*/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()="CMRE Sensors"]/gmd:keyword/gco:CharacterString/text()',
                'mdb:identificationInfo/srv:SV_ServiceIdentification/mri:descriptiveKeywords/mri:MD_Keywords[mri:thesaurusName/cit:CI_Citation/cit:title/gco:CharacterString/text()="CMRE Sensors"]/mri:keyword/gco:CharacterString/text()'
            ],
            multiplicity="*"
        ),
        ISO19115_3Element(
            name="keyword-experiment",
            search_paths=[
                'gmd:identificationInfo/*/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()="CMRE Experiment Types"]/gmd:keyword/gco:CharacterString/text()',
                'mdb:identificationInfo/srv:SV_ServiceIdentification/mri:descriptiveKeywords/mri:MD_Keywords[mri:thesaurusName/cit:CI_Citation/cit:title/gco:CharacterString/text()="CMRE Experiment Types"]/mri:keyword/gco:CharacterString/text()'
            ],
            multiplicity="*"
        ),
        ISO19115_3Element(
            name="keyword-platform",
            search_paths=[
                'gmd:identificationInfo/*/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()="CMRE Platforms"]/gmd:keyword/gco:CharacterString/text()',
                'mdb:identificationInfo/srv:SV_ServiceIdentification/mri:descriptiveKeywords/mri:MD_Keywords[mri:thesaurusName/cit:CI_Citation/cit:title/gco:CharacterString/text()="CMRE Platforms"]/mri:keyword/gco:CharacterString/text()'
            ],
            multiplicity="*"
        ),
        ISO19115_3Element(
            name="keyword-trial",
            search_paths=[
                'gmd:identificationInfo/*/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:thesaurusName/gmd:CI_Citation/gmd:title/gco:CharacterString/text()="CMRE Trials"]/gmd:keyword/gco:CharacterString/text()',
                'mdb:identificationInfo/srv:SV_ServiceIdentification/mri:descriptiveKeywords/mri:MD_Keywords[mri:thesaurusName/cit:CI_Citation/cit:title/gco:CharacterString/text()="CMRE Trials"]/mri:keyword/gco:CharacterString/text()'
            ],
            multiplicity="*"
        ),
        ISO19115_3Element(
            name="dimension_name",
            search_paths=[
                'gmd:contentInfo/gmd:MD_CoverageDescription/gmd:dimension/gmd:MD_Band/gmd:descriptor/gco:CharacterString/text()',
                'mdb:contentInfo/mrc:MD_CoverageDescription/mrc:attributeDescription/text()'
            ],
            multiplicity="*"
        ),
        EKOEClassification(
            name="ekoe-classification",
            search_paths=[
               "gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_SecurityConstraints[gmd:classification/gmd:MD_ClassificationCode/@codeList='http://eden.ign.fr/xsd/ngmp/20110916/resources/codelist/ngmpCodelists.xml#MD_ClassificationCode']",
                'mdb:identificationInfo/srv:SV_ServiceIdentification/mri:resourceConstraints/mco:MD_SecurityConstraints[mco:classification/mco:MD_ClassificationCode/@codeList="http://eden.ign.fr/xsd/ngmp/20110916/resources/codelist/ngmpCodelists.xml#MD_ClassificationCode"]'
            ],
            multiplicity="0..1"
        )
    ]
