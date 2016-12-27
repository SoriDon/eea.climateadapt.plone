"""
Various page overrides
"""
from plone.app.contentmenu.menu import DisplaySubMenuItem as DSMI
from plone.app.content.browser.interfaces import IContentsPage
from plone.memoize.instance import memoize
from Products.CMFPlone import utils

from plone.app.widgets.dx import RichTextWidget
from eea.climateadapt.interfaces import IEEAClimateAdaptInstalled
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer
from z3c.form.util import getSpecification
from plone.app.contenttypes.behaviors.richtext import IRichText  # noqa
from z3c.form.interfaces import IFormLayer
from plone.app.widgets.interfaces import IWidgetsLayer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from eea.pdf.interfaces import IPDFTool
from zope.component import queryUtility
from Products.Five.browser import BrowserView


class DisplaySubMenuItem(DSMI):
    """ Override because we have covers with id 'index_html' and we want to
    be able to choose the display template for them
    """

    @memoize
    def disabled(self):
        if IContentsPage.providedBy(self.request):
            return True
        context = self.context
        if self.context_state.is_default_page():
            context = utils.parent(context)
        if not getattr(context, 'isPrincipiaFolderish', False):
            return False
        # By default an index_html signals disabled Display Menu, we don't want
        # that, so we return False, not disabled, by default
        elif 'index_html' in context:
            return False
        else:
            return False


class FolderPdfBody (BrowserView):
    """ Override folder pdf body
    """
    template = ViewPageTemplateFile("pt/folder.body.pt")

    def __init__(self, context, request):
        super(FolderPdfBody, self).__init__(context, request)
        self._macro = "content-core"
        self._theme = None
        self._maxdepth = None
        self._maxbreadth = None
        self._maxitems = None
        self._depth = 0
        self._count = 1

    def theme(self, context=None):
        """ PDF Theme
        """
        if context:
            tool = queryUtility(IPDFTool)
            return tool.theme(context)

        if self._theme is None:
            tool = queryUtility(IPDFTool)
            self._theme = tool.theme(self.context)

        return self._theme

    def getValue(self, name, context='', default=None):
        """ Get value
        """
        if context == '':
            context = self.context

        getField = getattr(context, 'getField', lambda name: None)
        field = getField(name)
        if not field:
            return default

        value = field.getAccessor(context)()
        return value or default

    @property
    def macro(self):
        """ ZPT macro to use while rendering PDF
        """
        return self._macro

    @property
    def maxdepth(self):
        """ Maximum depth
        """
        if self._maxdepth is None:
            self._maxdepth = self.getValue('pdfMaxDepth',
                   default=self.getValue('maxdepth', self.theme(), default=0))
        return self._maxdepth

    @property
    def maxbreadth(self):
        """ Maximum breadth
        """
        if self._maxbreadth is None:
            self._maxbreadth = self.getValue('pdfMaxBreadth',
                   default=self.getValue('maxbreadth', self.theme(), default=0))
        return self._maxbreadth

    @property
    def maxitems(self):
        """ Maximum items
        """
        if self._maxitems is None:
            self._maxitems = self.getValue('pdfMaxItems',
                 default=self.getValue('maxitems', self.theme(), default=0))
        return self._maxitems

    @property
    def depth(self):
        """ Current depth
        """
        return self._depth

    @property
    def count(self):
        """ Current counter
        """
        return self._count

    @property
    def brains(self):
        """ Brains
        """
        return self.context.getFolderContents()[:self.maxbreadth]

    def show_limit_page(self):
        """ Returns the pdf limit page
        """
        pdf = self.context.restrictedTraverse("@@pdf.limit")
        return pdf()

    @property
    def pdfs(self):
        """ Folder children
        """
        self._depth += 1

        if not self.request.get('pdf_last_brain_url'):
            brains = self.context.getFolderContents(
                contentFilter={
                    'portal_type': ['Folder', 'Collection', 'Topic']
                })
            if brains:
                self.request['pdf_last_brain_url'] = brains[-1].getURL()
                # 31424 in case there is only one result from the content
                # filter then we need to reset the depth in order to
                # get the content of the brain
                if len(brains) == 1:
                    self._depth -= 1
        if self.depth > self.maxdepth:
            if self.context.absolute_url() == \
                    self.request.get('pdf_last_brain_url'):
                yield self.show_limit_page()
            return

        ajax_load = self.request.get('ajax_load', True)
        self.request.form['ajax_load'] = ajax_load

        for brain in self.brains:
            if self.count > self.maxitems:
                if not self.request.get('pdflimit'):
                    self.request['pdflimit'] = "reached"
                    yield self.show_limit_page()
                break

            doc = brain.getObject()
            theme = self.theme(doc)
            body = getattr(theme, 'body', '')
            if not body:
                continue

            if isinstance(body, unicode):
                body = body.encode('utf-8')
            if (self.theme(self.context).id == theme.id and
                self.depth == self.maxdepth):
                if brain.getURL() == self.request.get('pdf_last_brain_url'):
                    if not self.request.get('pdflimit'):
                        self.request['pdflimit'] = "reached"
                        yield self.show_limit_page()
                continue
            try:
                pdf = doc.restrictedTraverse(body.split("?")[0])
                self._count += 1
                html = pdf(
                    macro=self.macro,
                    maxdepth=self.maxdepth,
                    maxbreadth=self.maxbreadth,
                    maxitems=self.maxitems,
                    depth=self.depth,
                    count=self.count
                )
            except Exception:
                continue
            else:
                self._count = getattr(pdf, 'count', self._count)
                yield html

        self.request.form['ajax_load'] = ajax_load

    def update(self, **kwargs):
        """ Update counters
        """
        self._macro = kwargs.get('macro', self._macro)
        self._maxdepth = kwargs.get('maxdepth', None)
        self._maxbreadth = kwargs.get('maxbreadth', None)
        self._maxitems = kwargs.get('maxitems', None)
        self._depth = kwargs.get('depth', self._depth)
        self._count = kwargs.get('count', self._count)

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        self.update(**kwargs)
        return self.template(**kwargs)


class OverrideRichText (RichTextWidget):
    """ Richtext field override for tinymce tabs plugin """

    def _base_args(self):
        # Get options
        args = super(OverrideRichText, self)._base_args()

        # Get tinymce options
        tinyoptions = args['pattern_options']['tiny']
        buttons = 'tabs tabsDelete tabsItemDelete tabsItemInsertAfter tabsItemInsertBefore accordion accordionDelete accordionItemDelete accordionItemInsertAfter accordionItemInsertBefore  '
        toolbar = tinyoptions['toolbar']
        plugins = tinyoptions['plugins']

        # Modify toolbar
        toolbar = toolbar.split('|')
        toolbar[5] = toolbar[5] + buttons
        toolbar = '|'.join(toolbar)

        # Override
        args['pattern_options']['tiny']['theme_advanced_buttons3'] = buttons
        args['pattern_options']['tiny']['toolbar'] = toolbar
        args['pattern_options']['tiny']['plugins'].append('tabs')
        args['pattern_options']['tiny']['plugins'].append('accordion')
        args['pattern_options']['tiny']['plugins'].remove('contextmenu')

        return args

    def render(self):
        return super(OverrideRichText, self).render()


@adapter(getSpecification(IRichText['text']), IWidgetsLayer)
@implementer(IFieldWidget)
def RichTextFieldWidget(field, request):
    return FieldWidget(field, OverrideRichText(request))


@adapter(getSpecification(IRichText['text']), IFormLayer)
@implementer(IFieldWidget)
def RichTextFieldWidgett(field, request):
    return FieldWidget(field, OverrideRichText(request))
