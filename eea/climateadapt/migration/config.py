IGNORED_CONTENT_TYPES = [
    # TODO:
    # 'Document',
    'Event',
    'News Item',
    'cca-event',

    'eea.climateadapt.aceproject',
    'eea.climateadapt.adaptationoption',
    'eea.climateadapt.c3sindicator',
    'eea.climateadapt.casestudy',
    'eea.climateadapt.city_profile',
    'eea.climateadapt.guidancedocument',
    'eea.climateadapt.indicator',
    'eea.climateadapt.informationportal',
    'eea.climateadapt.mapgraphdataset',
    'eea.climateadapt.organisation',
    'eea.climateadapt.publicationreport',
    'eea.climateadapt.researchproject',
    'eea.climateadapt.tool',
    'eea.climateadapt.video',

    'Image', 'LRF', 'LIF', 'Collection', 'Link', 'DepictionTool', 'Subsite',
    'File',
    'eea.climateadapt.city_profile',
    'FrontpageSlide',
    'EasyForm'

]

LANGUAGES = ['de', 'fr', 'es', 'it', 'pl', 'en']


IGNORED_PATHS = [
    'cca/{lang}/mission',
    'cca/{lang}/metadata'
    'cca/frontpage',
    'cca/{lang}/frontpage',
    'cca/{lang}/observatory/news-archive-observatory',
]

COL_MAPPING = {
    2: 'oneThird',
    3: 'oneThird',
    4: 'oneThird',
    5: 'oneThird',
    6: 'halfWidth',
    7: 'twoThirds',
    8: 'twoThirds',
    9: 'twoThirds',
    10: 'twoThirds',
    12: 'full',
}

TOP_LEVEL = {
    '/cca/en/about': [],
    '/cca/en/eu-adaptation-policy': [],
    '/cca/en/countries-regions': [],
    '/cca/en/knowledge': [],
    '/cca/en/network': [],
}
