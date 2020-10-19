""" CaseStudy and AdaptationOption implementations
"""

import json
import logging
from datetime import date

from collective import dexteritytextindexer
from zope.component import adapter
from zope.interface import implementer, implements
from zope.schema import (URI, Bool, Choice, Date, Datetime, Int, List, Text,
                         TextLine, Tuple)

from eea.climateadapt import MessageFactory as _
from eea.climateadapt.interfaces import IClimateAdaptContent
from eea.climateadapt.sat.datamanager import queue_callback
from eea.climateadapt.sat.handlers import HANDLERS
from eea.climateadapt.sat.settings import get_settings
from eea.climateadapt.sat.utils import _measure_id, to_arcgis_coords
from eea.climateadapt.schema import Year
#from eea.climateadapt.schema import Date
from eea.climateadapt.utils import _unixtime, shorten
from eea.climateadapt.vocabulary import BIOREGIONS
from eea.climateadapt.widgets.ajaxselect import BetterAjaxSelectWidget
from eea.rabbitmq.plone.rabbitmq import queue_msg
from plone.api.portal import get_tool
from plone.app.contenttypes.interfaces import IImage
from plone.app.textfield import RichText
from plone.app.widgets.interfaces import IWidgetsLayer
from plone.autoform import directives
from plone.directives import dexterity, form
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from z3c.form.browser.textlines import TextLinesWidget
from z3c.form.interfaces import IAddForm, IEditForm, IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from z3c.relationfield.schema import RelationChoice, RelationList

logger = logging.getLogger('eea.climateadapt.acemeasure')


class IAceMeasure(form.Schema, IImageScaleTraversable):
    """
    Defines content-type schema for Ace Measure
    """

    dexteritytextindexer.searchable('challenges')
    dexteritytextindexer.searchable('climate_impacts')
    dexteritytextindexer.searchable('contact')
    dexteritytextindexer.searchable('cost_benefit')
    dexteritytextindexer.searchable('geochars')
    dexteritytextindexer.searchable('implementation_time')
    dexteritytextindexer.searchable('important')
    dexteritytextindexer.searchable('keywords')
    dexteritytextindexer.searchable('legal_aspects')
    dexteritytextindexer.searchable('lifetime')
    dexteritytextindexer.searchable('long_description')
    dexteritytextindexer.searchable('description')
    dexteritytextindexer.searchable('measure_type')
    dexteritytextindexer.searchable('objectives')
    dexteritytextindexer.searchable('sectors')
    dexteritytextindexer.searchable('solutions')
    dexteritytextindexer.searchable('source')
    dexteritytextindexer.searchable('spatial_layer')
    dexteritytextindexer.searchable('spatial_values')
    dexteritytextindexer.searchable('special_tags')
    dexteritytextindexer.searchable('stakeholder_participation')
    dexteritytextindexer.searchable('success_limitations')
    dexteritytextindexer.searchable('title')
    dexteritytextindexer.searchable('websites')
    dexteritytextindexer.searchable('year')
    dexteritytextindexer.searchable('publication_date')

    form.fieldset('default',
                  label=u'Item Description',
                  fields=['publication_date', 'title', 'long_description',
                          'description', 'climate_impacts', 'keywords',
                          'sectors', 'year', 'featured',
                          ]
                  )

    form.fieldset('additional_details',
                  label=u'Additional Details',
                  fields=['stakeholder_participation',
                          'success_limitations',
                          'cost_benefit', 'legal_aspects',
                          'implementation_time', 'lifetime']
                  )

    #form.fieldset('inclusion_health_observatory',
    #              label=u'Inclusion in health observatory',
    #              fields=['include_in_observatory', 'health_impacts']
    #              )

    form.fieldset('reference_information',
                  label=u'Reference information',
                  fields=[  # 'contact',
                      'websites', 'source', 'special_tags', 'comments']
                  )

