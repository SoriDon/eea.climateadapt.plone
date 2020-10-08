from collective import dexteritytextindexer
from eea.climateadapt import MessageFactory as _
from eea.climateadapt.interfaces import IClimateAdaptContent
from eea.climateadapt.widgets.ajaxselect import BetterAjaxSelectWidget
from plone.app.textfield import RichText
from plone.app.widgets.interfaces import IWidgetsLayer
from plone.autoform import directives
from plone.directives import dexterity, form
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from z3c.form.browser.textlines import TextLinesWidget
from z3c.form.interfaces import IAddForm, IEditForm, IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from z3c.relationfield.schema import RelationChoice
from zope.component import adapter
from zope.interface import implementer, implements
from zope.schema import URI, Bool, Choice, Date, Int, List, Text, TextLine, Tuple
from zope.schema import Datetime


class IAceProject(form.Schema, IImageScaleTraversable):
    """
    Defines content-type schema for Ace Project
    """

    dexteritytextindexer.searchable('acronym')
    dexteritytextindexer.searchable('title')
    dexteritytextindexer.searchable('lead')
    dexteritytextindexer.searchable('partners')
    dexteritytextindexer.searchable('keywords')
    dexteritytextindexer.searchable('sectors')
    dexteritytextindexer.searchable('climate_impacts')
    dexteritytextindexer.searchable('elements')
    dexteritytextindexer.searchable('funding')
    dexteritytextindexer.searchable('duration')

    dexteritytextindexer.searchable('websites')
    dexteritytextindexer.searchable('source')

    dexteritytextindexer.searchable('geochars')

    # dexteritytextindexer.searchable('specialtagging')
    dexteritytextindexer.searchable('special_tags')
    dexteritytextindexer.searchable('important')
    dexteritytextindexer.searchable('spatial_layer')
    dexteritytextindexer.searchable('spatial_values')

    form.fieldset('default',
                  label=u'Item Description',
                  fields=['acronym', 'title', 'lead',
                          'long_description', 'partners', 'keywords', 'sectors',
                          'climate_impacts', 'elements', 'funding',
                          'funding_programme', 'duration', 'featured'])

    form.fieldset('reference_information',
                  label=u'Reference information',
                  fields=['websites', 'source',
                          'special_tags', 'partners_source_link'])

    form.fieldset('geographic_information',
                  label=u'Geographic Information',
                  fields=['geochars', 'comments'])

    form.fieldset('categorization',
                  label=u'Inclusion in the Health Observatory',
                  fields=['include_in_observatory', 'health_impacts']
                  )

    # -----------[ "default" fields ]------------------


    # These fields are richtext in the db:
    #set(['keywords', 'partners', 'admincomment', 'abstracts', 'source'])
    origin_website = List(title=_(u"Origin website"),
                          required=True,
                          value_type=Choice(
                              vocabulary="eea.climateadapt.origin_website"),
                          )

    image = NamedBlobImage(
        title=_(u"Thumbnail"),
        description=_(u"Upload a representative picture or logo for the item."
                      u" Recomanded size 360/180, aspect ratio 2x"),
        required=False,
    )

    funding_programme = Choice(title=_(u"Funding Programme"),
                            required = False,
                            #value_type = Choice(
                                vocabulary = "eea.climateadapt.funding_programme"
                            #    )
                            )

    acronym = TextLine(title=_(u"Acronym"),
                       description=_(u"Acronym of the project"),
                       required=True,
                       )

    title = TextLine(title=_(u"Title"),
                     description=_(u"Project title or name"),
                     required=True,
                     )

    dexteritytextindexer.searchable('long_description')
    long_description = RichText(
        title=_(u"Abstracts"),
        description=_(u"Provide information focusing on project output. "
                      u"Possibly on specific Website features."),
        required=True,
    )

    lead = TextLine(
        title=_(u"Lead"),
        description=_(u"Lead organisation or individual of the project"),
        required=True,
    )

    dexteritytextindexer.searchable('partners')
    partners = RichText(
        title=_(u"Partners"),
        description=_(u"Provide information about project partners "
                      u"(organisation names)."),
        required=True,
    )

    dexteritytextindexer.searchable('keywords')
    keywords = Tuple(
        title=_(u"Keywords"),
        description=_(u"Provide Keywords related to the project. "
                      u"Press Enter after writing your keyword."),
        required=False,
        value_type=TextLine(),
        missing_value=(None),
    )

    health_impacts = List(title=_(u"Health impacts"),
                            required = False,
                            value_type = Choice(
                                vocabulary = "eea.climateadapt.health_impacts")
                            )

    publication_date = Date(title=_(u"Date of item's creation"),
                description=u"The date refers to the moment in which the item "
                            u"has been prepared by contributing expeerts to be "
                            u"submitted for the publication in Climate "
                            u"ADAPTPublication/last update date",
                required=False
                )

    include_in_observatory = Bool(title=_(u"Include in observatory"),
                     required=False, default=False)

    form.widget(sectors="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    sectors = List(
        title=_(u"Sectors"),
        description=_(u"Select one or more relevant sector policies that "
                      u"this item relates to."),
        required=True,
        missing_value=[],
        default=None,
        value_type=Choice(
            vocabulary="eea.climateadapt.aceitems_sectors",),
    )

    form.widget(climate_impacts="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    climate_impacts = List(
        title=_(u"Climate impacts"),
        description=_(u"Select one or more climate change impact topics that "
                      u"this item relates to."),
        missing_value=[],
        default=None,
        required=True,
        value_type=Choice(
            vocabulary="eea.climateadapt.aceitems_climateimpacts",),
    )

    form.widget(elements="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    elements = List(title=_(u"Elements"),
                    description=_(u"Select one or more elements."),
                    required=False,
                    value_type=Choice(
                        vocabulary="eea.climateadapt.aceitems_elements",),
                    )

    funding = TextLine(title=_(u"Further information on the funding"),
                       description=_(u"Provide source of funding"),
                       required=False,
                       )

    duration = TextLine(
        title=_(u"Duration"),
        description=_(u"Provide duration of project - Start and end date [yr]"),
        required=False,
    )

    featured = Bool(title=_(u"Featured"),
                     required=False,
                     default=False,
                     )

    # -----------[ "reference_information" fields ]------------------
    directives.widget('websites', TextLinesWidget)
    websites = Tuple(
        title=_(u"Websites"),
        description=_(u"List the Websites where the item can be found or is "
                      u"described. Please place each website on a new line"),
        required=False,
        value_type=URI(),
        missing_value=(),
    )

    dexteritytextindexer.searchable('source')
    source = TextLine(
        title=_(u"Reference"),
        description=_(u"Provide source from which project was retrieved (e.g. "
                      u"specific DB) "),
        required=False)

    # -----------[ "geographic_information" fields ]------------------
    form.widget(geochars='eea.climateadapt.widgets.geochar.GeoCharFieldWidget')
    geochars = Text(title=_(u"Geographic characterisation"),
                    required=True,
                    default=u'{"geoElements":{"element":"GLOBAL", "macrotrans":null,"biotrans":null,"countries":[],"subnational":[],"city":""}}',
                    description=u"Select the characterisation for this item",
                    )

    comments = Text(
        title=_(u"Source"),
        description=_(u"Comments about this database item [information entered"
                      u" below will not be displayed on the public pages of "
                      u"climate-adapt]"),
        required=False,
    )

    # -----------[ "omitted" fields ]------------------

    directives.omitted(IEditForm, 'specialtagging')
    directives.omitted(IAddForm, 'specialtagging')
    # directives.omitted(IEditForm, 'special_tags')
    # directives.omitted(IAddForm, 'special_tags')
    directives.omitted(IEditForm, 'important')
    directives.omitted(IAddForm, 'important')
    directives.omitted(IEditForm, 'rating')
    directives.omitted(IAddForm, 'rating')
    directives.omitted(IEditForm, 'spatial_layer')
    directives.omitted(IAddForm, 'spatial_layer')
    directives.omitted(IEditForm, 'spatial_values')
    directives.omitted(IAddForm, 'spatial_values')
    directives.omitted(IAddForm, 'modification_date')
    directives.omitted(IEditForm, 'modification_date')
    directives.omitted(IAddForm, 'creation_date')
    directives.omitted(IEditForm, 'creation_date')
    directives.omitted(IAddForm, 'id')
    directives.omitted(IEditForm, 'id')

    # end

    creation_date = Datetime(title=_(u"Created"), required=False,)

    modification_date = Datetime(title=_(u"Last Modified"), required=False,)

    id = TextLine(title=_(u"Object ID"), required=False,)

    specialtagging = TextLine(
        title=_(u"Special Tagging"),
        description=_(u"Special tags that allow for linking the item"),
        required=False,
        )

    # special_tags = TextLine(
    #     title=_(u"Special Tagging"),
    #     description=_(u"Special tags that allow for linking the item"),
    #     required=False,
    #     )

    special_tags = Tuple(
        title=_(u"Special tagging"),
        required=False,
        value_type=TextLine(),
        missing_value=(None),
    )

    important = Bool(title=_(u"Important"),
                     required=False,
                     default=False,
                     )

    rating = Int(title=_(u"Rating"), required=True, default=0)

    spatial_layer = TextLine(
        title=_(u"Spatial Layer"), required=False, default=u"",
        )

    spatial_values = List(title=_(u"Countries"),
                          description=_(u"European countries"),
                          required=False,
                          value_type=Choice(
                              vocabulary="eea.climateadapt.ace_countries"),
                          )

    partners_source_link = URI(title=_(u"Partners Source Link"),
                              description=(u"Provide URL from project partners"),
                              required=False,
                              )

class AceProject(dexterity.Container):
    implements(IAceProject, IClimateAdaptContent)

    search_type = "RESEARCHPROJECT"


@adapter(getSpecification(IAceProject['keywords']), IWidgetsLayer)
@implementer(IFieldWidget)
def KeywordsFieldWidget(field, request):
    widget = FieldWidget(field, BetterAjaxSelectWidget(request))
    widget.vocabulary = 'eea.climateadapt.keywords'
    return widget


@adapter(getSpecification(IAceProject['special_tags']), IWidgetsLayer)
@implementer(IFieldWidget)
def SpecialTagsFieldWidget(field, request):
    widget = FieldWidget(field, BetterAjaxSelectWidget(request))
    widget.vocabulary = 'eea.climateadapt.special_tags'
    return widget
