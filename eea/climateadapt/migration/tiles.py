import logging
from collections import namedtuple
from uuid import uuid4

from bs4 import BeautifulSoup
from eea.climateadapt.config import DEFAULT_LOCATIONS
from eea.climateadapt.translation.utils import get_current_language
from eea.climateadapt.vocabulary import BIOREGIONS
from plone import api
from plone.api import content
from plone.app.uuid.utils import uuidToObject
from plone.namedfile.file import NamedBlobImage
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import sortable_title
from zope.component.hooks import getSite

from .utils import convert_to_blocks, make_uid, path

logger = logging.getLogger("eea.climateadapt")


def assigned(tile):
    """Return the list of objects stored in the tile as UUID. If an UUID
    has no object associated with it, removes the UUID from the list.
    :returns: a list of objects.
    """
    # self.set_limit()

    # always get the latest data
    data = tile.get()
    uuids = data.get('uuids')

    results = list()

    if uuids:
        ordered_uuids = [(k, v) for k, v in uuids.items()]
        ordered_uuids.sort(key=lambda x: x[1]["order"])

        for uuid in [i[0] for i in ordered_uuids]:
            obj = uuidToObject(uuid)

            if obj:
                results.append(obj)

            else:
                # maybe the user has no permission to access the object
                # so we try to get it bypassing the restrictions
                catalog = api.portal.get_tool("portal_catalog")
                # brain = catalog.unrestrictedSearchResults(UID=uuid, review_state='published')
                brain = catalog.searchResults(UID=uuid, review_state='published')

                if not brain:
                    # the object was deleted; remove it from the tile
                    obj.remove_item(uuid)
                    logger.warning(
                        "Nonexistent object {0} removed from " "tile".format(uuid)
                    )
    return results


Item = namedtuple(
    "Item", [
        "id",
        "portal_type",
        "getId",
        "UID",
        "Title",
        "title",
        "Description",
        "meta_type",
        "created",
        "effective",
        "modified",
        "review_state",
        "sortable_title",
    ]
)


def relevant_items(obj, request, tile):
    site = getSite()
    data = tile.get()
    results = []
    items = []

    for item in assigned(tile):
        wftool = getToolByName(item, "portal_workflow")
        state = wftool.getInfoFor(item, "review_state")
        obj_path = item.getPhysicalPath()
        site_path = site.getPhysicalPath()
        path = '/' + '/'.join(obj_path[len(site_path):])

        if not item:
            continue

        adapter = sortable_title(item)
        st = adapter()
        o = Item(
            path,
            item.portal_type,
            item.getId(),
            item.UID(),
            item.Title(),
            item.Title(),
            item.Description(),
            item.meta_type,
            item.created(),
            item.effective(),
            item.modified(),
            state,
            st,
        )
        items.append(o)

    combine = data.get("combine_results", False)

    if not combine:
        if items:
            if data.get("sortBy", "") == "NAME":
                items = sorted(items, key=lambda o: o.sortable_title)

    for item in items:
        o = {
            '@id': str(uuid4()),
            'item_title': item.Title,
            'link': path,
            'source': [{
                "@id": path,
                "@type": item.portal_type,
                "getId": item.getId,
                "UID": item.UID,
                "Title": item.Title,
                "title": item.Title,
                "meta_type": item.meta_type,
                "Description": item.Description,
                "created": item.created,
                "effective": item.effective,
                "modified": item.modified,
                "review_state": item.review_state,
            }]
        }

        results.append(o)

    return results


def cards_tile_to_block(tile_dm, obj, request):
    # data = tile_dm.get()

    if tile_dm.tile.is_empty():
        return {"blocks": []}

    collection = tile_dm.tile.get_context()
    query = collection.query

    query.append({
        "i": "path",
        "o": "plone.app.querystring.operation.string.absolutePath",
        "v": "/cca/en/metadata/organisations"
    })

    block_id = make_uid()

    blocks = [[block_id, {
        "@type": "listing",
        "block": block_id,
        "headlineTag": "h2",
        "gridSize": "four",
        "query": [],
        "querystring": {
            "query": query,
        },
        "variation": "cardsGallery"
    }]]

    return {
        "blocks": blocks,
    }


