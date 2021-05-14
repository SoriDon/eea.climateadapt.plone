import csv
import json
import logging
import lxml.etree
import lxml.html
import urllib2
from datetime import datetime
from pkg_resources import resource_filename
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from eea.climateadapt.vocabulary import ace_countries
from plone.api import portal
from plone.intelligenttext.transforms import \
    convertWebIntelligentPlainTextToHtml as convWebInt


def parse_csv(path):
    wf = resource_filename("eea.climateadapt", path)

    reader = csv.reader(open(wf))
    cols = reader.next()
    out = []

    for line in reader:
        out.append(dict(zip(cols, line)))

    return out


def get_country_code(country_name):
    country_code = next(
        (k for k, v in ace_countries if v == country_name), 'Not found'
    )

    return country_code


def setup_discodata(annotations):
    response = urllib2.urlopen(DISCODATA_URL)
    data = json.loads(response.read())
    annotations['discodata'] = {
        'timestamp': datetime.now(),
        'data': data
    }
    annotations._p_changed = True
    logger.info("RELOAD URL %s", DISCODATA_URL)

    return data


def get_discodata():
    annotations = portal.getSite().__annotations__

    if 'discodata' not in annotations:
        annotations._p_changed = True
        return setup_discodata(annotations)

    last_import_date = annotations['discodata']['timestamp']

    if (datetime.now() - last_import_date).total_seconds() > 60 * 2:
        annotations._p_changed = True
        return setup_discodata(annotations)

    return annotations['discodata']['data']


def get_discodata_for_country(country_code):
    data = get_discodata()

    orig_data = next((
        x
        for x in data['results']
        if x['countryCode'] == country_code
    ), {})

    # remove the countryCode as we don't need it
    processed_data = {
        k: unicode(v)
        for k, v in orig_data.items()
        if k != 'countryCode'
    }

    # some values are strings, and need to be transformed
    # into Python objects
    for k, val in processed_data.items():
        json_val = json.loads(val)
        new_value = json_val[k][0]

        processed_data[k] = new_value

    return processed_data


DISCODATA_URL = 'https://discodata.eea.europa.eu/sql?query=select%20*%20from%20%5BNCCAPS%5D.%5Blatest%5D.%5BAdaptation_JSON%5D&p=1&nrOfHits=100'

logger = logging.getLogger("eea.climateadapt")

_COUNTRIES_WITH_NAS = [
    "Austria",
    "Belgium",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
    "United Kingdom",
    "Liechtenstein",
    "Norway",
    "Switzerland",
    "Turkey",
]

_COUNTRIES_WITH_NAP = [
    "Austria",
    "Belgium",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Ireland",
    "Lithuania",
    "Netherlands",
    "Romania",
    "Spain",
    "United Kingdom",
    "Switzerland",
    "Turkey",
]

_MARKERS = [
    ("national adaption policy", "National adaption policy"),
    ("national adaptation strategy", "National adaptation strategy (NAS)"),
    ("national adaptation plan", "National adaptation plan (NAP)"),
    # ('action plans', 'National adaptation plans (NAP)'),
    # ('action plans', 'Action plans'),
    # ('impacts', 'Impacts, vulnerability and adaptation assessments'),
    # ('climate services', 'Climate services / Met office'),
    # TODO: this is not found in the information extracted in DB
    # this needs to be fixed in content
    # ('adaptation platform', 'Adaptation platform'),
    #
    # ('web portal', 'Web portal'),
    # ('national communication', 'National Communication to the UNFCCC'),
    # ('monitoring', 'Monitoring, Indicators, Methodologies'),
    # ('research program', 'Research programs')
    # ('training', 'Training and education resources')
]


def normalized(key):
    """Returns NAP/NAS label if they key is NAP or NAS"""
    # We depend on human entered labels in the first column
    # We need to "normalize" it, because sometimes the case is wrong or some
    # parts of the text are missing (for example the NAS/NAP bit)

    for marker, label in _MARKERS:
        if marker in key.lower():
            return label


