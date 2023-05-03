""" Migrate content to Volto
"""
from Products.Five.browser import BrowserView
from plone.api import portal
from eea.climateadapt.scripts import get_plone_site
from eea.climateadapt.translation.admin import get_all_objs
from zope.component import getMultiAdapter
from eea.climateadapt.migration.interfaces import IMigrateToVolto
import logging

logger = logging.getLogger('eea.climateadapt')


def _migrate_to_volto(site, request):
    """ #161595 migration script for Plone 4 to Volto content
    """
    logger.info("--- START MIGRATION -----------------------------")
    logger.info("Get the list of items ordered by levels...")
    brains = get_all_objs(site)

    for brain in brains:
        obj = brain.getObject()
        logger.info("Migrating %s" % obj.absolute_url())

        try:
            migrate = getMultiAdapter((obj, request), IMigrateToVolto)
            migrate()
        except Exception:
            logger.info("Error for %s" % obj.absolute_url())

    logger.info("--- Done ----------------------------------------")
    return "Done"


def migrate_to_volto(site=None, request=None):
    """ bin/standalone run bin/migrate_to_volto
    """
    if site is None:
        site = get_plone_site()
    if request is None:
        logger.info("TODO implement fake request")
    else:
        _migrate_to_volto(site, request)


class MigrateToVolto(BrowserView):
    """ A view to manually run the script for migrating to Volto content
    """

    def __call__(self):

        site = portal.get()

        return migrate_to_volto(site, self.request)