def region_select_to_block(tile_dm, obj, request):
    countries = tile_dm.tile.countries()

    if countries:
        img_name = countries[1][0].replace('.jpg', '_bg.png').replace(' ', '').decode('utf-8')
        img_path = (
            "/cca/++theme++climateadaptv2/static/images/transnational/" + img_name).encode('utf-8')
        fs_file = obj.restrictedTraverse(img_path)
        fs_file.request = request
        bits = fs_file().read()
        parent = obj.aq_parent
        contentType = img_name.endswith('jpg') and 'image/jpeg' or 'image/png'
        images = parent.listFolderContents(contentFilter={"portal_type": "Image"})
        image = None

        imagefield = NamedBlobImage(
            # TODO: are all images jpegs?
            data=bits,
            contentType=contentType,
            filename=img_name,
        )

        if not images:
            image = content.create(
                type="Image",
                title=img_name,
                image=imagefield,
                container=parent,
            )
        else:
            image = images[0]

        return {
            "blocks": [
                [make_uid(), {
                    "@type": "image",
                    "url": path(image)
                }],
                [make_uid(), {
                    "@type": "transRegionSelect",
                    "title": '',
                }]
            ],
        }
    else:
        return {
            "blocks": [
                [make_uid(), {
                    "@type": "transRegionSelect",
                    "title": '',
                }]
            ],
        }


def share_info_tile_to_block(tile_dm, obj, request):
    data = tile_dm.get()
    current_lang = get_current_language(obj, request)

    def link_url():
        type_ = data.get('shareinfo_type')
        location, _t, factory = DEFAULT_LOCATIONS[type_]
        location = '/' + current_lang + '/' + location
        return "{0}/add?type={1}".format(location, factory)

    blocks = [[make_uid(), {
        "@type": "callToActionBlock",
        "href": link_url(),
        "styles": {
            "icon": "ri-share-line",
            "theme": "primary",
            "align": "left"
        },
        "text": "Share your information",  # TODO: translation
        "target": "_self",
    }]]

    return {
        "blocks": blocks,
    }


def richtext_tile_to_blocks(tile_dm, obj, request):
    attributes = {}
    data = tile_dm.get()
    title_level = data.get('title_level')
    title = data.get('title')

    if title_level == 'h1' and title:
        attributes['title'] = title

    blocks = []
    text = data.get('text')
    if text:
        html = text.raw     # TODO: should we use .output ?
        logger.debug("Converting--")
        logger.debug(html)
        logger.debug("--/Converting")
        blocks = convert_to_blocks(html)

    return {
        "blocks": blocks,
    }


def embed_tile_to_block(tile_dm, obj, request):
    data = tile_dm.get()
    embed = data.get("embed", None)

    if not embed:
        return None

    if '<video' in embed:
        soup = BeautifulSoup(embed, "html.parser")
        video = soup.find("video")
        url = video.attrs.get('src')
        preview_image = video.attrs.get('poster', None)
        video_description = soup.get_text().replace('\n', '')

        video_block = {
            # "@type": "video", -not working for cmshare.eea.europa.eu
            "@type": "nextCloudVideo",
            "url": url,
            "title": video_description,
        }

        if preview_image is not None:
            video_block['preview_image'] = preview_image

        return {
            "blocks": [[make_uid(), video_block]]
        }

    elif 'discomap' or 'maps.arcgis' in embed:
        soup = BeautifulSoup(embed, "html.parser")
        iframe = soup.find("iframe")
        url = iframe.attrs.get('src')

        maps_block = {
            "@type": "maps",
            "align": "full",
            "dataprotection": {},
            "height": "100vh",
            "url": url,
        }

        return {
            "blocks": [[make_uid(), maps_block]]
        }
    logger.error("Implement missing embed tile type.")
    return None


