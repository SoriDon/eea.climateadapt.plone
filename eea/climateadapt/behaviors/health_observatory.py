from zope.interface import provider
from zope.schema import (URI, Bool, Choice, Date, Datetime, List, Text,
                         TextLine, Tuple)

from eea.climateadapt import CcaAdminMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model


@provider(IFormFieldProvider)
class IHealthObservatoryMetadata(model.Schema):
    model.fieldset(
        "health_inclusion",
        label=u"Inclusion in the subsites",
        fields=["include_in_observatory",
                "include_in_mission", "health_impacts"],
    )

    include_in_observatory = Bool(
        title=_(u"Include in observatory"), required=False, default=False
    )

    include_in_mission = Bool(
        title=_(u"Include in the Mission Portal"), required=False, default=False
    )

    health_impacts = List(
        title=_(u"Health impacts"),
        required=False,
        value_type=Choice(vocabulary="eea.climateadapt.health_impacts"),
    )
