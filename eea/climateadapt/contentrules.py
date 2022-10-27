# -*- coding: utf-8 -*-
""" Content rules
"""
import logging
from plone import api
from plone.api.portal import get_tool
import transaction
from OFS.SimpleItem import SimpleItem
# from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import NullAddForm
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from ZODB.POSException import ConflictError
from zope.component import adapter
from zope.interface import Interface, implementer
from DateTime import DateTime

from eea.climateadapt import CcaAdminMessageFactory as _
from eea.climateadapt.translation.admin import translate_obj
from eea.climateadapt.translation.admin import create_translation_object
from eea.climateadapt.translation.admin import copy_missing_interfaces
from eea.climateadapt.translation.admin import translation_step_4
from eea.climateadapt.translation.utils import get_site_languages
from plone.app.multilingual.manager import TranslationManager
from zope.site.hooks import getSite

logger = logging.getLogger('eea.climateadapt')


class IObjectDateExpirationAction(Interface):
    """Interface for the configurable aspects of a archived action. """


@implementer(IObjectDateExpirationAction, IRuleElementData)
class ObjectDateExpirationAction(SimpleItem):
    """The actual persistent implementation of the action element. """

    element = "eea.climateadapt.ObjectDateExpiration"
    summary = _(u"Set object expiration date")


@adapter(Interface, IObjectDateExpirationAction, Interface)
@implementer(IExecutable)
class ObjectDateExpirationActionExecutor(object):
    """The executor for this action."""

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        transaction.savepoint()

        try:
            state = api.content.get_state(obj)
            if state == 'published':
                obj.setExpirationDate(None)
                obj._p_changed = True
                obj.reindexObject()
            if state == 'archived':
                obj.setExpirationDate(DateTime())
                obj._p_changed = True
                obj.reindexObject()

        except Exception as e:
            # self.error(obj, str(e))
            return False

        return True


class ObjectDateExpirationAddForm(NullAddForm):
    """A reindex action form"""

    def create(self):
        return ObjectDateExpirationAction()


class IReindexAction(Interface):
    """Interface for the configurable aspects of a reindex action. """


@implementer(IReindexAction, IRuleElementData)
class ReindexAction(SimpleItem):
    """The actual persistent implementation of the action element. """

    element = "eea.climateadapt.Reindex"
    summary = _(u"Reindex object")


@adapter(Interface, IReindexAction, Interface)
@implementer(IExecutable)
class ReindexActionExecutor(object):
    """The executor for this action."""

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object

        transaction.savepoint()

        catalog = get_tool("portal_catalog")

        try:
            catalog.unindexObject(obj)
            catalog.indexObject(obj)
        except ConflictError as err:
            raise err
        except Exception as err:
            self.error(obj, str(err))
            return False

        return True

    def error(self, obj, error):
        """ Show error """
        request = getattr(self.context, "REQUEST", None)
        if request is not None:
            title = utils.pretty_title_or_id(obj, obj)
            message = _(
                u"Unable to reindex ${name} as part of content rule 'reindex' action: ${error}",
                mapping={"name": title, "error": error},
            )
            IStatusMessage(request).addStatusMessage(message, type="error")


class ReindexAddForm(NullAddForm):
    """A reindex action form"""

    def create(self):
        return ReindexAction()


class ITranslateAction(Interface):
    """Interface for the configurable aspects of a translate action. """


@implementer(ITranslateAction, IRuleElementData)
class TranslateAction(SimpleItem):
    """The actual persistent implementation of the action element. """

    element = "eea.climateadapt.Translate"
    summary = _(u"Translate object")


@adapter(Interface, ITranslateAction, Interface)
@implementer(IExecutable)
class TranslateActionExecutor(object):
    """The executor for this action."""

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        if "/en/" in obj.absolute_url():
            self.create_translations(obj)
            self.copy_fields(obj)
            self.translate_obj(obj)
            self.copy_interfaces(obj)  # TODO: delete. It's already included in
            # create_translation_object. It is used here only for testing
            # on old created content. Example: fixing interfaces for pages
            # like share-your-info

    def error(self, obj, error):
        """ Show error """
        request = getattr(self.context, "REQUEST", None)
        if request is not None:
            title = utils.pretty_title_or_id(obj, obj)
            message = _(
                u"Unable to translate ${name} as part of content rule "
                "'translate' action: ${error}",
                mapping={"name": title, "error": error},
            )
            IStatusMessage(request).addStatusMessage(message, type="error")

    def create_translations(self, obj):
        """ Make sure all translations (cloned) objs exists for this obj
        """
        transaction.savepoint()
        translations = TranslationManager(obj).get_translations()
        for language in get_site_languages():
            if language != "en" and language not in translations:
                create_translation_object(obj, language)
        transaction.commit()

    def translate_obj(self, obj):
        """ Send the obj to be translated
        """
        try:
            result = translate_obj(obj, one_step=True)
        except Exception as e:
            self.error(obj, str(e))

    def copy_interfaces(self, obj):
        """ Copy interfaces from en to translated obj
        """
        translations = TranslationManager(obj).get_translations()
        for language in translations:
            trans_obj = translations[language]
            copy_missing_interfaces(obj, trans_obj)

    def set_workflow_states(self, obj):
        """ Mark translations as not approved
        """
        translations = TranslationManager(obj).get_translations()
        for language in translations:
            this_obj = translations[language]
            wftool = getToolByName(this_obj, "portal_workflow")
            wftool.doActionFor(this_obj, 'send_to_translation_not_approved')

    def copy_fields(self, obj):
        """ Run step 4 for this obj
        """
        translations = TranslationManager(obj).get_translations()
        for language in translations:
            if language != "en":
                settings = {
                    "language": language,
                    "uid": obj.UID(),
                }
                translation_step_4(getSite(), settings)


class TranslateAddForm(NullAddForm):
    """A translate action form"""

    def create(self):
        return TranslateAction()
