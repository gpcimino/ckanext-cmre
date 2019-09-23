'''plugin.py

'''
import logging
from datetime import date
import json

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
        log.info("BEFORE_INDEX")

        for f in ['platform', 'instrument', 'cruise']:
            key = 'ekoe_' + f
            v = dataset_dict.get(key)
            log.info("INDEXING {} -> ({}) {}".format(key, type(v), v))

            if v and isinstance(v, unicode):
                dataset_dict[key] = json.loads(v)
                log.info("DUMPING {}".format(v))

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
    def dataset_facets(self, facets_dict, package_type):
        for f in ['platform', 'instrument', 'cruise']:
            facets_dict['ekoe_' + f] = plugins.toolkit._("EKOE " + f)
        return facets_dict

