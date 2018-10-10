from plone import api
from plone.api.portal import getSite
from plone.app.textfield import RichText
from plone.directives import form, dexterity
from plone.memoize import view
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from Products.Five.browser import BrowserView
from eea.climateadapt.interfaces import IEEAClimateAdaptInstalled
from zope.interface import implements
from zope.lifecycleevent import modified
from zope.schema import TextLine


class RichImageSchema(form.Schema, IImageScaleTraversable):
    form.fieldset('default',
                  label=u'Item Description',
                  fields=['title', 'long_description',
                          'rich_image', 'read_more_link']
                  )

    title = TextLine(title=(u"Title"),
                     description=u"Item Name (250 character limit)",
                     required=True)

    long_description = RichText(title=(u"Description"),
                                description=u"Provide a description of the "
                                u"item.(5,000 character limit)",
                                required=True)

    rich_image = NamedBlobImage(
        title=(u"Image"),
        required=True,
    )

    read_more_link = TextLine(title=u"Read more link",
                              required=False)


class IRichImage(RichImageSchema):
    """ Interface for the RichImage content type """


class RichImage(dexterity.Container):
    """ Image content type for which we the richtext behavior is activated """
    implements(IRichImage, IEEAClimateAdaptInstalled)

    def html2text(self, html):
        if not isinstance(html, basestring):
            return u""
        portal_transforms = api.portal.get_tool(name='portal_transforms')
        data = portal_transforms.convertTo('text/plain',
                                           html, mimetype='text/html')
        text = data.getData()
        return text.strip()

    def PUT(self, REQUEST=None, RESPONSE=None):
        """DAV method to replace image field with a new resource."""
        request = REQUEST if REQUEST is not None else self.REQUEST
        response = RESPONSE if RESPONSE is not None else request.response

        self.dav__init(request, response)
        self.dav__simpleifhandler(request, response, refresh=1)

        infile = request.get('BODYFILE', None)
        filename = request['PATH_INFO'].split('/')[-1]
        self.image = NamedBlobImage(
            data=infile.read(), filename=unicode(filename))

        modified(self)
        return response

    def get_size(self):
        return getattr(self.rich_image, 'size', None)

    def content_type(self):
        return getattr(self.image, 'contentType', None)


class FrontpageSlidesView (BrowserView):
    """ BrowserView for the frontpage slides which will be loaded through diazo
    """

    def __call__(self):
        site = api.portal.get()
        sf = site.unrestrictedTraverse('/cca/frontpage-slides')
        slides = [o for o in sf.contentValues()
                  if api.content.get_state(o) == 'published']
        images = []
        for slide in slides:
            handler = getattr(self, 'handle_' + slide.title.encode(), None)
            slide_data = {}
            if handler:
                slide_data = handler()
            else:
                slide_data = {
                    'image': slide.absolute_url(),
                    'title': slide.title,
                    'description': slide.long_description,
                    'url': slide.read_more_link}
            images.append(slide_data)
        self.images = images
        return self.index()

    def getDescription(self, image):
        description = image.get('description', '')
        if hasattr(description, 'output'):
            return self.html2text(description.output)
        else:
            return description

    def getTitle(self, image):
        return image.get('title', '')

    def getImageUrl(self, image):
        return image.get('image', '')

    def getMoreLink(self, image):
        return image.get('url', '')

    def handle_news_items(self):
        """ Gets the most recent updated news/events item"""
        site = getSite()
        catalog = site.portal_catalog
        result = catalog.searchResults({'portal_type': ['News Item', 'Event'],
                                        'review_state': 'published',
                                        'sort_on': 'effective',
                                        'sort_order': 'reverse'},
                                       full_objects=True)[0]

        news = result.getObject()

        return {
            'image':
            "/++resource++eea.climateadapt/frontpage/events.jpg",
            'title': news.Title(),
            'description': news.description,
            'url': news.absolute_url(),

        }

    def handle_last_casestudy(self):
        """ Gets the most recent updated casestudy"""
        site = getSite()
        catalog = site.portal_catalog
        brain = catalog.searchResults({
            'portal_type': 'eea.climateadapt.casestudy',
            'review_state': 'published',
            'sort_on': 'effective',
            'sort_order': 'descending',
        }, full_objects=True)[0]

        cs = brain.getObject()

        return {
            'image':
            "{0}/@@images/primary_photo/?c={1}".format(
                cs.absolute_url(),
                brain.modified and brain.modified.ISO() or ''
            ),
            'title': cs.Title(),
            'description': cs.long_description,
            'url': cs.absolute_url(),

        }

    @view.memoize
    def html2text(self, html):
        if not isinstance(html, basestring):
            return u""
        portal_transforms = api.portal.get_tool(name='portal_transforms')
        data = portal_transforms.convertTo('text/plain',
                                           html, mimetype='text/html')
        text = data.getData()

        return text

    def handle_last_dbitem(self):
        """ Gets the most recent updated aceitem"""
        site = getSite()
        catalog = site.portal_catalog
        result = catalog.searchResults({
            'portal_type': [
                'eea.climateadapt.informationportal',
                'eea.climateadapt.guidancedocument',
                'eea.climateadapt.tool',
                'eea.climateadapt.mapgraphdataset',
                'eea.climateadapt.indicator',
                'eea.climateadapt.organisation'
            ],
            'review_state': 'published',
            'sort_by': 'effective'}, full_objects=True)[0]

        db_item = result.getObject()

        return {
            'image':
            "/++resource++eea.climateadapt/frontpage/aceitem_picture.jpg",
            'title': db_item.Title(),
            'description': db_item.long_description,
            'url': db_item.absolute_url(),

        }

    def handle_last_publication(self):
        """ Gets the most recent updated publication and report"""
        site = getSite()
        catalog = site.portal_catalog
        result = catalog.searchResults({
            'portal_type': 'eea.climateadapt.publicationreport',
            'review_state': 'published',
            'sort_on': 'effective',
            'sort_order': 'descending',
        }, full_objects=True)[0]

        publi = result.getObject()

        return {
            'image':
            "/++resource++eea.climateadapt/frontpage/last_publication.jpg",
            'title': publi.Title(),
            'description': publi.long_description,
            'url': publi.absolute_url(),

        }
