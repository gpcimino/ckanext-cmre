import os

from ckanext.spatial.validation.validation import (Validators, XsdValidator,
                                                   all_validators)


NGMP_NAME = "NGMP"


class NgmpSchema(XsdValidator):
    name = NGMP_NAME
    title = 'NGMP 1.0 XSD Schema'

    @classmethod
    def is_valid(cls, xml):
        return True, NGMP_NAME, []

all_validators += (NgmpSchema,)
