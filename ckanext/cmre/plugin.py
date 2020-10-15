'''plugin.py

'''
import logging
import json
from collections import OrderedDict
from dateutil.parser import parse

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

log = logging.getLogger(__name__)


class CMREFacetsPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IPackageController)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IConfigurer)

    # IPackageController
    def before_search(self, search_params):
        return self._temporal_search(search_params)

    def _temporal_search(self, search_params):
        extras = search_params.get('extras')
        if not extras:
            # There are no extras in the search params, so do nothing.
            return search_params

        # Add a date-range query with the selected start and end dates into the
        # Solr facet queries.
        fq = search_params['fq']

        start_date = extras.get('ext_startdate')
        end_date = extras.get('ext_enddate')

        if start_date:
            fq = '{fq} +ekoe_temporal_end:[{start_date} TO *]'.format(
                fq=fq, start_date=start_date)

        if end_date:
            fq = '{fq} +ekoe_temporal_start:[* TO {end_date}]'.format(
                fq=fq, end_date=end_date)

        search_params['fq'] = fq
        return search_params

    def after_search(self, search_results, search_params):
        return search_results

    def before_index(self, dataset_dict):
        log.debug("BEFORE_INDEX")

        # expand multi valued fields

        for f in ['trial', 'platform', 'sensor', 'experiment']:
            key = 'ekoe_' + f
            v = dataset_dict.get(key, None)
            log.debug("INDEXING {} -> ({}) {}".format(key, type(v), v))

            if v and isinstance(v, unicode):
                dataset_dict[key] = json.loads(v)
                log.debug("DUMPING {}".format(v))

        for key in ['ekoe_dimension']:
            v = dataset_dict.get(key, None)
            log.debug("INDEXING {} -> ({}) {}".format(key, type(v), v))

            if v and isinstance(v, unicode):
                dataset_dict[key] = json.loads(v)
                log.debug("DUMPING {}".format(v))

        for isokey,ekoekey in [('temporal-extent-begin', 'ekoe_temporal_start'),
                               ('temporal-extent-end', 'ekoe_temporal_end')]:
            datetime = dataset_dict.get(isokey, None)
            if datetime:
                log.debug("TEMPORAL:  {field}:{value}".format(field=isokey, value=datetime))
                try:
                    date = parse(datetime)
                    dataset_dict[ekoekey] = date
                except ValueError as e:
                    log.warn("Error while parsing {field}:{value}".format(field=isokey, value=datetime))

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
        facets_dict['ekoe_owner_org'] = plugins.toolkit._("Owner org")

        for f, value in {'trial': 'Sea trials', 'platform': 'Platform id',
                         'sensor': 'Instrument id', 'experiment': 'Experiment type'}.iteritems():
            facets_dict['ekoe_' + f] = plugins.toolkit._(value.capitalize())

        facets_dict['ekoe_classification'] = plugins.toolkit._("Data classification")
        facets_dict['ekoe_dimension'] = plugins.toolkit._("Variable")
        facets_dict['ekoe_identifier'] = plugins.toolkit._("Geographic identifier")

        remove = ['organization', 'groups']

        # Add back original facets to the bottom
        for key, value in orig_facets_dict.items():
            if key not in remove:
                # log.info("Add facet key:{key}".format(key=key))
                facets_dict[key] = value

        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict


    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_resource('fanstatic', 'ckanext-datesearch')
        toolkit.add_public_directory(config, 'public')
