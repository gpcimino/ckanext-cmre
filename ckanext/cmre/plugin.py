'''plugin.py

'''
import logging
import json
from collections import OrderedDict

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

log = logging.getLogger(__name__)


class CMREFacetsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IPackageController)
    plugins.implements(plugins.IFacets)

    # IPackageController
    def before_search(self, search_params):
        return search_params

    def after_search(self, search_results, search_params):
        return search_results

    def before_index(self, dataset_dict):
        log.debug("BEFORE_INDEX")

        # expand multi valued fields

        for f in ['trial', 'platform', 'sensor', 'experiment']:
            key = 'ekoe_' + f
            v = dataset_dict.get(key)
            log.debug("INDEXING {} -> ({}) {}".format(key, type(v), v))

            if v and isinstance(v, unicode):
                dataset_dict[key] = json.loads(v)
                log.debug("DUMPING {}".format(v))

        for key in ['ekoe_dimension']:
            v = dataset_dict.get(key)
            log.debug("INDEXING {} -> ({}) {}".format(key, type(v), v))

            if v and isinstance(v, unicode):
                dataset_dict[key] = json.loads(v)
                log.debug("DUMPING {}".format(v))

        return dataset_dict

    def before_view(self, pkg_dict):
        return pkg_dict

    def read(self, entity):
        return entity

    def create(self, entity):
        return entity

    def edit(self, entity):
        return entity

    def delete(self, entity):
        return entity

    def after_create(self, context, pkg_dict):
        return pkg_dict

    def after_update(self, context, pkg_dict):
        return pkg_dict

    def after_delete(self, context, pkg_dict):
        return pkg_dict

    def after_show(self, context, pkg_dict):
        return pkg_dict

    # IFacets
    def dataset_facets(self, orig_facets_dict, package_type):
        facets_dict = OrderedDict()
        facets_dict['ekoe_owner_org'] = plugins.toolkit._("Owner")

        for f in ['trial', 'platform', 'sensor', 'experiment']:
            facets_dict['ekoe_' + f] = plugins.toolkit._(f.capitalize())

        facets_dict['ekoe_classification'] = plugins.toolkit._("Classification")
        facets_dict['ekoe_dimension'] = plugins.toolkit._("Dimension")

        # Add back original facets to the bottom
        for key, value in orig_facets_dict.items():
            facets_dict[key] = value

        return facets_dict