def get_nap_nas(obj, text, country):
    res = {}

    for name in ["nap", "nas"]:
        if obj.hasProperty(name):
            res[name] = obj.getProperty(name)

    # return res

    e = lxml.html.fromstring(text)
    rows = e.xpath('//table[contains(@class, "listing")]/tbody/tr')

    for row in rows:
        try:
            cells = row.xpath("td")
            # key = cells[0].text_content().strip()
            # key = ''.join(cells[0].itertext()).strip()
            key = " ".join([c for c in cells[0].itertext() if type(c) is not unicode])

            if key in [None, ""]:
                key = cells[0].text_content().strip()

            if len(list(cells)) < 3:
                children = []
            else:
                children = list(cells[2])

            text = [lxml.etree.tostring(c) for c in children]
            value = u"\n".join(text)
            key = normalized(key)

            if key is None:
                continue

            # If there's no text in the last column, write "Established".

            is_nap_country = country in _COUNTRIES_WITH_NAP
            is_nas_country = country in _COUNTRIES_WITH_NAS

            if (not value) and (is_nap_country or is_nas_country):
                value = u"<p>Established</p>"

            if "NAP" in key:
                prop = "nap_info"
            else:
                prop = "nas_info"

            # We're using a manually added property to set the availability of
            # NAP or NAS on a country. To use it, add two boolean properties:
            # nap and nas on the country folder. For example here:
            # /countries-regions/countries/ireland/manage_addProperty
            # is_nap_nas = obj.getProperty(prop, False)

            res[prop] = value

        except Exception:
            logger.exception("Error in extracting information from country %s", country)

    return res


class CountriesMetadataExtract(BrowserView):
    """Extract metadata from all country profiles, exports as json"""

    def extract_country_metadata_from_discodata(self, obj):
        res = {}

        for name in ["nap", "nas"]:
            if obj.hasProperty(name):
                res[name] = obj.getProperty(name)

        country_name = obj.Title()
        country_code = get_country_code(country_name)

        processed_data = get_discodata_for_country(country_code)

        if not processed_data:
            return res

        for name in ('NAS', 'NAP'):
            values = processed_data['Legal_Policies'].get(name, [])
            is_nap_country = country_name in _COUNTRIES_WITH_NAP
            is_nas_country = country_name in _COUNTRIES_WITH_NAS

            # if (not values) and (is_nap_country or is_nas_country):
            #     value = u"<p>Established</p>"

            value = [
                u"<li><a href='{}'>{}</a></li>".format(
                    v.get('Link'), v.get('Title'))
                for v in values
            ]
            value = u"<ul>{}</ul>".format(''.join(value))

            if "NAP" in name:
                prop = "nap_info"
            else:
                prop = "nas_info"

            res[prop] = value

        return res

    def extract_country_metadata(self, obj):
        """ replaced by method 'extract_country_metadata_from_discodata' """

        # if 'ireland' in obj.absolute_url().lower():
        #     import pdb
        #     pdb.set_trace()

        if "index_html" in obj.contentIds():
            cover = obj["index_html"]
        else:
            cover = obj

        layout = cover.cover_layout
        layout = json.loads(layout)

        try:
            main_tile = layout[0]["children"][1]["children"][1]
        except:
            main_tile = layout[0]["children"][0]["children"][2]

        assert main_tile["tile-type"] == "collective.cover.richtext"

        uid = main_tile["id"]
        tile_data = cover.__annotations__["plone.tiles.data." + uid]
        text = tile_data["text"].raw

        res = get_nap_nas(obj, text, country=obj.Title())

        return res

    def __call__(self):
        res = {}

        for child in self.context.contentValues():
            if child.portal_type not in ["Folder", "collective.cover.content"]:
                continue

            res[child.Title()] = [
                self.extract_country_metadata_from_discodata(child),
                child.absolute_url(),
            ]

        self.request.response.setHeader("Content-type", "application/json")

        return json.dumps([res, [x[1] for x in _MARKERS]])