# richtext fields in database:
# set(['legalaspects', 'implementationtime', 'description', 'source',
# 'objectives', 'stakeholderparticipation', 'admincomment', 'comments',
# 'challenges', 'keywords', 'contact', 'solutions', 'costbenefit',
# 'succeslimitations', 'lifetime'])

    form.fieldset('geographic_information',
                  label=u'Geographic Information',
                  fields=['governance_level', 'geochars']
                  )

    form.fieldset('categorization',
                  label=u'Inclusion in the Health Observatory',
                  fields=['include_in_observatory', 'health_impacts']
                  )

    # -----------[ "default" fields ]------------------

    title = TextLine(title=_(u"Title"),
                     description=_(u"Name of the case study clearly "
                                   u"identifying its scope and location "
                                   u"(250 character limit)"),
                     required=True)

    long_description = RichText(title=_(u"Description"), required=True,)

    description = Text(
        title=_(u"Short summary"),
        required=False,
        description=u"Enter a short summary that will be used in listings.",
    )

    form.widget(
        climate_impacts="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    climate_impacts = List(
        title=_(u"Climate impacts"),
        missing_value=[],
        default=None,
        description=_(u"Select one or more climate change impact topics that "
                      u"this item relates to:"),
        required=True,
        value_type=Choice(
            vocabulary="eea.climateadapt.aceitems_climateimpacts",),
    )

    keywords = Tuple(
        title=_(u"Keywords"),
        description=_(u"Describe and tag this item with relevant keywords. "
                      u"Press Enter after writing your keyword. "
                      u"Use specific and not general key words (e.g. avoid "
                      u"words as: adaption, climate change, measure, "
                      u"integrated approach, etc.):"),
        required=False,
        value_type=TextLine(),
        missing_value=(None),
    )

    form.widget(sectors="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    sectors = List(title=_(u"Sectors"),
                   description=_(u"Select one or more relevant sector policies"
                                 u" that this item relates to:"),
                   required=True,
                   missing_value=[],
                   default=None,
                   value_type=Choice(
        vocabulary="eea.climateadapt.aceitems_sectors",),
    )

    year = Year(title=_(u"Year"),
                description=u"Date of publication/release/update of the items "
                u"related source",
                required=False,)

    publication_date = Date(title=_(u"Date of item's creation"),
                description=u"The date refers to the moment in which the item "
                            u"has been prepared by contributing expeerts to be "
                            u"submitted for the publication in Climate "
                            u"ADAPTPublication/last update date",
                required=False
                )

    featured = Bool(
        title=_(u"Featured"),
        description=u"Feature in search and Case Study Search Tool",
        required=False,
        default=False)

    # -----------[ "additional_details" fields ]------------------

    dexteritytextindexer.searchable('stakeholder_participation')
    stakeholder_participation = RichText(
        title=_(u"Stakeholder participation"), required=False,
        default=u"",
        description=_(u"Describe the Information about actors involved, the "
                      u"form of participation and the participation process. "
                      u" Focus should be on the level of participation needed "
                      u"and/or adopted already (from information, to full "
                      u"commitment in the deliberation/implementation "
                      u"process), with useful notes e.g. regarding "
                      u"motivations. (5,000 character limit)"))

    dexteritytextindexer.searchable('success_limitations')
    success_limitations = RichText(
        title=_(u"Success / limitations"), required=False, default=u"",
        description=_(u"Describe factors that are decisive for a successful "
                      u"implementation and expected challenges or limiting "
                      u"factors which may hinder the process and need to be "
                      u"considered (5,000 character limit)"))

    dexteritytextindexer.searchable('cost_benefit')
    cost_benefit = RichText(
        title=_(u"Cost / Benefit"), required=False, default=u"",
        description=_(u"Describe costs (possibly providing quantitative "
                      u"estimate) and funding sources. Describe benefits "
                      u"provided by implemented solutions, i.e.: positive "
                      u"outcomes related climate change adaptation, "
                      u"co-benefits in other areas, quantitative estimation "
                      u"of benefits and related methodologies (e.g. "
                      u"monetization of benefits for cost benefit analysis, "
                      u"indicators of effectiveness of actions implemented, "
                      u"etc.) (5,000 characters limit)"))

    dexteritytextindexer.searchable('legal_aspects')
    legal_aspects = RichText(
        title=_(u"Legal aspects"),
        required=False,
        default=u"",
        description=_(u"Describe the Legislation "
                      u"framework from which the case "
                      u"originated, relevant institutional"
                      u" opportunities and constrains, "
                      u"which determined the case as it "
                      u"is (5000 character limit):"))

    dexteritytextindexer.searchable('implementation_time')
    implementation_time = RichText(
        title=_(u"Implementation Time"), required=False, default=None,
        description=_(u"Describe the time needed to implement the measure. "
                      u"Include: Time frame, e.g. 5-10 years, Brief "
                      u"explanation(250 char limit)"))

    dexteritytextindexer.searchable('lifetime')
    lifetime = RichText(title=_(u"Lifetime"),
                        required=False,
                        default=u"",
                        description=u"Describe the lifetime of the measure: "
                        u"Time frame, e.g. 5-10 years, Brief explanation "
                        u"(250 char limit)")

    # -----------[ "reference_information" fields ]------------------

    directives.widget('websites', TextLinesWidget)
    websites = Tuple(
        title=_(u"Websites"),
        description=_(u"List the Websites where the option can be found"
                      u" or is described. Note: may refer to the original "
                      u"document describing a measure and does not have to "
                      u"refer back to the project e.g. collected measures. "
                      u"NOTE: Add http:// in front of every website link."),
        required=False,
        value_type=URI(),
        missing_value=(),
    )

    dexteritytextindexer.searchable('source')
    source = TextLine(title=_(u"References"),
                      required=False,
                      description=_(u"Describe the references (projects, a"
                                  u" tools reports,etc.) used for the "
                                  u" preparation of the adaptation option "
                                  u" description"))

    # -----------[ "geographic_information" fields ]------------------

    form.widget(
        governance_level="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    governance_level = List(
        title=_(u"Governance Level"),
        description=_(u"Select the one governance level that relates to this "
                      u"adaptation option"),
        required=False,
        value_type=Choice(
            vocabulary="eea.climateadapt.aceitems_governancelevel",),
    )

    form.widget(geochars='eea.climateadapt.widgets.geochar.GeoCharFieldWidget')
    geochars = Text(title=_(u"Geographic characterisation"),
                    required=True,
                    default=u"""{
                    "geoElements":{"element":"GLOBAL",
                    "macrotrans":null,"biotrans":null,"countries":[],
                    "subnational":[],"city":""}}""",
                    description=u"Select the characterisation for this item",
                    )

    comments = Text(title=_(u"Comments"), required=False, default=u"",
                    description=_(u"Comments about this database item "
                                  u"[information entered below will not be "
                                  u"displayed on the public pages of "
                                  u"climate-adapt]")
                    )

    origin_website = List(title=_(u"Origin website"),
                          required=True,
                          value_type=Choice(
                              vocabulary="eea.climateadapt.origin_website"),
                        )

    image = NamedBlobImage(
        title=_(u"Thumbnail or logo"),
        description=_(u"Upload a representative picture or logo for the item."
                      u" Recomanded size 360/180, aspect ratio 2x"),
        required=False,
    )

    contributors = RelationList(
        title=u"Contributor(s)",
        default=[],
        description=_(u"Select from the Climate ADAPT Organisation items the "
                      u"organisations contributing to/ involved in this item"),
        value_type=RelationChoice(
            title=_(u"Related"),
            vocabulary="eea.climateadapt.organisations"
            # source=ObjPathSourceBinder(),
            # source=CatalogSource(portal_type='eea.climateadapt.adaptionoption'),
        ),
        required=False,
    )

    # -----------[ "omitted" fields ]------------------

    directives.omitted(IEditForm, 'implementation_type')
    directives.omitted(IAddForm, 'implementation_type')
    directives.omitted(IEditForm, 'spatial_layer')
    directives.omitted(IAddForm, 'spatial_layer')
    directives.omitted(IEditForm, 'spatial_values')
    directives.omitted(IAddForm, 'spatial_values')
    directives.omitted(IEditForm, 'elements')
    directives.omitted(IAddForm, 'elements')
    directives.omitted(IEditForm, 'measure_type')
    directives.omitted(IAddForm, 'measure_type')
    directives.omitted(IEditForm, 'important')
    directives.omitted(IAddForm, 'important')
    directives.omitted(IEditForm, 'rating')
    directives.omitted(IAddForm, 'rating')
    directives.omitted(IAddForm, 'modification_date')
    directives.omitted(IEditForm, 'modification_date')
    directives.omitted(IAddForm, 'creation_date')
    directives.omitted(IEditForm, 'creation_date')
    directives.omitted(IAddForm, 'id')
    directives.omitted(IEditForm, 'id')
    # end

    implementation_type = Choice(
        title=_(u"Implementation Type"), required=False, default=None,
        vocabulary="eea.climateadapt.acemeasure_implementationtype"
    )

    spatial_layer = TextLine(
        title=_(u"Spatial Layer"), required=False, default=u"")

    spatial_values = List(title=_(u"Countries"),
                          description=_(u"European countries"),
                          required=False,
                          value_type=Choice(
                              vocabulary="eea.climateadapt.ace_countries"))

    # TODO: startdate, enddate, publicationdate have no values in DB
    # TODO: specialtagging is not used in any view jsp, only in add and edit
    # views

    form.widget(elements="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    elements = List(title=_(u"Elements"),
                    description=_(u"TODO: Elements description here"),
                    required=False,
                    value_type=Choice(
                        vocabulary="eea.climateadapt.aceitems_elements",),
                    )

    measure_type = Choice(title=_(u"Measure Type"),
                          required=True,
                          default="A",
                          vocabulary="eea.climateadapt.acemeasure_types")

    health_impacts = List(title=_(u"Health impacts"),
                            required = False,
                            value_type = Choice(
                                vocabulary = "eea.climateadapt.health_impacts")
                            )


    include_in_observatory = Bool(title=_(u"Include in observatory"),
                     required=False, default=False)

    important = Bool(title=_(u"High importance"), required=False,
                     default=False)

    rating = Int(title=_(u"Rating"), required=True, default=0)

    special_tags = Tuple(
        title=_(u"Special tagging"),
        required=False,
        value_type=TextLine(),
        missing_value=(None),
    )

    creation_date = Datetime(title=_(u"Created"), required=False,)

    modification_date = Datetime(title=_(u"Last Modified"), required=False,)

    id = TextLine(title=_(u"Object ID"), required=False,)

    # dexteritytextindexer.searchable('summary')
    # summary = Text(title=_(u"Summary"), required=False, default=u"")


