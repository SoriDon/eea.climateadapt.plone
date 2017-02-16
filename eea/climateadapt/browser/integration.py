""" Integration and overrides with various components
"""


from Acquisition import Explicit
from Acquisition import aq_inner
from OFS.Image import Image
from OFS.Traversable import Traversable
from UserDict import UserDict
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.edit import CustomEditForm as CoverEditForm
from collective.cover.tiles.edit import CustomTileEdit as CoverTileEdit
from plone.api import portal
from plone.app.layout.globals.layout import LayoutPolicy
from plone.app.widgets.browser import vocabulary as vocab
from plone.dexterity.browser.add import DefaultAddView
from plone.namedfile.scaling import ImageScaling
from plone.tiles.interfaces import ITileDataManager
from types import FunctionType
from zope.component import queryUtility
from zope.interface import implementer
from zope.interface.common.mapping import IMapping
from zope.schema.interfaces import IVocabularyFactory
import inspect


class VocabularyView(vocab.VocabularyView):
    """ Override the default getVocabulary because it doesn't work
        well with the add view and the editing of an item
    """

    _vocabs = [
        ('eea.climateadapt.keywords', 'keywords'),
        ('eea.climateadapt.special_tags', 'special_tags'),
        ('eea.climateadapt.adaptation_options', 'adaptationoptions'),
        ('eea.climateadapt.cca_items', 'ccaitems')
    ]

    def get_vocabulary(self):
        context = self.get_context()
        factory_name = self.request.get('name', None)
        field_name = self.request.get('field', None)

        if (factory_name, field_name) not in self._vocabs:
            return super(VocabularyView, self).get_vocabulary()

        factory = queryUtility(IVocabularyFactory, factory_name)
        if not factory:
            raise vocab.VocabLookupException(
                'No factory with name "%s" exists.' % factory_name)

        #import pdb; pdb.set_trace()
        # This part is for backwards-compatibility with the first
        # generation of vocabularies created for plone.app.widgets,
        # which take the (unparsed) query as a parameter of the vocab
        # factory rather than as a separate search method.
        if type(factory) is FunctionType:
            factory_spec = inspect.getargspec(factory)
        else:
            factory_spec = inspect.getargspec(factory.__call__)
        query = vocab._parseJSON(self.request.get('query', ''))
        if query and 'query' in factory_spec.args:
            vocabulary = factory(context, query=query)
        else:
            # This is what is reached for non-legacy vocabularies.
            vocabulary = factory(context)

        return vocabulary


class AddView(DefaultAddView):
    """ Add form page for case studies

    The default add view, as generated by plone.autoform, cannot really use
    a custom FormExtender because the context is not the proper context (the one
    for which we want a custom form), but the container where the content is
    added. So we override this view and properly set the forms, so they can be
    overrided.
    """

    def __init__(self, context, request, ti):
        self.context = context
        self.request = request

        if self.form is not None:

            if ti.klass == 'eea.climateadapt.acemeasure.CaseStudy':
                from eea.climateadapt.browser.casestudy import CaseStudyAddForm
                self.form = CaseStudyAddForm
            elif ti.klass == 'eea.climateadapt.acemeasure.AdaptationOption':
                from eea.climateadapt.browser.adaptationoption import \
                    AdaptationOptionAddForm
                self.form = AdaptationOptionAddForm

            self.form_instance = self.form(aq_inner(self.context), self.request)
            self.form_instance.__name__ = self.__name__

        self.ti = ti

        # Set portal_type name on newly created form instance
        if self.form_instance is not None \
           and not getattr(self.form_instance, 'portal_type', None):
            self.form_instance.portal_type = ti.getId()


# collective.cover fixes
# The problem starts with the TinyMCE widget, which needs to come from
# plone.app.widgets, to properly be integrated with the site (content tree
# browser, etc). But plone.app.widgets, in its RichText editor, does a
# getToolByName(), and the context to the widget is not acquisition aware. For
# this we want an acquisition aware context (which, originally, is just a simple
# dict).


@implementer(IMapping)
class AcquisitionAwareDict(Explicit, Traversable, UserDict):
    def __init__(self, *args, **kwargs):
        super(AcquisitionAwareDict, self).__init__()
        UserDict.__init__(self, *args, **kwargs)

    def absolute_url(self):
        return self.aq_parent.absolute_url()

    @property
    def portal_type(self):
        return self.aq_parent.portal_type


class PloneLayout(LayoutPolicy):
    def __init__(self, context, request):
        #print "custom plone layout view", context
        if hasattr(context, 'aq_parent'):
            return LayoutPolicy.__init__(self, context.aq_parent, request)
        else:
            return super(PloneLayout, self).__init__(context, request)


@implementer(ITileEditForm)
class CustomEditForm(CoverEditForm):

    def getContent(self):
        dataManager = ITileDataManager(self.getTile())
        val = dataManager.get()
        context = AcquisitionAwareDict(val)
        context.REQUEST = self.request
        return context.__of__(self.context)


class CustomTileEdit(CoverTileEdit):
    form = CustomEditForm


class IconWrapper(Traversable):
    """ Class hack to allow traversing to type icons. See below"""

    def __init__(self, context):
        self.context = context

    def __bobo_traverse__(self, request, name):
        if name == "icon":
            return self.context


class AceContentImagesTraverser(ImageScaling):
    """ A hack to use the content type icons for @@images view

    It is needed because relatedItems widget from plone.app.widgets hardcodes
    the path that is used to get the icons.
    """

    def publishTraverse(self, request, name):
        if name == 'image':
            site = portal.getSite()
            icon = self.context.getIcon()
            if icon.startswith('/'):
                icon = icon[1:]
            img = site.restrictedTraverse(icon)
            if "++resource++" in icon:
                img = Image('img', 'image', img.GET())
                img = img.__of__(self.context)
            return IconWrapper(img)
        return super(AceContentImagesTraverser, self).publishTraverse(request,
                                                                      name)
