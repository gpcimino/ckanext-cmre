'''plugin.py

'''
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

class CMREThemePlugin(plugins.SingletonPlugin):
    
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config, 'templates')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config, 'public')

    
    def before_map(self, map):
	map.connect('aboutcmre', '/aboutcmre', controller='ckanext.cmre.controllers.cmre:CMREController', action='aboutcmre')
        map.connect('aboutilab', '/aboutilab', controller='ckanext.cmre.controllers.cmre:CMREController', action='aboutilab')
        map.connect('contactus', '/contactus', controller='ckanext.cmre.controllers.cmre:CMREController', action='contactus')
        return map

    def after_map(self, route_map):
        return route_map
