from collective import dexteritytextindexer
from zope.component import adapter
from zope.interface import implementer, implements
from zope.schema import (URI, Bool, Choice, Datetime, Int, List, Text,
                         TextLine, Tuple)

from eea.climateadapt import MessageFactory as _
from eea.climateadapt.interfaces import IClimateAdaptContent
from eea.climateadapt.schema import AbsoluteUrl, PortalType, Uploader, Year
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
from z3c.relationfield.schema import RelationChoice, RelationList


class IAceItem(form.Schema, IImageScaleTraversable):
    """
    Defines content-type schema for Ace Item
    """

    dexteritytextindexer.searchable('title')
    dexteritytextindexer.searchable('long_description')
    dexteritytextindexer.searchable('description')
    dexteritytextindexer.searchable('keywords')
    dexteritytextindexer.searchable('sectors')
    dexteritytextindexer.searchable('climate_impacts')
    dexteritytextindexer.searchable('elements')
    dexteritytextindexer.searchable('year')

    dexteritytextindexer.searchable('websites')
    dexteritytextindexer.searchable('source')

    dexteritytextindexer.searchable('geochars')

    dexteritytextindexer.searchable('data_type')
    dexteritytextindexer.searchable('storage_type')
    dexteritytextindexer.searchable('spatial_layer')
    dexteritytextindexer.searchable('spatial_values')
    dexteritytextindexer.searchable('important')
    dexteritytextindexer.searchable('metadata')
    dexteritytextindexer.searchable('special_tags')

    form.fieldset('default',
                  label=u'Item Description',
                  fields=['title', 'description', 'long_description',
                          'keywords', 'sectors', 'climate_impacts', 'elements',
                          'year', 'featured']
                  )

    form.fieldset('reference_information',
                  label=u'Reference information',
                  fields=['websites', 'source']
                  )

    form.fieldset('geographic_information',
                  label=u'Geographic Information',
                  fields=['geochars', 'comments']
                  )

    form.fieldset('categorization',
                  label=u'Categorization',
                  fields=['special_tags']
                  )

    form.fieldset('backend',
                  label=u'Backend fields',
                  fields=[]
                  )

    # -----------[ "default" fields ]------------------
    # these are the richtext fields from the db:
    # set(['description', 'storedat', 'admincomment', 'comments', 'source',
    #      'keyword', 'textsearch'])

    origin_website = List(title=_(u"Origin website"),
                          required=True,
                          value_type=Choice(
                              vocabulary="eea.climateadapt.origin_website"),
                          )

    partner_organisation  = RelationChoice(title=_(u"Partner organisation"),
                                required=False,
                                vocabulary="eea.climateadapt.organisations")

    health_impacts = Choice(title=_(u"Health impacts"),
                            required=True,
                            vocabulary="eea.climateadapt.health_impacts")

    include_in_observatory = Bool(title=_(u"Include in observatory"),
                     required=False, default=False)

    important = Bool(title=_(u"High importance"),
                     required=False, default=False)

    title = TextLine(title=_(u"Title"),
                     description=u"Item Name (250 character limit)",
                     required=True)

    long_description = RichText(title=(u"Description"),
                                description=u"Provide a description of the "
                                u"item.(5,000 character limit)",
                                required=True)

    description = Text(
        title=_(u"Short summary"),
        required=False,
        description=u"Enter a short summary that will be used in listings.",
    )

    keywords = Tuple(
        title=_(u"Keywords"),
        description=_(u"Describe and tag this item with relevant keywords."
                      u"Press Enter after writing your keyword."),
        required=False,
        value_type=TextLine(),
        missing_value=None,
    )

    form.widget(sectors="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    sectors = List(title=_(u"Sectors"),
                   description=_(u"Select one or more relevant sector policies"
                                 u" that this item relates to."),
                   required=True,
                   missing_value=[],
                   default=None,
                   value_type=Choice(
                       vocabulary="eea.climateadapt.aceitems_sectors",),
                   )

    form.widget(
        climate_impacts="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    climate_impacts = List(
        title=_(u"Climate impacts"),
        description=_(u"Select one or more climate change impact topics that "
                      u"this item relates to."),
        required=True,
        missing_value=[],
        default=None,
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

    year = Year(title=_(u"Year"),
                description=u"Date of publication/release/update of the item",
                required=False
                )

    featured = Bool(title=_(u"Featured"),
                    required=False,
                    default=False,
                    )

    # -----------[ "reference_information" fields ]------------------

    directives.widget('websites', TextLinesWidget)
    websites = Tuple(
        title=_(u"Website"),
        description=_(u"List the Website where the item can be found or is "
                      u"described. Please place each website on a new line"),
        required=False,
        value_type=URI(),
        missing_value=(),
    )

    source = TextLine(title=_(u"Source"),
                      required=False,
                      description=u"Describe the original source of the item "
                                  u"description (250 character limit)")

    # -----------[ "geographic_information" fields ]------------------

    form.widget(geochars='eea.climateadapt.widgets.geochar.GeoCharFieldWidget')
    geochars = Text(title=_(u"Geographic characterisation"),
                    required=True,
                    default=u'{"geoElements":{"element":"GLOBAL", "macrotrans"'
                            u':null,"biotrans":null,"countries":[],'
                            u'"subnational":[],"city":""}}',
                    description=u"Select the characterisation for this item",
                    )

    comments = Text(title=_(u"Comments"), required=False, default=u"",
                    description=u"Comments about this database item"
                                u"[information entered below will not be"
                                u"displayed on the public pages of"
                                u"climate-adapt]")

    contributors = RelationList(
        title=u"Contributors list:",
        default=[],
        description=_(u"Select one or more contributors for this item "),
        value_type=RelationChoice(
            title=_(u"Related"),
            vocabulary="eea.climateadapt.organisations"
            # source=ObjPathSourceBinder(),
            # source=CatalogSource(portal_type='eea.climateadapt.adaptionoption'),
        ),
        required=False,
    )

    # -----------[ "omitted" fields ]------------------
    directives.omitted(IAddForm, 'portal_type')
    directives.omitted(IEditForm, 'portal_type')

    directives.omitted(IAddForm, 'item_link')
    directives.omitted(IEditForm, 'item_link')

    directives.omitted(IAddForm, 'uploader')
    directives.omitted(IEditForm, 'uploader')

    directives.omitted(IAddForm, 'data_type')
    directives.omitted(IEditForm, 'data_type')

    directives.omitted(IAddForm, 'storage_type')
    directives.omitted(IEditForm, 'storage_type')

    directives.omitted(IAddForm, 'spatial_layer')
    directives.omitted(IEditForm, 'spatial_layer')

    directives.omitted(IAddForm, 'spatial_values')
    directives.omitted(IEditForm, 'spatial_values')

    directives.omitted(IAddForm, 'important')
    directives.omitted(IEditForm, 'important')

    directives.omitted(IAddForm, 'metadata')
    directives.omitted(IEditForm, 'metadata')

    # directives.omitted(IAddForm, 'special_tags')
    # directives.omitted(IEditForm, 'special_tags')

    directives.omitted(IAddForm, 'rating')
    directives.omitted(IEditForm, 'rating')

    directives.omitted(IAddForm, 'modification_date')
    directives.omitted(IEditForm, 'modification_date')

    directives.omitted(IAddForm, 'creation_date')
    directives.omitted(IEditForm, 'creation_date')

    directives.omitted(IAddForm, 'id')
    directives.omitted(IEditForm, 'id')

    # -----------[ "backend" fields ]------------------

    special_tags = Tuple(
        title=_(u"Special tagging"),
        required=False,
        value_type=TextLine(),
        missing_value=None,
    )

    portal_type = PortalType(title=_(u"Portal type"),
                             required=False,
                             default=u""
                             )

    item_link = AbsoluteUrl(title=_(u"Item link"),
                            required=False,
                            default=u""
                            )

    uploader = Uploader(title=_(u"Uploaded by"),
                        required=False,
                        default=u""
                        )
    # fix???
    data_type = Choice(title=_(u"Data Type"),
                       required=False,
                       vocabulary="eea.climateadapt.aceitems_datatypes")

    # fix???
    storage_type = Choice(title=_(u"Storage Type"),
                          required=False,
                          vocabulary="eea.climateadapt.aceitems_storagetypes")

    spatial_layer = TextLine(title=_(u"Spatial Layer"),
                             required=False,
                             default=u""
                             )

    spatial_values = List(title=_(u"Countries"),
                          description=_(u"European countries"),
                          required=False,
                          value_type=Choice(
                              vocabulary="eea.climateadapt.ace_countries")
                          )

    important = Bool(title=_(u"High importance"),
                     required=False, default=False)

    metadata = TextLine(title=_(u"Metadata"), required=False,)

    creation_date = Datetime(title=_(u"Created"), required=False,)

    modification_date = Datetime(title=_(u"Last Modified"), required=False,)

    id = TextLine(title=_(u"Object ID"), required=False,)

    # TODO: see if possible to use eea.promotions for this
    # featured = List(title=_(u"Featured in location"),
    #                 description=_(u"TODO: Featured description here"),
    #                 required=False,
    #                 value_type=Choice(
    #                     vocabulary="eea.climateadapt.aceitems_featured",),
    #                 )

    rating = Int(title=_(u"Rating"), required=True, default=0)

    # TODO: rating??? seems to be manually assigned, not computed

    # TODO: storedat: can contain a related measure or project, or a URL
    # if contains inner contents, starts with ace_project_id=<id>
    # or ace_measure_id=<id>

    # supdocs - this is a related field. It seems to point to dlfileentry

    # replacesid - tot un related??

    # scenario: only 3 items have a value: "SCENES SUE", "SCENES ECF", "IPCCS",
    # IPCCSRES A1B
    # the options are stored in a AceItemScenario constant in Java code

    # TODO: special search behaviour, should aggregate most fields


class IPublicationReport(IAceItem):
    """ Publication Report Interface
    """


class IInformationPortal(IAceItem):
    """ Information Portal Interface
    """


class IGuidanceDocument(IAceItem):
    """ Guidance Document Interface
    """


class ITool(IAceItem):
    """ Tool Interface
    """


class IOrganisation(IAceItem):
    """ Organisation Interface"""

    logo = NamedBlobImage(
        title=_(u"Logo"),
        required=False,
    )


class IIndicator(IAceItem):
    """ Indicator Interface"""


class IAction(IAceItem):
    """ Action Interface"""


class IMapGraphDataset(IAceItem):
    """ Maps, Graphs and Datasets Interface
    """
    gis_layer_id = TextLine(
        title=_(u"GIS Layer ID"),
        description=u"Enter the layer id for the map-viewer "
        u"(250 character limit)",
        required=False, default=u"")


class IResearchProject(IAceItem):
    """ ResearchProject Interface
    """


class PublicationReport(dexterity.Container):
    implements(IPublicationReport, IClimateAdaptContent)

    search_type = "DOCUMENT"


class InformationPortal(dexterity.Container):
    implements(IInformationPortal, IClimateAdaptContent)

    search_type = "INFORMATIONSOURCE"


class GuidanceDocument(dexterity.Container):
    implements(IGuidanceDocument, IClimateAdaptContent)

    search_type = "GUIDANCE"


class Tool(dexterity.Container):
    implements(ITool, IClimateAdaptContent)

    search_type = "TOOL"


class Organisation(dexterity.Container):
    implements(IOrganisation, IClimateAdaptContent)

    search_type = "ORGANISATION"


class Indicator(dexterity.Container):
    implements(IIndicator, IClimateAdaptContent)

    search_type = "INDICATOR"


class MapGraphDataset(dexterity.Container):
    implements(IMapGraphDataset, IClimateAdaptContent)

    search_type = "MAPGRAPHDATASET"


class ResearchProject(dexterity.Container):
    implements(IResearchProject, IClimateAdaptContent)

    search_type = "RESEARCHPROJECT"


class Action(dexterity.Container):
    implements(IAction, IClimateAdaptContent)

    search_type = "ACTION"


@adapter(getSpecification(IAceItem['special_tags']), IWidgetsLayer)
@implementer(IFieldWidget)
def SpecialTagsFieldWidget(field, request):
    widget = FieldWidget(field, BetterAjaxSelectWidget(request))
    widget.vocabulary = 'eea.climateadapt.special_tags'

    return widget


@adapter(getSpecification(IAceItem['keywords']), IWidgetsLayer)
@implementer(IFieldWidget)
def KeywordsFieldWidget(field, request):
    widget = FieldWidget(field, BetterAjaxSelectWidget(request))
    widget.vocabulary = 'eea.climateadapt.keywords'
    # widget.vocabulary = 'plone.app.vocabularies.Catalog'

    return widget
