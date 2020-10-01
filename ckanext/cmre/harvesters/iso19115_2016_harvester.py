import logging
import uuid

import dateutil

from ckan import logic, model
from ckan import plugins as p
from ckan.lib.navl.validators import not_empty
from ckan.lib.search.index import PackageSearchIndex
from ckanext.cmre.harvesters.iso19115_2016_parser import ISO19115_3Document
from ckanext.cmre.harvesters.iso19115_2016_validator import \
    ISO19115_3Validators
from ckanext.harvest.model import HarvestObject
from ckanext.spatial.interfaces import ISpatialHarvester
from ckanext.spatial.validation.validation import (Validators, XsdValidator,
                                                   all_validators)
from pylons import config
from ckanext.cmre.harvesters.cmre import CMREHarvester

log = logging.getLogger(__name__)


class ISO19115_3Harvester(CMREHarvester):
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
        context = {
            'model': model,
            'session': model.Session,
            'user': self._get_user_name(),
        }

        log = logging.getLogger(__name__ + '.import')
        log.debug('Import stage for harvest object: %s', harvest_object.id)

        if not harvest_object:
            log.error('No harvest object received')
            return False

        self._set_source_config(harvest_object.source.config)

        if self.force_import:
            status = 'change'
        else:
            status = self._get_object_extra(harvest_object, 'status')

        # Get the last harvested object (if any)
        previous_object = model.Session.query(HarvestObject) \
            .filter(HarvestObject.guid == harvest_object.guid) \
            .filter(HarvestObject.current == True) \
            .first()

        if status == 'delete':
            # Delete package
            context.update({
                'ignore_auth': True,
            })
            p.toolkit.get_action('package_delete')(
                context, {'id': harvest_object.package_id})
            log.info('Deleted package {0} with guid {1}'.format(
                harvest_object.package_id, harvest_object.guid))

            return True

        # Check if it is a non ISO document
        original_document = self._get_object_extra(
            harvest_object, 'original_document')
        original_format = self._get_object_extra(
            harvest_object, 'original_format')

        if original_document and original_format:
            # DEPRECATED use the ISpatialHarvester interface method
            self.__base_transform_to_iso_called = False
            content = self.transform_to_iso(
                original_document, original_format, harvest_object)
            if not self.__base_transform_to_iso_called:
                log.warn('Deprecation warning: calling transform_to_iso directly is deprecated. ' +
                         'Please use the ISpatialHarvester interface method instead.')

            for harvester in p.PluginImplementations(ISpatialHarvester):
                content = harvester.transform_to_iso(
                    original_document, original_format, harvest_object)

            if content:
                harvest_object.content = content
            else:
                self._save_object_error(
                    'Transformation to ISO failed', harvest_object, 'Import')
                return False
        else:
            if harvest_object.content is None:
                self._save_object_error('Empty content for object {0}'.format(
                    harvest_object.id), harvest_object, 'Import')
                return False

            # Validate ISO document
            is_valid, profile, errors = self._validate_document(
                harvest_object.content, harvest_object)
            if not is_valid:
                # If validation errors were found, import will stop unless
                # configuration per source or per instance says otherwise
                continue_import = p.toolkit.asbool(config.get('ckanext.spatial.harvest.continue_on_validation_errors', False)) or \
                    self.source_config.get('continue_on_validation_errors')
                if not continue_import:
                    return False

        # Parse ISO document
        try:
            iso_parser = ISO19115_3Document(harvest_object.content)
            iso_values = iso_parser.read_values()
        except Exception, e:
            self._save_object_error('Error parsing ISO document for object {0}: {1}'.format(harvest_object.id, str(e)),
                                    harvest_object, 'Import')
            return False

        # Flag previous object as not current anymore
        if previous_object and not self.force_import:
            previous_object.current = False
            previous_object.add()

        # Update GUID with the one on the document
        iso_guid = iso_values['guid']
        if iso_guid and harvest_object.guid != iso_guid:
            # First make sure there already aren't current objects
            # with the same guid
            existing_object = model.Session.query(HarvestObject.id) \
                .filter(HarvestObject.guid == iso_guid) \
                .filter(HarvestObject.current == True) \
                .first()
            if existing_object:
                self._save_object_error('Object {0} already has this guid {1}'.format(existing_object.id, iso_guid),
                                        harvest_object, 'Import')
                return False

            harvest_object.guid = iso_guid
            harvest_object.add()

        # Generate GUID if not present (i.e. it's a manual import)
        if not harvest_object.guid:
            m = hashlib.md5()
            m.update(harvest_object.content.encode('utf8', 'ignore'))
            harvest_object.guid = m.hexdigest()
            harvest_object.add()

        # Get document modified date
        try:
            metadata_modified_date = dateutil.parser.parse(
                iso_values['metadata-date'], ignoretz=True)
        except ValueError:
            self._save_object_error('Could not extract reference date for object {0} ({1})'
                                    .format(harvest_object.id, iso_values['metadata-date']), harvest_object, 'Import')
            return False

        harvest_object.metadata_modified_date = metadata_modified_date
        harvest_object.add()

        # Build the package dict
        package_dict = self.get_package_dict(iso_values, harvest_object)
        for harvester in p.PluginImplementations(ISpatialHarvester):
            package_dict = harvester.get_package_dict(context, {
                'package_dict': package_dict,
                'iso_values': iso_values,
                'xml_tree': iso_parser.xml_tree,
                'harvest_object': harvest_object,
            })
        if not package_dict:
            log.error('No package dict returned, aborting import for object {0}'.format(
                harvest_object.id))
            return False

        # Create / update the package
        context.update({
            'extras_as_string': True,
            'api_version': '2',
            'return_id_only': True})

        if self._site_user and context['user'] == self._site_user['name']:
            context['ignore_auth'] = True

        # The default package schema does not like Upper case tags
        tag_schema = logic.schema.default_tags_schema()
        tag_schema['name'] = [not_empty, unicode]

        # Flag this object as the current one
        harvest_object.current = True
        harvest_object.add()

        if status == 'new':
            package_schema = logic.schema.default_create_package_schema()
            package_schema['tags'] = tag_schema
            context['schema'] = package_schema

            # We need to explicitly provide a package ID, otherwise ckanext-spatial
            # won't be be able to link the extent to the package.
            package_dict['id'] = unicode(uuid.uuid4())
            package_schema['id'] = [unicode]

            # Save reference to the package on the object
            harvest_object.package_id = package_dict['id']
            harvest_object.add()
            # Defer constraints and flush so the dataset can be indexed with
            # the harvest object id (on the after_show hook from the harvester
            # plugin)
            model.Session.execute(
                'SET CONSTRAINTS harvest_object_package_id_fkey DEFERRED')
            model.Session.flush()

            try:
                package_id = p.toolkit.get_action(
                    'package_create')(context, package_dict)
                log.info('Created new package %s with guid %s',
                         package_id, harvest_object.guid)
            except p.toolkit.ValidationError, e:
                self._save_object_error('Validation Error: %s' % str(
                    e.error_summary), harvest_object, 'Import')
                return False

        elif status == 'change':

            # Check if the modified date is more recent
            if not self.force_import and previous_object and harvest_object.metadata_modified_date <= previous_object.metadata_modified_date:

                # Assign the previous job id to the new object to
                # avoid losing history
                harvest_object.harvest_job_id = previous_object.job.id
                harvest_object.add()

                # Delete the previous object to avoid cluttering the object table
                previous_object.delete()

                # Reindex the corresponding package to update the reference to the
                # harvest object
                if ((config.get('ckanext.spatial.harvest.reindex_unchanged', True) != 'False'
                     or self.source_config.get('reindex_unchanged') != 'False')
                        and harvest_object.package_id):
                    context.update({'validate': False, 'ignore_auth': True})
                    try:
                        package_dict = logic.get_action('package_show')(context,
                                                                        {'id': harvest_object.package_id})
                    except p.toolkit.ObjectNotFound:
                        pass
                    else:
                        for extra in package_dict.get('extras', []):
                            if extra['key'] == 'harvest_object_id':
                                extra['value'] = harvest_object.id
                        if package_dict:
                            package_index = PackageSearchIndex()
                            package_index.index_package(package_dict)

                log.info('Document with GUID %s unchanged, skipping...' %
                         (harvest_object.guid))
            else:
                package_schema = logic.schema.default_update_package_schema()
                package_schema['tags'] = tag_schema
                context['schema'] = package_schema

                package_dict['id'] = harvest_object.package_id
                try:
                    package_id = p.toolkit.get_action(
                        'package_update')(context, package_dict)
                    log.info('Updated package %s with guid %s',
                             package_id, harvest_object.guid)
                except p.toolkit.ValidationError, e:
                    self._save_object_error('Validation Error: %s' % str(
                        e.error_summary), harvest_object, 'Import')
                    return False

        model.Session.commit()

        return True

    def _get_validator(self):
        '''
        Returns the validator object using the relevant profiles

        The profiles to be used are assigned in the following order:

        1. 'validator_profiles' property of the harvest source config object
        2. 'ckan.spatial.validator.profiles' configuration option in the ini file
        3. Default value as defined in DEFAULT_VALIDATOR_PROFILES
        '''
        if not hasattr(self, '_validator'):
            if hasattr(self, 'source_config') and self.source_config.get('validator_profiles', None):
                profiles = self.source_config.get('validator_profiles')
            elif config.get('ckan.spatial.validator.profiles', None):
                profiles = [
                    profile.strip() for profile in
                    config.get('ckan.spatial.validator.profiles').split(',')
                ]
            else:
                profiles = ["iso19115-3"]

            self._validator = ISO19115_3Validators(profiles=profiles)

            # Add any custom validators from extensions
            for plugin_with_validators in p.PluginImplementations(ISpatialHarvester):
                custom_validators = plugin_with_validators.get_validators()
                for custom_validator in custom_validators:
                    if custom_validator not in all_validators:
                        self._validator.add_validator(custom_validator)

        return self._validator