class IAdaptationOption(IAceMeasure):
    """ Adaptation Option
    """

    directives.omitted(IEditForm, 'year')
    directives.omitted(IAddForm, 'year')
    directives.omitted(IEditForm, 'featured')
    directives.omitted(IAddForm, 'featured')

    form.widget(category="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    category = List(
        title=_(u"General category"),
        description=_(u"Select one or more categories of adaptation options. "
                      u"The 3 options are:"),
        required=False,
        value_type=Choice(
            vocabulary="eea.climateadapt.aceitems_category",),
    )

    form.widget(ipcc_category="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    ipcc_category = List(
        title=_(u"IPCC adaptation options categories"),
        description=_(u"Select one or more categories of adaptation options. "
                      u"The options are:"),
        required=False,
        value_type=Choice(
            vocabulary="eea.climateadapt.aceitems_ipcc_category",),
    )

    publication_date = Date(title=_(u"Date of item's creation"),
                description=u"The date refers to the moment in which the item "
                            u"has been prepared or  updated by contributing "
                            u"experts to be submitted for the publication in "
                            u"Climate ADAPT",
                required=False
                )


class ICaseStudy(IAceMeasure):  # , IGeolocatable):
    """ Case study
    """

    directives.omitted(IEditForm, 'year')
    directives.omitted(IAddForm, 'year')
    directives.omitted(IEditForm, 'featured')
    directives.omitted(IAddForm, 'featured')
    directives.omitted(IEditForm, 'primephoto')
    directives.omitted(IAddForm, 'primephoto')
    directives.omitted(IEditForm, 'supphotos')
    directives.omitted(IAddForm, 'supphotos')
    #directives.omitted(IEditForm, 'relatedItems')
    #directives.omitted(IAddForm, 'relatedItems')

    challenges = RichText(
        title=_(u"Challenges"), required=True, default=None,
        description=_(u"Describe what are the main climate change "
                      u"impacts/risks and related challenges addressed by the "
                      u"adaptation solutions proposed by the case study. "
                      u"Possibly include quantitate scenarios/projections of "
                      u"future climate change considered by the case study "
                      u"(5,000 characters limit):"),
    )

    objectives = RichText(
        title=_(u"Objectives"), required=True, default=None,
        description=_(u"Describe the objectives which triggered the "
                      u"adaptation measures (5,000 characters limit):"),
    )

    solutions = RichText(
        title=_(u"Solutions"), required=True, default=None,
        description=_(u"Describe the climate change adaptation solution(s) "
                      u"implemented (5,000 characters limit):"),
    )

    form.widget(relevance="z3c.form.browser.checkbox.CheckBoxFieldWidget")
    relevance = List(
        title=_(u"Relevance"),
        required=True,
        missing_value=[],
        default=None,
        description=_(u"Select only one category below that best describes "
                      u"how relevant this case study is to climate change "
                      u"adaptation:"),
        value_type=Choice(
            vocabulary="eea.climateadapt.aceitems_relevance",),
    )

    contact = RichText(
        title=_(u"Contact"), required=True, default=u"",
        description=_(u"Contact of reference (institution and persons) who is "
                      u"directly involved in the development and "
                      u"implementation of the case. (500 char limit) "))

    adaptationoptions = RelationList(
        title=u"Adaptation measures implemented in the case:",
        default=[],
        description=_(u"Select one or more adaptation options that this item "
                      u"relates to:"),
        value_type=RelationChoice(
            title=_(u"Related"),
            vocabulary="eea.climateadapt.adaptation_options"
            # source=ObjPathSourceBinder(),
            # source=CatalogSource(portal_type='eea.climateadapt.adaptionoption'),
        ),
        required=False,
    )

    primary_photo = NamedBlobImage(
        title=_(u"Primary photo"),
        required=False,
    )

    primary_photo_copyright = TextLine(
        title=_(u"Primary Photo Copyright"), required=False, default=u"",
        description=_(u"Copyright statement or other rights information for  "
                      u"the primary photo."))

    # BBB fields, only used during migration
    primephoto = RelationChoice(
        title=_(u"Prime photo"),
        source=ObjPathSourceBinder(object_provides=IImage.__identifier__),
        required=False,
    )
    supphotos = RelationList(
        title=u"Gallery",
        default=[],
        value_type=RelationChoice(
            title=_(u"Related"),
            source=ObjPathSourceBinder(
                object_provides=IImage.__identifier__)
        ),
        required=False,
    )


