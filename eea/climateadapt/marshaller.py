import json
import logging
from Products.CMFCore.utils import getToolByName
from eea.climateadapt.city_profile import ICityProfile
from eea.climateadapt.vocabulary import BIOREGIONS
from eea.climateadapt.vocabulary import SUBNATIONAL_REGIONS
from eea.climateadapt.vocabulary import ace_countries_dict
from eea.rdfmarshaller.dexterity import Dexterity2Surf
from eea.rdfmarshaller.interfaces import ISurfResourceModifier
from eea.rdfmarshaller.interfaces import ISurfSession
from eea.rdfmarshaller.value import Value2Surf
from plone.app.contenttypes.interfaces import ICollection
from plone.dexterity.interfaces import IDexterityContent
from plone.formwidget.geolocation.interfaces import IGeolocation
from plone.namedfile.interfaces import INamedBlobFile
from plone.namedfile.interfaces import INamedBlobImage
from zope.component import adapts
from zope.interface import implements
# import rdflib

logger = logging.getLogger('eea.climateadapt')


class Collection2Surf(Dexterity2Surf):
    adapts(ICollection, ISurfSession)

    @property
    def blacklist_map(self):
        ptool = getToolByName(self.context, 'portal_properties')
        props = getattr(ptool, 'rdfmarshaller_properties', None)
        if props:
            blacklist = props.getProperty('blacklist') + ('query', )
            return list(
                props.getProperty('%s_blacklist' % self.portalType.lower(),
                                  blacklist)
            )
        else:
            self._blacklist.append('query')
            return self._blacklist


class GeoCharsFieldModifier(object):
    """Add geographic information to rdf export
    """

    implements(ISurfResourceModifier)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource to include geochar terms
        """
        if not hasattr(self.context, 'geochars'):
            return

        value = self.context.geochars
        if not value:
            return u""

        value = json.loads(value)

        order = ['element', 'macrotrans', 'biotrans',
                 'countries', 'subnational', 'city']

        spatial = []
        for key in order:
            element = value['geoElements'].get(key)
            if element:
                renderer = getattr(self, "_render_geochar_" + key)
                values = renderer(element).split(':')
                values[1] = values[1].split(',')
                values[1] = [x.strip() for x in values[1]]
                spatial += values[1]

                setattr(resource, '%s_%s' % ("eea", values[0]),
                        values[1])
        setattr(resource, "dcterms_spatial", spatial)

    def _render_geochar_element(self, value):
        value = BIOREGIONS[value]
        return u"region:{0}".format(value)

    def _render_geochar_macrotrans(self, value):
        tpl = u"macro-transnational-region:{0}"
        return tpl.format(u", ".join([BIOREGIONS[x] for x in value]))

    def _render_geochar_biotrans(self, value):
        tpl = u"biographical-regions:{0}"
        return tpl.format(u", ".join([BIOREGIONS.get(x, x) for x in value]))

    def _render_geochar_countries(self, value):
        tpl = u"countries:{0}"
        value = [ace_countries_dict.get(x, x) for x in value]
        return tpl.format(u", ".join(value))

    def _render_geochar_subnational(self, value):
        tpl = u"sub-nationals:{0}"

        out = []
        for line in value:
            line = line.encode('utf-8')
            if line in SUBNATIONAL_REGIONS:
                out.append(SUBNATIONAL_REGIONS[line])
                continue
            else:
                logger.error("Subnational region not found: %s", line)

        text = u", ".join([x.decode('utf-8') for x in out])
        return tpl.format(text)

    def _render_geochar_city(self, value):
        text = value
        if isinstance(value, (list, tuple)):
            text = u", ".join(value)
        return u"city:{0}".format(text)


class CityProfile2Surf(Dexterity2Surf):
    adapts(ICityProfile, ISurfSession)

    @property
    def prefix(self):
        """ Prefix """
        if self.portalType.lower() == 'eeaclimateadaptcity_profile':
            return 'eeaclimateadaptcityprofile'
        return self.portalType.lower()


class Geolocation2Surf(Value2Surf):
    """IValue2Surf implementation for plone.formwidget.Geolocation """
    adapts(IGeolocation)

    def __init__(self, value):
        self.value = value
        self.longitude = 'longitude: %s' % value.longitude
        self.latitude = 'latitude: %s' % value.latitude

    def __call__(self, *args, **kwds):
        return [self.longitude, self.latitude]


class File2Surf(Value2Surf):
    """IValue2Surf implementation for plone.namedfile.file.NamedBlobFile """
    adapts(INamedBlobFile)

    def __init__(self, value):
        self.value = value.filename


class Image2Surf(Value2Surf):
    """IValue2Surf implementation for plone.namedfile.file.NamedBlobImage """
    adapts(INamedBlobImage)

    def __init__(self, value):
        self.value = value.filename
