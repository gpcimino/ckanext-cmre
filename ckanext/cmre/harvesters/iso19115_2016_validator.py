from ckanext.spatial.validation.validation import Validators, all_validators, XsdValidator
import os


class ISO19115_3Schema(XsdValidator):
    name = 'iso19115-3'
    title = 'ISO19115-3 XSD Schema'

    @classmethod
    def is_valid(cls, xml):
        xsd_path = 'xml/iso19115-3'
        gmx_xsd_filepath = os.path.join(os.path.dirname(__file__),
                                        xsd_path, 'xmlns/isotc211/19115/-3/mda/1.0/metadataApplication.xsd')

        xsd_name = 'ISO19115-3 Dataset schema (gmx.xsd)'
        is_valid, errors = cls._is_valid(xml, gmx_xsd_filepath, xsd_name)
        if not is_valid:
            # TODO: not sure if we need this one,
            # keeping for backwards compatibility
            errors.insert(0, ('{0} Validation Error'.format(xsd_name), None))
        return is_valid, errors


all_validators += (ISO19115_3Schema,)


class ISO19115_3Validators(Validators):
    def __init__(self, profiles=["iso19115-3", "constraints", "gemini2"]):
        super(ISO19115_3Validators, self).__init__(profiles=profiles)
        self.profiles = profiles

        self.validators = {}  # name: class
        for validator_class in all_validators:
            self.validators[validator_class.name] = validator_class