# this was to fix (probably) a bug in plone.app.widgets. This fix is no longer
# needed with plone.app.widgets 1.10.dev4
# @adapter(getSpecification(ICaseStudy['adaptationoptions']), IWidgetsLayer)
# @implementer(IFieldWidget)
# def AdaptationOptionsFieldWidget(field, request):
#     """ The vocabulary view is overridden so that
#         the widget will show only adaptation options
#         Check browser/overrides.py for more details
#     """
#     import pdb
#     pdb.set_trace()
#     widget = FieldWidget(field, RelatedItemsWidget(request))
#     widget.vocabulary = 'eea.climateadapt.adaptation_options'
#     widget.vocabulary_override = True
#
#     return widget


class CaseStudy(dexterity.Container):
    implements(ICaseStudy, IClimateAdaptContent)

    search_type = "ACTION"

    def _short_description(self):
        v = self.long_description
        html = v and v.output.strip() or ''

        if html:
            portal_transforms = get_tool(name='portal_transforms')
            data = portal_transforms.convertTo('text/plain',
                                               html, mimetype='text/html')
            html = shorten(data.getData(), to=100)

        return html

    def _get_area(self):
        if not self.geochars:
            return ''

        try:
            chars = json.loads(self.geochars)
            els = chars['geoElements']

            if 'biotrans' not in els.keys():
                return ''
            bio = els['biotrans']

            if not bio:
                return ''
            bio = BIOREGIONS[bio[0]]    # NOTE: we take the first one

            return bio
        except:
            logger.exception("Error getting biochar area for case study %s",
                             self.absolute_url())

            return ''

    def _repr_for_arcgis(self):
        is_featured = getattr(self, 'featured', False)
        # is_highlight = getattr(self, 'highlight', False)
        # classes = {
        #     (False, False): 'normal',
        #     (True, False): 'featured',
        #     (True, True): 'featured-highlight',
        #     (False, True): 'highlight',
        # }
        # client_cls = classes[(is_featured, is_highlight)]
        client_cls = is_featured and 'featured' or 'normal'

        if self.geolocation and self.geolocation.latitude:
            geo = to_arcgis_coords(
                self.geolocation.longitude,
                self.geolocation.latitude)
            geometry = {
                'x': geo[0],
                'y': geo[1],
            }
        else:
            geometry = {'x': '', 'y': ''}

        if self.effective_date is not None:
            if hasattr(self.effective_date, 'date'):
                effective = self.effective_date.date()
            else:
                effective = self.effective_date.asdatetime().date()
        else:
            effective = date.today()        # todo? item not published?

        today = date.today()
        timedelta = today - effective

        if timedelta.days > 90:
            newitem = 'no'
        else:
            newitem = 'yes'

        res = {
            'attributes': {
                'area': self._get_area(),
                'itemname': self.Title(),
                'desc_': self._short_description(),
                'website': self.websites and self.websites[0] or '',
                'sectors': ';'.join(self.sectors or []),
                'risks': ';'.join(self.climate_impacts or []),
                'measureid': getattr(self, '_acemeasure_id', '') or self.UID(),
                'featured': is_featured and 'yes' or 'no',
                'newitem': newitem,
                'casestudyf': 'CASESEARCH;',    # TODO: implement this
                'client_cls': client_cls,
                'Creator': self.creators[-1],
                'CreationDate': _unixtime(self.creation_date),
                'EditDate': _unixtime(self.modification_date),
                'Editor': self.workflow_history[
                    'cca_items_workflow'][-1]['actor'],
                'EffectiveDate': _unixtime(self.effective_date),
            },
            'geometry': geometry,
        }

        return res


