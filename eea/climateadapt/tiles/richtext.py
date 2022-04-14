from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover.tiles.richtext import IRichTextTile
from collective.cover.tiles.richtext import RichTextTile
from eea.climateadapt import CcaAdminMessageFactory as _
from zope import schema
from zope.interface import implements


class IRichTextWithTitle(IRichTextTile):
    """
    """

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    dont_strip = schema.Bool(
        title=_(u"Don't sanitize HTML"),
        description=_(u"Use with care!"),
        default=False,
    )

    title_level = schema.Choice(
        title=_(u"Change header style."),
        default="h1",
        vocabulary="eea.climateadapt.rich_header_level",
    )


class RichTextWithTitle(RichTextTile):
    """
    """

    implements(IRichTextWithTitle)

    index = ViewPageTemplateFile('pt/richtext_with_title.pt')
