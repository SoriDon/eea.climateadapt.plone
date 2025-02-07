from zope.interface import alsoProvides
from zope.schema import (URI, Bool, Choice, Date, Datetime, Int, List, Text,
                         TextLine, Tuple)

from eea.climateadapt import CcaAdminMessageFactory as _
from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
from plone.app.textfield import RichText
from plone.autoform import directives
from z3c.form.interfaces import IAddForm, IEditForm

from .indicator import IIndicator


# TODO: simplify this schema
class IC3sIndicator(IIndicator):
    """ Indicator Interface"""

    #directives.omitted(IEditForm, "contributor_list")
    #directives.omitted(IAddForm, "contributor_list")
    directives.omitted(IEditForm, "other_contributor")
    directives.omitted(IAddForm, "other_contributor")
    directives.omitted(IEditForm, "map_graphs")
    directives.omitted(IAddForm, "map_graphs")
    #directives.omitted(IEditForm, "publication_date")
    #directives.omitted(IAddForm, "publication_date")

    #directives.omitted(IEditForm, "keywords")
    #directives.omitted(IAddForm, "keywords")
    #directives.omitted(IEditForm, "sectors")
    #directives.omitted(IAddForm, "sectors")
    #directives.omitted(IEditForm, "climate_impacts")
    #directives.omitted(IAddForm, "climate_impacts")
    #directives.omitted(IEditForm, "elements")
    #directives.omitted(IAddForm, "elements")

    #directives.omitted(IEditForm, "websites")
    #directives.omitted(IAddForm, "websites")
    #directives.omitted(IEditForm, "source")
    #directives.omitted(IAddForm, "source")
    #directives.omitted(IEditForm, "special_tags")
    #directives.omitted(IAddForm, "special_tags")
    # directives.omitted(IEditForm, 'comments')
    # directives.omitted(IAddForm, 'comments')

    directives.omitted(IEditForm, "geographic_information")
    directives.omitted(IAddForm, "geographic_information")

    #directives.omitted(IEditForm, "include_in_observatory")
    #directives.omitted(IAddForm, "include_in_observatory")
    #directives.omitted(IEditForm, "health_impacts")
    #directives.omitted(IAddForm, "health_impacts")

    indicator_title = TextLine(
        title=_(u"Indicator title"), required=False
    )

    definition_app = RichText(
        title=(u"App definition"),
        description=u"Provide a short description",
        required=False,
    )

    c3s_identifier = TextLine(
        title=_(u"C3S Identifier"), required=True
    )

    overview_app_toolbox_url = TextLine(
        title=_(u"Overview APP Toolbox URL"), required=True
    )

    overview_app_parameters = Text(title=(u"Overview APP parameters"), required=True)

    details_app_toolbox_url = TextLine(
        title=_(u"Details APP Toolbox URL"), required=False
    )

    details_app_parameters = Text(title=(u"Details APP parameters"), required=False)

    sectors = List(
        title=_(u"Sectors"),
        description=_(
            u"Select one or more relevant sector policies"
            u" that this item relates to."
        ),
        required=False,
        missing_value=[],
        default=None,
        value_type=Choice(
            vocabulary="eea.climateadapt.aceitems_sectors",
        ),
    )

    climate_impacts = List(
        title=_(u"Climate impacts"),
        description=_(
            u"Select one or more climate change impact topics that "
            u"this item relates to."
        ),
        required=False,
        missing_value=[],
        default=None,
        value_type=Choice(
            vocabulary="eea.climateadapt.aceitems_climateimpacts",
        ),
    )

    publication_date = Date(
        title=_(u"Date of item's publication"),
        description=u"The date refers to the latest date of publication of "
        u"the item."
        u" Please use the Calendar icon to add day/month/year. If you want to "
        u"add only the year, please select \"day: 1\", \"month: January\" "
        u"and then the year",
        required=False
    )


alsoProvides(IC3sIndicator["c3s_identifier"], ILanguageIndependentField)
alsoProvides(IC3sIndicator["overview_app_toolbox_url"], ILanguageIndependentField)
alsoProvides(IC3sIndicator["overview_app_parameters"], ILanguageIndependentField)
alsoProvides(IC3sIndicator["details_app_toolbox_url"], ILanguageIndependentField)
alsoProvides(IC3sIndicator["details_app_parameters"], ILanguageIndependentField)
alsoProvides(IC3sIndicator["sectors"], ILanguageIndependentField)
alsoProvides(IC3sIndicator["climate_impacts"], ILanguageIndependentField)
alsoProvides(IC3sIndicator["publication_date"], ILanguageIndependentField)