class CountryMetadataExtract(object):
    """This is a demo view, shows metadata extracted from country

    It's not used in real code, it's mainly for debugging
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        cover = self.context["index_html"]

        layout = cover.cover_layout
        layout = json.loads(layout)

        try:
            main_tile = layout[0]["children"][1]["children"][1]
        except:
            main_tile = layout[0]["children"][0]["children"][2]

        assert main_tile["tile-type"] == "collective.cover.richtext"

        uid = main_tile["id"]
        tile_data = cover.__annotations__["plone.tiles.data." + uid]
        text = tile_data["text"].raw

        e = lxml.etree.fromstring(text)
        rows = e.xpath("//table/tbody/tr")

        res = {}

        for row in rows:
            cells = row.xpath("td")
            # key = cells[0].text.strip()
            key = "".join(cells[0].itertext()).strip()
            children = list(cells[2])
            text = [lxml.etree.tostring(c) for c in children]
            value = u"\n".join(text)
            res[key] = value

        self.request.response.setHeader("Content-type", "application/json")

        return json.dumps([res])


class CountriesD3View(BrowserView):
    """"""


class ContextCountriesView(BrowserView):
    """A small pagelet to show the countries as a tile"""

    available_countries = [
        "Austria",
        "Belgium",
        "Bulgaria",
        "Croatia",
        "Iceland",
        "Latvia",
        "Cyprus",
        "Czechia",
        "Denmark",
        "Estonia",
        "Finland",
        "France",
        "Germany",
        "Greece",
        "Hungary",
        "Ireland",
        "Italy",
        "Lithuania",
        "Luxembourg",
        "Malta",
        "Netherlands",
        "Poland",
        "Portugal",
        "Romania",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
        "United Kingdom",
        "Liechtenstein",
        "Norway",
        "Switzerland",
        "Turkey",
    ]

    def countries(self):
        objects = self.context.aq_parent.contentValues()

        return sorted(
            [x for x in objects if x.Title() in self.available_countries],
            key=lambda x: x.Title(),
        )

    def script_country_settings(self):
        context_titles = [x.Title() for x in self.context.aq_parent.contentValues()]
        available_countries = [
            x for x in self.available_countries if x in context_titles
        ]

        return """window.countrySettings = %s;""" % json.dumps(available_countries)

    def csv_data_js(self):
        # used for heat_index map
        info = parse_csv("data/heat_index.csv")
        m = {}

        for line in info:
            if line["country_id"].strip():
                m[line["country_id"]] = line

        s = """var heat_index_info = {0};console.log(heat_index_info);""".format(
            json.dumps(m)
        )

        return s


class CountryProfileData(BrowserView):
    template = ViewPageTemplateFile("pt/country-profile.pt")

    def convert_web_int(self, text):
        return convWebInt(text)

    def get_sorted_affected_sectors_data(self):
        items = self.processed_data['National_Circumstances'].get(
            'Afected_Sectors', [])

        sorted_items = sorted(
            items,
            key=lambda i: (i['SectorTitle'], i['SectorDescribeIfOther'])
        )

        return sorted_items

    def get_sorted_action_measures_data(self):
        items = self.processed_data['Strategies_Plans'].get(
            'Action_Measures', [])

        sorted_items = sorted(
            items,
            key=lambda i: (i['KeyTypeMeasure'], i['subKTM'], i['Title'])
        )

        return sorted_items

    def get_sorted_available_practices_data(self):
        items = self.processed_data['Cooperation_Experience'].get(
            'Available_Good_Practices', [])

        sorted_items = sorted(
            items,
            key=lambda i: i['Area']
        )

        return sorted_items

    def __call__(self):
        country_name = self.context.title
        country_code = get_country_code(country_name)

        processed_data = get_discodata_for_country(country_code)
        # [u'AT', u'BE', u'BG', u'CZ', u'DE', u'DK', u'EE', u'ES', u'FI',
        # u'GR', u'HR', u'HU', u'IE', u'IT', u'LT', u'LU', u'LV', u'MT',
        # u'NL', u'PL', u'PT', u'RO', u'SE', u'SI', u'SK', u'TR']

        self.processed_data = processed_data

        return self.template(country_data=processed_data)


class CountryProfileDataRaw(CountryProfileData):
    template = ViewPageTemplateFile("pt/country-profile-raw.pt")
