""" To be executed after migration is done and tested
"""
import logging
import plone.api
import transaction

from eea.climateadapt.translation.admin import get_all_objs

from plone.app.contenttypes.interfaces import IFolder
from plone.dexterity.interfaces import IDexterityContainer

from .config import IGNORED_CONTENT_TYPES

logger = logging.getLogger('SiteMigrate')
logger.setLevel(logging.INFO)


def is_folderish(obj):
    if IFolder in obj.__provides__.interfaces() or \
            IDexterityContainer in obj.__provides__.interfaces():
        return True
    return False


def post_migration_cleanup(site, request):
    """ Remove old index_html leaf page
    """
    logger.info("--- START CLEANUP ---")
    brains = get_all_objs(site)

    for brain in brains:
        if brain.portal_type in IGNORED_CONTENT_TYPES:
            continue

        try:
            obj = brain.getObject()
        except Exception:
            continue

        if not is_folderish(obj):
            continue

        default_page = obj.getProperty('default_page')
        if not default_page and "index_html" in obj.contentIds():
            default_page = 'index_html'

        if default_page:
            logger.info(default_page)
            default_page_obj = None
            try:
                default_page_obj = obj[default_page]
                print(default_page_obj)
            except (AttributeError, KeyError):
                logger.warning("Ignored %s" % obj.absolute_url())

            if default_page_obj:
                logger.info("Current folder %s" % obj.absolute_url())
                logger.info("Deleting %s" % default_page_obj.absolute_url())
                try:
                    plone.api.content.delete(default_page_obj)
                except Exception:
                    logger.info("Error %s" % default_page_obj.absolute_url())

    transaction.commit()
    logger.info("--- Cleanup done ---")
