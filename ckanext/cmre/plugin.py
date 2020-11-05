'''plugin.py

'''
import logging
import json
from collections import OrderedDict

from dateutil.parser import parse

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.cmre.ekoe_const import *

log = logging.getLogger(__name__)


class CMREFacetsPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IPackageController)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

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
        # log.debug("BEFORE_INDEX")

        # expand multi valued fields
        # log.debug("INDEX FULL DICT {}".format(json.dumps(dataset_dict)))
        # log.debug("INDEX ----------------------------------------")
        dict_update = {}
        for k,v in dataset_dict.items():
            if k.startswith('ekoe'):
                # log.debug("INDEX {} <{}>: {}".format(k, type(v), v))
                if k in COMPLEX_EKOE_FIELDS:
                    dict_update[k] = json.loads(v)

        dataset_dict.update(dict_update)

        for isokey,ekoekey in [('temporal-extent-begin', 'ekoe_temporal_start'),
                               ('temporal-extent-end', 'ekoe_temporal_end')]:
            datetime = dataset_dict.get(isokey, None)
            if datetime:
                # log.debug("TEMPORAL:  {field}:{value}".format(field=isokey, value=datetime))
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

        for f, value in [
            (EKOE_OWNER_ORG, 'Owner org'),
            (EKOE_TRIAL, 'Sea trials'),
            (EKOE_PLATFORM, 'Platforms'),
            (EKOE_INSTRUMENT, 'Instruments'),
            (EKOE_EXPERIMENT, 'Experiment type'),
            (EKOE_DATA_CLASSIFICATION, 'Data classification'),
            (EKOE_VARIABLE, 'Variable'),
            (EKOE_GEO_IDENTIFIER, 'Geographic identifier'),
        ]:
            facets_dict[f] = plugins.toolkit._(value.capitalize())

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

    def get_helpers(self):
        return {'cmre_sorted_extras': cmre_sorted_extras}


def cmre_sorted_extras(package_extras, include):
    ''' Based on original sorted_extras() -- Used for outputting package extras

    :param package_extras: the package extras
    :type package_extras: dict
    :include exclude: keys to include
    :type exclude: list of strings
    '''

    extra_dict = {x['key']:x['value'] for x in package_extras if x.get('state') != 'deleted'}

    output = []
    for label, name in include:
        v = extra_dict[name]
        try:
            v = json.loads(v)
            # log.info('decoded [{}]'.format(name))
        except Exception:
            # not a string for sure, other unexpected types?
            # if isinstance(v, (list, tuple)):
            #     log.warn('Should be decoded [{}]<{}>->{}'.format(name, type(v), v))
            pass

        output.append((label, name, v))
    return output