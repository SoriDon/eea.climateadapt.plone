from plone import api
from plone.app.theming.interfaces import IThemeSettings
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.component import getUtility


class ExternalTemplateHeader(BrowserView):

    def theme_base_url(self):
        reg = getUtility(IRegistry)
        settings = reg.forInterface(IThemeSettings, False)
        portal = api.portal.get()
        base_url = portal.absolute_url()

        return base_url + '/++theme++' + settings.currentTheme + '/'
