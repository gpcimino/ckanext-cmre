import logging
import ckan.lib.base as base

class CMREController(base.BaseController):
	
    def aboutcmre(self):
        return base.render('home/aboutcmre.html')

    def aboutilab(self):
        return base.render('home/aboutilab.html')

    def contactus(self):
        return base.render('home/contactus.html')		