class AdaptationOption(dexterity.Container):
    """ The AdaptationObject content type.
    """

    implements(IAdaptationOption, IClimateAdaptContent)

    search_type = "MEASURE"


@adapter(getSpecification(IAceMeasure['keywords']), IWidgetsLayer)
@implementer(IFieldWidget)
def KeywordsFieldWidget(field, request):
    """ The vocabulary view is overridden so that
        the widget will work properly
        Check browser/overrides.py for more details
    """
    widget = FieldWidget(field, BetterAjaxSelectWidget(request))
    widget.vocabulary = 'eea.climateadapt.keywords'

    return widget


@adapter(getSpecification(IAceMeasure['special_tags']), IWidgetsLayer)
@implementer(IFieldWidget)
def SpecialTagsFieldWidget(field, request):
    widget = FieldWidget(field, BetterAjaxSelectWidget(request))
    widget.vocabulary = 'eea.climateadapt.special_tags'

    return widget


def handle_for_arcgis_sync(obj, event):
    """ Dispatch event to RabbitMQ to trigger synchronization to ArcGIS
    """
    event_name = event.__class__.__name__
    uid = _measure_id(obj)
    msg = "{0}|{1}".format(event_name, uid)
    logger.info("Queuing RabbitMQ message: %s", msg)

    settings = get_settings()

    if settings.skip_rabbitmq:
        queue_callback(lambda: HANDLERS[event_name](obj, uid))

        return

    try:
        queue_msg(msg, queue='eea.climateadapt.casestudies')
    except Exception:
        logger.exception(
            "Couldn't queue RabbitMQ message for case study event")


def handle_measure_added(obj, event):
    """ Assign a new measureid to this AceMeasure
    """

    catalog = get_tool(name='portal_catalog')
    ids = sorted(filter(None, catalog.uniqueValuesFor('acemeasure_id')))
    obj._acemeasure_id = ids[-1] + 1
    obj.reindexObject(idxs=['acemeasure_id'])