def search_acecontent_to_block(tile_dm, obj, request):
    data = tile_dm.get()

    blocks = [[make_uid(), {
        "@type": "searchAceContent",
        "title": data.get('title'),
        "search_text": data.get('search_text'),
        "origin_website": data.get('origin_website'),
        "search_type": data.get('search_type'),
        "element_type": data.get('element_type'),
        "sector": data.get('sector'),
        "special_tags": data.get('special_tags'),
        'countries': data.get('countries'),
        "macro_regions": data.get('macro_regions'),
        "bio_regions": data.get('bio_regions'),
        "funding_programme": data.get('funding_programme'),
        "nr_items": data.get('nr_items'),
    }]]

    return {
        "blocks": blocks,
    }


def relevant_acecontent_to_block(tile_dm, obj, request):
    data = tile_dm.get()

    blocks = [[make_uid(), {
        "@type": "relevantAceContent",
        "title": data.get('title'),
        "items": relevant_items(obj, request, tile_dm),
        "search_text": data.get('search_text'),
        "origin_website": data.get('origin_website'),
        "search_type": data.get('search_type'),
        "element_type": data.get('element_type'),
        "sector": data.get('sector'),
        "special_tags": data.get('special_tags'),
        'countries': data.get('countries'),
        "macro_regions": data.get('macro_regions'),
        "bio_regions": data.get('bio_regions'),
        "funding_programme": data.get('funding_programme'),
        "nr_items": data.get('nr_items'),
        "show_share_btn": data.get('show_share_btn'),
        "sortBy": data.get('sortBy'),
        "combine_results": data.get('combine_results'),
    }]]

    return {
        "blocks": blocks,
    }


def nop_view(obj, data):
    return {"blocks": []}


view_convertors = {
    'eu-sector-policies': nop_view,
    'countries-list': nop_view,
    'video-thumbs': nop_view,
    'countries-context-pagelet': nop_view,
    'c3s_indicators_overview': nop_view,
    'observatory_indicators_list': nop_view,
    'countries-heat-index': nop_view,
    'case-study-and-adaptation-options-map-viewer': nop_view,
    'forest-landing-page': nop_view,
    'urban-landing-page': nop_view,
    'view_last_modified': nop_view,
    'country-disclaimer': nop_view,
    'country-profile': nop_view,
    'regions-section': nop_view,
    'help-categories': nop_view,
    'regions-section': nop_view,
    'fp-countries-tile': nop_view,
    'fp-news-tile': nop_view,
    'fp-events-tile': nop_view,
}


def genericview_tile_to_block(tile_dm, obj, request):
    data = tile_dm.get()
    view_name = data.get('view_name')

    if not view_name:
        return {"blocks": []}

    converter = view_convertors.get(view_name)
    if converter is None:
        logger.warn("GenericView tile converter not implemented: %s", view_name)
        return {"blocks": []}

    return converter(obj, data)


def filter_acecontent_to_block(tile_dm, obj, request):
    data = tile_dm.get()
    macro_regions = data.get('macro_regions')
    sortBy = None
    trans_macro_regions = []
    sortingValues = {
        'effective': 'EFFECTIVE',
        'modified': 'MODIFIED',
        'getId': 'NAME'
    }
    otherRegions = {
        'Macaronesia',
        'Caribbean Area',
        'Amazonia',
        'Anatolian',
        'Indian Ocean Area'
    }
    if macro_regions is not None:
        regions = [i for i in macro_regions if i not in otherRegions]
    else:
        regions = []

    for region_name in regions:
        if 'Other Regions' == region_name:
            trans_macro_regions.append('Other Regions')
        for k, v in BIOREGIONS.items():
            if 'TRANS_MACRO' in k and v == region_name:
                trans_macro_regions.append(k)

    for k, v in sortingValues.items():
        if v == data.get('sortBy'):
            sortBy = k

    blocks = [[make_uid(), {
        "@type": "filterAceContent",
        "title": data.get('title'),
        "search_text": data.get('search_text'),
        "origin_website": data.get('origin_website'),
        "search_type": data.get('search_type'),
        "element_type": data.get('element_type'),
        "sector": data.get('sector'),
        "special_tags": data.get('special_tags'),
        'countries': data.get('countries'),
        "macro_regions": trans_macro_regions,
        "bio_regions": data.get('bio_regions'),
        "funding_programme": data.get('funding_programme'),
        "nr_items": data.get('nr_items'),
        "sortBy": sortBy,
    }]]

    return {
        "blocks": blocks,
    }
