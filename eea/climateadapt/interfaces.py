from zope.interface import Interface


class IClimateAdaptContent(Interface):
    """ Marker interface for climate adapt content
    """


class IEEAClimateAdaptInstalled(Interface):
    """ Browser layer marker interface
    """


class IBalticRegionMarker(Interface):
    """ A marker interface for Baltic Region pages. They get a special nav menu
    """


class ITransnationalRegionMarker(Interface):
    """ A marker interface for transnational region pages.
    """


class IASTNavigationRoot(Interface):
    """ A marker interface for AST tools
    """


class ISiteSearchFacetedView(Interface):
    """ A marker interface for the /data-and-downloads page
    """


class IClimateAdaptSharePage(Interface):
    """ A marker interface for the /share-your-info/ pages
    """


class IUrbanASTPage(Interface):
    """ A marker interface for Urban AST pages
    """


class ICountriesRoot(Interface):
    """ A marker interface for /countries page
    """


class IMayorAdaptRoot(Interface):
    """ A marker interface for /mayors-adapt
    """


class ICitiesListingsRoot(Interface):
    """ A marker interface for /city-profile
    """


class IContentRoot(Interface):
    """ A marker interface for /content
    """


class ITransRegioRoot(Interface):
    """ A marker interface for /transnations-regions
    """
