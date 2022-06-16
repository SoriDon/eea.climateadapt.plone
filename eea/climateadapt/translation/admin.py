""" Admin translation
"""
import json
import logging
import os
import time
from collections import defaultdict
from datetime import date, datetime
from DateTime import DateTime
import transaction

from collective.cover.tiles.richtext import RichTextTile
from plone import api
from plone.api import content, portal
from plone.api.content import get_state
from plone.app.layout.viewlets import ViewletBase
from plone.app.multilingual.factory import DefaultTranslationFactory
from plone.app.multilingual.manager import TranslationManager
from plone.api.portal import get_tool
from plone.app.textfield.value import RichTextValue
from plone.behavior.interfaces import IBehaviorAssignable
from plone.formwidget.geolocation.geolocation import Geolocation
from plone.namedfile.file import NamedBlobImage, NamedBlobFile
from plone.namedfile.file import NamedFile, NamedImage
from plone.tiles.interfaces import ITileDataManager
from z3c.relationfield.relation import RelationValue
from Products.Five.browser import BrowserView

from eea.climateadapt.browser.admin import force_unlock
from eea.climateadapt.tiles.richtext import RichTextWithTitle
from eea.climateadapt.translation import retrieve_translation
from eea.climateadapt.translation import retrieve_html_translation
from eea.climateadapt.translation import get_translated

from zope.schema import getFieldsInOrder
from zope.site.hooks import getSite

logger = logging.getLogger('eea.climateadapt')


def is_json(input):
    try:
        json.loads(input)
    except ValueError as e:
        return False
    return True


def translate_obj(obj, lang=None, version=None):
    tile_fields = ['title', 'description', 'tile_title', 'footer', 'alt_text']
    errors = []
    force_unlock(obj)

    site_url = portal.getSite().absolute_url()
    obj_url = obj.absolute_url()
    obj_path = '/cca' + obj_url.split(site_url)[-1]

    # get behavior fields and values
    behavior_assignable = IBehaviorAssignable(obj)
    fields = {}
    if behavior_assignable:
        behaviors = behavior_assignable.enumerateBehaviors()
        for behavior in behaviors:
            for k, v in getFieldsInOrder(behavior.interface):
                fields.update({k: v})

    #  get schema fields and values
    for k, v in getFieldsInOrder(obj.getTypeInfo().lookupSchema()):
        fields.update({k: v})

    translations = TranslationManager(obj).get_translations()
    obj_en = translations.pop('en')
    layout_en = obj_en.getLayout()
    default_view_en = obj_en.getDefaultPage()
    if default_view_en is not None:
        layout_default_view_en = obj_en[default_view_en].getLayout()

    for language in translations:
        if lang is not None:
            if language != lang:
                continue

        trans_obj = translations[language]
        trans_obj_url = trans_obj.absolute_url()
        trans_obj_path = '/cca' + trans_obj_url.split(site_url)[-1]

        if version is not None:
            obj_version = int(getattr(trans_obj, 'version', 0))

            if obj_version >= version:
                logger.info(
                    "Skipping! object already at version %s", obj_version)
                continue

            trans_obj.version = version

        # set the layout of the translated object to match the english object
        trans_obj.setLayout(layout_en)

        # also set the layout of the default view
        if default_view_en:
            trans_obj[default_view_en].setLayout(layout_default_view_en)

        # get tile data
        if trans_obj.portal_type == 'collective.cover.content':
            tiles_id = trans_obj.list_tiles()

            for tile_id in tiles_id:
                tile = trans_obj.get_tile(tile_id)
                for field in tile_fields:
                    value = tile.data.get(field)
                    if value:
                        translated = retrieve_translation(
                                'EN', value, [language.upper()])

                        if 'translated' in translated:
                            encoded_text = translated['transId'].encode(
                                    'latin-1')
                            tile.data.update({field: encoded_text})

                if isinstance(tile, RichTextWithTitle) or \
                   isinstance(tile, RichTextTile):
                    try:
                        value = tile.data.get('text').raw
                    except Exception:
                        value = None
                    if value:
                        html_content = u"<!doctype html>" + \
                            u"<head><meta charset=utf-8></head><body>"

                        value = value.replace('\r\n', '')
                        try:
                            test_value = value + u"test"
                        except UnicodeDecodeError:
                            value = value.decode("utf-8")
                        html_tile = u"<div class='cca-translation-tile'" + \
                            u" data-field='" + field + u"'" + \
                            u" data-tile-id='" + tile_id + u"'" + \
                            u">" + value + u"</div>"

                        html_content += html_tile

                        html_content += u"</body></html>"
                        html_content = html_content.encode('utf-8')
                        translated = retrieve_html_translation(
                            'EN',
                            html_content,
                            trans_obj_path,
                            language.upper(),
                            False,
                        )

                        if 'translated' in translated:
                            try:
                                encoded_text = translated['transId'].encode(
                                        'latin-1')
                                tile.data['text'].raw = encoded_text
                            except AttributeError:
                                logger.info("Error for tile. TODO improve.")
                                logger.info(tile_id)

        # send requests to translation service for each field
        # update field in obj
        rich_fields = []

        for key in fields:
            rich = False
            # print(key)
            if key in ['acronym', 'id', 'language', 'portal_type',
                       'contentType']:
                continue

            value = getattr(getattr(obj, key), 'raw', getattr(obj, key))

            if trans_obj.portal_type in ['Event', 'cca-event']:
                force_unlock(trans_obj)
                reindex = False
                if key == 'start':
                    # setattr(trans_obj, key, obj.start)
                    trans_obj.start = obj.start
                    reindex = True
                if key == 'end':
                    trans_obj.end = obj.end
                    # setattr(trans_obj, key, obj.start)
                    reindex = True
                if key == 'effective':
                    trans_obj.setEffectiveDate(obj.effective_date)
                    reindex = True
                if key == 'timezone':
                    trans_obj.timezone = obj.timezone
                    reindex = True

                if reindex is True:
                    # reindex object
                    trans_obj._p_changed = True
                    trans_obj.reindexObject()
                    continue

                    # transaction.commit()

            if not value:
                continue

            if callable(value):
                # ignore datetimes
                if isinstance(value(), DateTime):
                    continue

                value = value()

            # ignore some value types
            if isinstance(value, bool) or \
               isinstance(value, int) or \
               isinstance(value, long) or \
               isinstance(value, tuple) or \
               isinstance(value, list) or \
               isinstance(value, set) or \
               isinstance(value, dict) or \
               isinstance(value, NamedBlobImage) or \
               isinstance(value, NamedBlobFile) or \
               isinstance(value, NamedImage) or \
               isinstance(value, NamedFile) or \
               isinstance(value, DateTime) or \
               isinstance(value, date) or \
               isinstance(value, RelationValue) or \
               isinstance(value, Geolocation):
                continue

            if isinstance(getattr(obj, key), RichTextValue):
                value = getattr(obj, key).raw.replace('\r\n', '')
                rich = True
                if key not in rich_fields:
                    rich_fields.append(key)

            if is_json(value):
                continue

            if key not in errors:
                errors.append(key)
            force_unlock(trans_obj)
            translated = retrieve_translation('EN', value, [language.upper()])
            if 'translated' in translated:
                # TODO improve this part, after no more errors
                encoded_text = translated['transId'].encode('latin-1')

                source_richtext_types = [
                    'eea.climateadapt.publicationreport',
                    'eea.climateadapt.researchproject',
                    'eea.climateadapt.mapgraphdataset',
                    'eea.climateadapt.video',
                    ]

                if key == 'source' and \
                        obj.portal_type in source_richtext_types:
                    # import pdb; pdb.set_trace()
                    setattr(trans_obj, key, getattr(obj, key))
                    # setattr(trans_obj, key, encoded_text)
                    # setattr(trans_obj, key, translated['transId'])

                    setattr(trans_obj, key, RichTextValue(encoded_text))
                    # ValueError: Can not convert 'Elsevier' to an IRichTextValue
                    # <ResearchProject at /cca/ro/help/share-your-info/research-and-knowledge-projects
                    # /elderly-resident2019s-uses-of-and-preferences-for-urban-green-spaces-during-hea
                    # t-periods>

                    # reindex object
                    trans_obj._p_changed = True
                    trans_obj.reindexObject(idxs=[key])
                    continue

                if rich:
                    pass
                    # TODO No action needed, right?
                    # setattr(trans_obj, key, getattr(obj, key))
                    # setattr(trans_obj, key, RichTextValue(encoded_text))
                    # setattr(getattr(trans_obj, key), 'raw', encoded_text)
                else:
                    if isinstance(value, str) and key in ['funding_programme']:
                        setattr(trans_obj, key, translated['transId'])
                    else:
                        setattr(trans_obj, key, encoded_text)

                # reindex object
                trans_obj._p_changed = True
                trans_obj.reindexObject(idxs=[key])

        if len(rich_fields) > 0:
            html_content = u"<!doctype html><head><meta charset=utf-8></head>"
            html_content += u"<body>"

            for key in rich_fields:
                value = getattr(obj, key).raw.replace('\r\n', '')
                html_section = u"<div class='cca-translation-section'" + \
                    u" data-field='" + key + u"'>" + value + u"</div>"

                html_content += html_section

            html_content += u"</body></html>"
            html_content = html_content.encode('utf-8')
            res = retrieve_html_translation(
                'EN',
                html_content,
                trans_obj_path,
                language.upper(),
                False,
            )

    return {'errors': errors}


def initiate_translations(site, skip=0, version=None, language=None):
    skip = int(skip)
    if language is None:
        return "Missing language parameter. (Example: ?language=it)"
    if version is None:
        return "Missing translation version. Status: /admin-translation-status"
    version = int(version)
    catalog = site.portal_catalog
    count = -1
    res = catalog.searchResults(path='/cca/en')
    errors = []
    debug_skip = False
    debug_skip_number = skip  # do not translate first objects

    if skip > 0:
        debug_skip = True
    total_objs = len(res)

    translate_only = False
    only = []  # Example: ['Event', 'cca-event']
    if len(only) > 0:
        translate_only = True  # translate only the specified content types

    for brain in res:
        count += 1

        if debug_skip is True and count < debug_skip_number:
            continue

        if translate_only is True and brain.portal_type not in only:
            continue

        logger.info("--------------------------------------------------------")
        logger.info(count)
        logger.info(total_objs)
        logger.info("--------------------------------------------------------")

        if brain.getPath() == '/cca/en' or brain.portal_type in ['LIF', 'LRF']:
            continue

        obj = brain.getObject()

        try:
            result = translate_obj(obj, language, version)
        except Exception as err:
            result = {'errors': [err]}
            logger.info(err)
            # errors.append(err)
            import pdb; pdb.set_trace()

        t_errors = result.get('errors', []) if result is not None else []
        if len(t_errors) > 0:
            for error in t_errors:
                if error not in errors:
                    errors.append(error)

        if count % 20 == 0:
            logger.info("Processed %s objects" % count)
            transaction.commit()

    logger.info("DONE")
    logger.info(errors)
    transaction.commit()

def translations_status(site, language=None):
    if language is None:
        return "Missing language."

    path = '/cca/' + language
    catalog = site.portal_catalog
    brains = catalog.searchResults(path=path)

    versions = defaultdict(int)
    template = "<p>{} at version {}</p>"
    logger.info("Translations status:")

    for brain in brains:
        obj = brain.getObject()
        obj_version = int(getattr(obj, 'version', 0))
        versions[obj_version] += 1

    res = []
    for k, v in versions.items():
        res.append(template.format(v, k))

    logger.info(res)
    return "".join(res)


def verify_cloned_language(site, language=None):
    """ Get all objects in english and check if all of them are cloned for
        given language. Also make sure all paths are similar.
        Correct:
            /cca/en/obj-path
            /cca/ro/obj-path
        Wrong:
            /cca/en/obj-path
            /cca/ro/obj-path-ro-ro-ro
    """
    if language is None:
        return "Missing language parameter. (Example: ?language=it)"
    catalog = site.portal_catalog
    brains = catalog.searchResults(path='/cca/en')
    site_url = portal.getSite().absolute_url()
    logger.info("I will list the missing objects if any. Checking...")

    res = []
    found = 0  # translation found with correct path
    found_changed = 0  # translation found but with different path
    not_found = 0  # translation not found
    for brain in brains:
        obj = brain.getObject()
        obj_url = obj.absolute_url()
        obj_path = '/cca' + obj_url.split(site_url)[-1]
        prefix = '/cca/' + language.lower() + '/'
        trans_obj_path = obj_path.replace('/cca/en/', prefix)
        try:
            trans_obj = site.unrestrictedTraverse(trans_obj_path)
            found += 1
        except Exception:
            res.append(trans_obj_path)
            translations = TranslationManager(obj).get_translations()
            if language in translations:
                trans_obj = translations[language]
                new_url = trans_obj.absolute_url()
                res.append("Found as: " + new_url)
                found_changed += 1
                logger.info(trans_obj_path)
                logger.info("Found as %s", new_url)
            else:
                not_found += 1
                res.append("Not found.")
                logger.info("Not found: %s", trans_obj_path)

    logger.info("Found: %s. Found with different path: %s. Not found: %s.",
                found, found_changed, not_found)

    return "\n".join(res)

def verify_translation_fields(site, language=None):
    """ Get all objects in english and check if all of them are cloned for
        given language and with fields filled.
    """
    if language is None:
        return "Missing language parameter. (Example: ?language=it)"
    catalog = site.portal_catalog
    brains = catalog.searchResults(path='/cca/en')
    site_url = portal.getSite().absolute_url()
    logger.info("I will list the missing translation fields. Checking...")

    res = []
    total_items = 0  # total translatable eng objects
    found = 0  # found end objects
    found_missing = 0  # missing at least one attribute
    not_found = 0  # eng obj not found
    missing_values = 0  # count the missing field values

    report = {}
    skip_items = ['.jpg','.pdf','.png']
    skip_fields = ["sync_uid", "allow_discussion"]

    for brain in brains:
        obj = brain.getObject()
        if is_obj_skipped_for_translation(obj):
            continue

        obj_url = obj.absolute_url()

        if obj.portal_type not in report:
            report[obj.portal_type] = {}

        #if '.jpg' in obj_url:
        if any(skip_item in obj_url for skip_item in skip_items):
            continue
        total_items += 1
        obj_path = '/cca' + obj_url.split(site_url)[-1]
        # logger.info("Will check: %s", obj_path)
        translations = TranslationManager(obj).get_translations()
        if language not in translations:
            #add message regarding no translation found
            logger.info("Not found: %s", obj_path)
            not_found += 1
            continue
        trans_obj = translations[language]

        # get behavior fields and values
        behavior_assignable = IBehaviorAssignable(obj)
        fields = {}
        if behavior_assignable:
            behaviors = behavior_assignable.enumerateBehaviors()
            for behavior in behaviors:
                for k, v in getFieldsInOrder(behavior.interface):
                    fields.update({k: v})
        for k, v in getFieldsInOrder(obj.getTypeInfo().lookupSchema()):
            fields.update({k: v})

        fields_missing = []
        for field in fields.keys():
            if field in skip_fields:
                continue
            #TODO: check if we need to log if this is FALSE
            if not hasattr(obj, field):
                continue
            if not hasattr(trans_obj, field):
                fields_missing.append(field)
                continue
            #if bool(getattr(obj, field)) and not bool(getattr(trans_obj,field)):
            #        fields_missing.append(field)
            missing = object()
            if not getattr(obj,field,missing) in (missing, None) and getattr(trans_obj,field,missing) in (missing, None):
                fields_missing.append(field)
                missing_values += 1

                if field not in report[obj.portal_type]:
                    report[obj.portal_type][field] = 0

                prev_value = report[obj.portal_type][field]
                report[obj.portal_type][field] = prev_value + 1

        if len(fields_missing):
            logger.info("FIELDS NOT SET: %s %s", trans_obj.absolute_url(), fields_missing)
            found_missing += 1

        #import pdb; pdb.set_trace()
        logger.info("URL: %s", trans_obj.absolute_url())
        found += 1

    logger.info("TotalItems: %s, Found with correct data: %s. Found with mising data: %s. Not found: %s. Missing values: %s",
                total_items, found, found_missing, not_found, missing_values)

    json_object = json.dumps(report, indent=4)
    with open("/tmp/translation_report.json", "w") as outfile:
        outfile.write(json_object)

    return "\n".join(res)

def get_object_fields(obj):
    behavior_assignable = IBehaviorAssignable(obj)
    fields = {}
    if behavior_assignable:
        behaviors = behavior_assignable.enumerateBehaviors()
        for behavior in behaviors:
            for k, v in getFieldsInOrder(behavior.interface):
                fields.update({k: v})
    for k, v in getFieldsInOrder(obj.getTypeInfo().lookupSchema()):
        fields.update({k: v})
    return fields

def get_object_fields_values(obj):
    #TODO: perhaps a list by each portal_type
    skip_fields = ['c3s_identifier', 'contact_email', 'contact_name', 'details_app_toolbox_url', 'duration', 'event_url', 'funding_programme', 'method', 'other_contributor',
        'organisational_contact_information', 'organisational_websites', 'overview_app_toolbox_url', 'partners_source_link', 'remoteUrl', 'storage_type', 'sync_uid','timezone']
    tile_fields = ['title', 'text', 'description', 'tile_title', 'footer', 'alt_text']

    data = {}
    data['portal_type'] = obj.portal_type
    data['path'] = obj.absolute_url()
    data['item'] = {}
    data['html'] = {}
    data['tile'] = {}
    # get tile data
    #import pdb; pdb.set_trace()
    if obj.portal_type == 'collective.cover.content':
        tiles_id = obj.list_tiles()
        for tile_id in tiles_id:
            data['tile'][tile_id] = {'item':{},'html':{}}
            tile = obj.get_tile(tile_id)
            for field in tile_fields:
                value = None
                if isinstance(tile, RichTextWithTitle) or \
                   isinstance(tile, RichTextTile):
                    if field in tile_fields:
                        try:
                            if isinstance(tile.data.get(field), RichTextValue):
                                value = tile.data.get(field).raw
                                if value:
                                    data['tile'][tile_id]['html'][field] = value
                            else:
                                value = tile.data.get(field)
                                if value:
                                    data['tile'][tile_id]['item'][field] = value
                        except Exception:
                            value = None
                else:
                    value = tile.data.get(field, None)
                    if value:
                        data['tile'][tile_id]['item'][field] = value
    else:
        fields = get_object_fields(obj)
        for key in fields:
            rich = False
            # print(key)
            if key in ['acronym', 'id', 'language', 'portal_type',
                       'contentType']:
                continue
            if key in skip_fields:
                continue

            value = getattr(getattr(obj, key), 'raw', getattr(obj, key))

            if not value:
                continue

            if callable(value):
                # ignore datetimes
                if isinstance(value(), DateTime):
                    continue

                value = value()

            # ignore some value types
            if isinstance(value, bool) or \
               isinstance(value, int) or \
               isinstance(value, long) or \
               isinstance(value, tuple) or \
               isinstance(value, list) or \
               isinstance(value, set) or \
               isinstance(value, dict) or \
               isinstance(value, NamedBlobImage) or \
               isinstance(value, NamedBlobFile) or \
               isinstance(value, NamedImage) or \
               isinstance(value, NamedFile) or \
               isinstance(value, DateTime) or \
               isinstance(value, date) or \
               isinstance(value, RelationValue) or \
               isinstance(value, Geolocation):
                continue

            if isinstance(getattr(obj, key), RichTextValue):
                value = getattr(obj, key).raw.replace('\r\n', '')
                data['html'][key] = value
                continue
                #rich = True
                #if key not in rich_fields:
                #    rich_fields.append(key)

            if is_json(value):
                continue

            #if key not in errors:
            #    errors.append(key)
            #force_unlock(trans_obj)
            #translated = retrieve_translation('EN', value, [language.upper()])
            data['item'][key] = value
    return data

def is_obj_skipped_for_translation(obj):
    #skip by portal types
    if obj.portal_type in ['eea.climateadapt.city_profile','LIF']:
        return True

    #skip by string in path
    skip_path_items = ['.jpg','.pdf','.png']
    obj_url = obj.absolute_url()
    if any(skip_item in obj_url for skip_item in skip_path_items):
        return True

    #TODO: add here archived and other rules
    return False

def get_translation_object(obj, language):
    translations = TranslationManager(obj).get_translations()
    if language not in translations:
        return None
    trans_obj = translations[language]
    return trans_obj

def get_translation_object_path(obj, language, site_url):
    trans_obj = get_translation_object(obj, language)
    if not trans_obj:
        return None
    trans_obj_url = trans_obj.absolute_url()
    return '/cca' + trans_obj_url.split(site_url)[-1]

def get_translation_object_from_uid(json_uid_file, catalog):
    brains = catalog.searchResults(UID=json_uid_file.replace(".json",""))
    if 0 == len(brains):
        return None
    return brains[0].getObject()

def get_translation_json_files(uid=None):
    json_files = []
    if uid:
        if os.path.exists("/tmp/jsons/"+str(uid)+".json"):
            json_files.append(str(uid)+".json")
    else:
        json_files = os.listdir("/tmp/jsons/")
    return json_files

def translation_step_1(site, request):
    """ Save all items for translation in a json file
    """
    limit = int(request.get('limit', 0))
    search_path = request.get('search_path', None)
    portal_type = request.get('portal_type', None)

    catalog = site.portal_catalog
    #TODO: remove this, it is jsut for demo purpose
    search_data = {}
    search_data['path'] = '/cca/en'
    if limit:
        search_data['sort_limit'] = limit
    if portal_type:
        search_data['portal_type'] = portal_type
    #brains = catalog.searchResults(path='/cca/en', sort_limit=limit)
    brains = catalog.searchResults(search_data)
    site_url = portal.getSite().absolute_url()
    logger.info("I will start to create json files. Checking...")

    res = {}
    total_items = 0  # total translatable eng objects

    for brain in brains:
        obj = brain.getObject()
        obj_url = obj.absolute_url()
        if is_obj_skipped_for_translation(obj):
            continue
        if search_path:
            if search_path not in obj_url:
                continue
        logger.info("PROCESS: %s", obj_url)

        data = get_object_fields_values(obj)
        json_object = json.dumps(data, indent = 4)
        #import pdb; pdb.set_trace()

        with open("/tmp/jsons/"+brain.UID+".json", "w") as outfile:
            outfile.write(json_object)
        if obj.portal_type not in res:
            res[obj.portal_type] = 1
        else:
            res[obj.portal_type] += 1

    logger.info("RESP %s", res)

def translation_step_2(site, request):
    language = request.get('language', None)
    uid = request.get('uid', None)
    limit = int(request.get('limit', 0))
    offset = int(request.get('offset', 0))
    portal_type = request.get('portal_type', None)

    """ Get all jsons objects in english and call etranslation for each field
        to be translated in specified language.
    """
    if language is None:
        return "Missing language parameter. (Example: ?language=it)"
    catalog = site.portal_catalog
    site_url = portal.getSite().absolute_url()
    #import pdb; pdb.set_trace()
    json_files = get_translation_json_files(uid)

    report = {}
    report['date'] = {'start':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'end':None}
    report['filter'] = {'language':language, 'uid':uid, 'limit': limit, 'offset': offset}
    total_files = len(json_files)  # total translatable eng objects (not unique)
    nr_files = 0  # total translatable eng objects (not unique)
    nr_items = 0  # total translatable eng objects (not unique)
    nr_html_items = 0  # total translatable eng objects (not unique)
    nr_items_translated = 0  # found translated objects
    #import pdb; pdb.set_trace()
    if limit:
        json_files.sort()
        json_files = json_files[offset: offset+limit]

    for json_file in json_files:
        file = open("/tmp/jsons/"+json_file, "r")
        json_content = file.read()
        json_data = json.loads(json_content)
        if portal_type and portal_type!=json_data['portal_type']:
            continue
        nr_files += 1
        #LOPP object tiles
        tile_html_fields = []
        for tile_id in json_data['tile'].keys():
            tile_data = json_data['tile'][tile_id]
            #LOOP tile text items
            for key in tile_data['item'].keys():
                res = retrieve_translation('EN', tile_data['item'][key], [language.upper()])
                nr_items += 1
                if 'translated' in res:
                    nr_items_translated += 1
            #LOOP tile HTML items
            for key in tile_data['html'].keys():
                value = tile_data['html'][key]
                value = value.replace('\r\n', '')
                try:
                    test_value = value + u"test"
                except UnicodeDecodeError:
                    value = value.decode("utf-8")
                tile_html_fields.append({'tile_id':tile_id,'field':key, 'value':value})
        #TILE HTML fields translate in one call
        if len(tile_html_fields):
            nr_html_items += 1
            obj = get_translation_object_from_uid(json_file, catalog)
            trans_obj_path = get_translation_object_path(obj, language, site_url)
            if not trans_obj_path:
                continue
            html_content = u"<!doctype html>" + \
                u"<head><meta charset=utf-8></head><body>"
            for item in tile_html_fields:
                html_tile = u"<div class='cca-translation-tile'" + \
                    u" data-field='" + item['field'] + u"'" + \
                    u" data-tile-id='" + item['tile_id'] + u"'" + \
                    u">" + item['value'] + u"</div>"
                html_content += html_tile

            html_content += u"</body></html>"
            html_content = html_content.encode('utf-8')
            translated = retrieve_html_translation(
                'EN',
                html_content,
                trans_obj_path,
                language.upper(),
                False,
            )

        #LOOP object text items
        for key in json_data['item'].keys():
            res = retrieve_translation('EN', json_data['item'][key], [language.upper()])
            nr_items += 1
            if 'translated' in res:
                nr_items_translated += 1
        #LOOP object HTML items
        if len(json_data['html']):
            nr_html_items += 1
            obj = get_translation_object_from_uid(json_file, catalog)
            trans_obj_path = get_translation_object_path(obj, language, site_url)
            if not trans_obj_path:
                continue

            html_content = u"<!doctype html><head><meta charset=utf-8></head>"
            html_content += u"<body>"

            for key in json_data['html'].keys():
                value = json_data['html'][key].replace('\r\n', '')
                html_section = u"<div class='cca-translation-section'" + \
                    u" data-field='" + key + u"'>" + value + u"</div>"

                html_content += html_section

            html_content += u"</body></html>"
            html_content = html_content.encode('utf-8')
            res = retrieve_html_translation(
                'EN',
                html_content,
                trans_obj_path,
                language.upper(),
                False,
            )
        logger.info("TransStep2 File  %s from %s, total files %s",nr_files, len(json_files), total_files)
        tmp_report = {}
        tmp_report['limit'] = limit
        tmp_report['offset'] = offset
        tmp_report['last_file_position'] = nr_files
        json_object = json.dumps(tmp_report, indent = 4)
        with open("/tmp/translate_step_2_last_file.json", "w") as outfile:
            outfile.write(json_object)
        time.sleep(2)

    report['date']['end'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report['response'] = {'items': {'nr_files': nr_files, 'nr':nr_items, 'nr_already_translated':nr_items_translated},'htmls':nr_html_items, 'portal_type':portal_type}
    report['total_files'] = total_files

    json_object = json.dumps(report, indent = 4)
    with open("/tmp/translate_step_2_"+language+"_"+str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".json", "w") as outfile:
        outfile.write(json_object)

    logger.info("Files: %s, TotalItems: %s, Already translated: %s HtmlItems: %s",
                nr_files, nr_items, nr_items_translated, nr_html_items)

def translation_step_3(site, request):
    """ Get all jsons objects in english and overwrite targeted language
        object with translations.
    """
    language = request.get('language', None)
    uid = request.get('uid', None)
    #limit = int(request.get('limit', 0))
    #offset = int(request.get('offset', 0))
    portal_type = request.get('portal_type', None)

    if language is None:
        return "Missing language parameter. (Example: ?language=it)"
    catalog = site.portal_catalog
    json_files = get_translation_json_files(uid)

    nr_files = 0  # total translatable eng objects (not unique)
    nr_items = 0  # total translatable eng objects (not unique)
    nr_items_translated = 0  # found translated objects

    for json_file in json_files:
        nr_files += 1

        obj = get_translation_object_from_uid(json_file, catalog)
        trans_obj = get_translation_object(obj, language)

        file = open("/tmp/jsons/"+json_file, "r")
        json_content = file.read()
        json_data = json.loads(json_content)
        if portal_type and portal_type!=json_data['portal_type']:
            continue
        have_change = False
        if 'tile' in json_data:
            for tile_id in json_data['tile'].keys():
                tile_data = json_data['tile'][tile_id]
                tile_annot_id = 'plone.tiles.data.' + tile_id
                tile = trans_obj.__annotations__.get(tile_annot_id, None)
                if not tile:
                    continue
                for key in tile_data['item'].keys():
                    try:
                        update = tile.data
                    except AttributeError:
                        update = tile
                    translated_msg = get_translated(tile_data['item'][key], language.upper())
                    if translated_msg:
                        update[key] = translated_msg
                        have_change = True
                    # tile.data.update(update)
                    trans_obj.__annotations__[tile_annot_id] = update

        for key in json_data['item'].keys():
            translated_msg = get_translated(json_data['item'][key], language.upper())
            if uid:
                logger.info(
                    "Nr_file: %s, Key: %s, Msg: %s, Translate: %s",
                    nr_files, key, json_data['item'][key], translated_msg)
            else:
                logger.info("Nr_file: %s, Key: %s", nr_files, key)

            if translated_msg:
                # TODO implement cover tiles case
                # Step 1 and 2 to be updated first, I think
                # try:
                #     encoded_text = translated_msg.encode('latin-1')
                #     tile.data['text'].raw = encoded_text
                # except AttributeError:
                #     logger.info("Error for tile. TODO improve.")
                #     logger.info(tile_id)

                encoded_text = translated_msg.encode('latin-1')

                source_richtext_types = [
                    'eea.climateadapt.publicationreport',
                    'eea.climateadapt.researchproject',
                    'eea.climateadapt.mapgraphdataset',
                    'eea.climateadapt.video',
                    ]

                if key == 'source' and \
                        obj.portal_type in source_richtext_types:
                    setattr(trans_obj, key, getattr(obj, key))
                    # solves Can not convert 'Elsevier' to an IRichTextValue
                    setattr(trans_obj, key, RichTextValue(encoded_text))
                    have_change = True
                else:
                    try:
                        setattr(trans_obj, key, encoded_text)
                        have_change = True
                    except AttributeError:
                        logger.info("AttributeError for obj: %s key: %s",
                                    obj.absolute_url(), key)
        if have_change:
            trans_obj._p_changed = True
            trans_obj.reindexObject()

    logger.info("Fianlize step 3")


def translation_step_4(site, language=None, uid=None):
    """ Copy fields values from en to given language for language independent
        fields.
    """
    if language is None:
        return "Missing language parameter. (Example: ?language=it)"
    catalog = site.portal_catalog

    brains = catalog.searchResults(path='/cca/en')
    site_url = portal.getSite().absolute_url()
    logger.info("Start copying values for language independent fields...")

    language_independent_fields = {
        "eea.climateadapt.tool": [
            "spatial_values", "storage_type", "publication_date",
            ],
        "eea.climateadapt.guidancedocument": [
            "storage_type", "spatial_values",
            ],
        "EasyForm": ["showFields"],
        "eea.climateadapt.adaptationoption": ["implementation_type"],
        "eea.climateadapt.mapgraphdataset": ["storage_type", "spatial_values"],
        "Collection": ["sort_reversed", "query"],
        "Document": ["table_of_contents"],
        "News Item": ["health_impacts"],
        "eea.climateadapt.casestudy": [
            "geolocation", "implementation_type", "spatial_values",
            ],
        "eea.climateadapt.aceproject": [
            "specialtagging", "spatial_values", "funding_programme",
            ],
        "eea.climateadapt.indicator": [
            "publication_date", "storage_type", "spatial_values"
            ],
        "eea.climateadapt.informationportal": [
            "spatial_values", "storage_type", "publication_date"
            ],
        "eea.climateadapt.organisation": [
            "storage_type", "spatial_values", "publication_date"
            ],
        "eea.climateadapt.publicationreport": [
            "storage_type", "spatial_values"
            ],
        "Event": [
            "start", "end", "effective", "timezone", "event_url",
            "health_impacts", "contact_email", "location", "contact_name"
            ],
        "cca-event": [
            "start", "end", "effective", "timezone", "contact_email",
            "contact_name"
            ],
    }

    for brain in brains:
        obj = brain.getObject()

        if obj.portal_type in language_independent_fields:
            obj_url = obj.absolute_url()
            logger.info("PROCESS: %s", obj_url)

            translations = TranslationManager(obj).get_translations()
            try:
                trans_obj = translations[language]
            except KeyError:
                logger.info("Missing translation for: %s", obj_url)
                continue

            force_unlock(trans_obj)
            reindex = False

            fields = language_independent_fields[obj.portal_type]
            for key in fields:
                logger.info("Field: %s", key)

                # TODO simplify this
                if key == 'start':
                    # setattr(trans_obj, key, obj.start)
                    trans_obj.start = obj.start
                    reindex = True
                elif key == 'end':
                    trans_obj.end = obj.end
                    # setattr(trans_obj, key, obj.start)
                    reindex = True
                elif key == 'effective':
                    trans_obj.setEffectiveDate(obj.effective_date)
                    reindex = True
                elif key == 'timezone':
                    trans_obj.timezone = obj.timezone
                    reindex = True
                else:
                    try:
                        setattr(trans_obj, key, getattr(obj, key))
                        reindex = True
                    except Exception:
                        logger.info("Skip: %s %s", obj.portal_type, key)

            if reindex is True:
                # reindex object
                trans_obj._p_changed = True
                trans_obj.reindexObject()
                continue

    logger.info("Finalize step 4")


def translation_list_type_fields(site):
    """ Show each field for each type
    """
    catalog = site.portal_catalog
    #TODO: remove this, it is jsut for demo purpose
    limit=10000
    brains = catalog.searchResults(path='/cca/en', sort_limit=limit)
    site_url = portal.getSite().absolute_url()
    logger.info("I will start to create json files. Checking...")

    res = {}
    total_items = 0  # total translatable eng objects

    for brain in brains:
        obj = brain.getObject()
        obj_url = obj.absolute_url()
        logger.info("PROCESS: %s", obj_url)
        if is_obj_skipped_for_translation(obj):
            continue
        data = get_object_fields_values(obj)

        if obj.portal_type not in res:
            res[obj.portal_type] = {"item":[],"html":[]}
        for key in data['item']:
            if key not in res[obj.portal_type]["item"]:
                res[obj.portal_type]["item"].append(key)
        for key in data['html']:
            if key not in res[obj.portal_type]["html"]:
                res[obj.portal_type]["html"].append(key)

    json_object = json.dumps(res, indent = 4)
    #import pdb; pdb.set_trace()

    with open("/tmp/portal_type_fields.json", "w") as outfile:
        outfile.write(json_object)

def translations_status_by_version(site, version=0, language=None):
    """ Show the list of urls of a version and language
    """
    if language is None:
        return "Missing language."

    path = '/cca/' + language
    version = int(version)
    catalog = site.portal_catalog
    brains = catalog.searchResults()
    brains = catalog.searchResults(path=path)

    res = []
    template = "<p>{}</p>"

    for brain in brains:
        obj = brain.getObject()
        obj_version = int(getattr(obj, 'version', 0))

        if obj_version != version:
            continue

        res.append(template.format(obj.absolute_url()))

    return "".join(res)


def get_tile_type(tile, from_cover, to_cover):
    """ Return tile type
    """
    tiles_types = {
        'RichTextWithTitle': 'eea.climateadapt.richtext_with_title',
        'EmbedTile': 'collective.cover.embed',
        'RichTextTile': 'collective.cover.richtext',
        'SearchAceContentTile': 'eea.climateadapt.search_acecontent',
        'GenericViewTile': 'eea.climateadapt.genericview',
        'RelevantAceContentItemsTile': 'eea.climateadapt.relevant_acecontent',
        'ASTNavigationTile': 'eea.climateadapt.ast_navigation',
        'ASTHeaderTile': 'eea.climateadapt.ast_header',
        'FilterAceContentItemsTile': 'eea.climateadapt.filter_acecontent',
        'TransRegionalSelectTile': 'eea.climateadapt.transregionselect',
        'SectionNavTile': 'eea.climateadapt.section_nav',
        'CountrySelectTile': 'eea.climateadapt.countryselect',
        'BannerTile': 'collective.cover.banner',
        'ShareInfoTile': 'eea.climateadapt.shareinfo',
        'FormTile': 'eea.climateadapt.formtile',
        'UrbanMenuTile': 'eea.climateadapt.urbanmenu',
        'CardsTile': 'eea.climateadapt.cards_tile',
    }
    for a_type in tiles_types.keys():
        if a_type in str(type(tile)):
            return tiles_types[a_type]

    return None


def copy_tiles(tiles, from_cover, to_cover):
    """ Copy the tiles from cover to translated cover
    """
    logger.info("Copy tiles")
    logger.info(from_cover.absolute_url())
    logger.info(to_cover.absolute_url())
    for tile in tiles:
        tile_type = get_tile_type(tile, from_cover, to_cover)

        if tile_type is not None:
            from_tile = from_cover.restrictedTraverse(
                '@@{0}/{1}'.format(tile_type, tile.id)
            )

            to_tile = to_cover.restrictedTraverse(
                '@@{0}/{1}'.format(tile_type, tile.id)
            )

            from_data_mgr = ITileDataManager(from_tile)
            to_data_mgr = ITileDataManager(to_tile)
            to_data_mgr.set(from_data_mgr.get())

        else:
            logger.info("Missing tile type")
            import pdb; pdb.set_trace()


def create_translation_object(obj, language):
    """ Create translation object for an obj
    """
    if language in TranslationManager(obj).get_translations():
        logger.info("Skip creating translation. Already exists.")
        return

    factory = DefaultTranslationFactory(obj)

    translated_object = factory(language)

    TranslationManager(obj).register_translation(language, translated_object)

    # https://github.com/plone/plone.app.multilingual/blob/2.x/src/plone/app/multilingual/manager.py#L85
    # translated_object.reindexObject()   ^ already reindexed.

    if obj.portal_type == 'collective.cover.content':
        tiles = [obj.get_tile(x) for x in obj.list_tiles()]
        translated_object.cover_layout = obj.cover_layout
        copy_tiles(tiles, obj, translated_object)

        translated_object.reindexObject()


def get_all_objs(container):
    """ Get the container's objects
    """
    all_objs = []

    def get_objs(context):
        contents = api.content.find(context=context, depth=1)
        for item in contents:
            all_objs.append(item)

        for item in contents:
            get_objs(item.getObject())

    get_objs(container)

    return all_objs


def execute_trans_script(site, language):
    """ Clone the content to be translated
    """
    catalog = site.portal_catalog
    english_container = site['en']
    language_folders = [
        x.id for x in catalog.searchResults(path='/cca', portal_type='LRF')]
    language_folders.remove('en')

    lang_independent_objects = [
        "newsletter", "Members", "repository", "test-baltic", "frontpage",
        "admin",  "more-latest-updates", "sandbox", "portal_pdf",
        "portal_vocabularies", "portal_depiction", "frontpage-slides",
        "dashboard", "latest-modifications-on-climate-adapt",
        "covenant-of-mayors-external-website", "rss-feed",
        "latest-news-events-on-climate-adapt",
        "specific-privacy-statement-for-climate-adapt",
        "privacy-and-legal-notice", "database-items-overview", "broken-links",
        "observatory-organisations",
        "observatory-management-group-organisations",
        "indicators-backup", "eea-copyright-notice", "eea-disclaimer",
        "user-dashboard"]

    # move folders under /en/
    for brain in site.getFolderContents():
        obj = brain.getObject()

        if obj.portal_type != 'LRF' and obj.id not in lang_independent_objects:
            content.move(source=obj, target=english_container)

    transaction.commit()
    errors = []
    # get and parse all objects under /en/
    res = get_all_objs(english_container)

    failed_translations = []
    count = 0
    for brain in res:
        logger.info('--------------------------------------------------------')
        logger.info(count)
        count += 1
        if brain.getPath() == '/cca/en' or brain.portal_type == 'LIF':
            continue
        obj = brain.getObject()
        try:
            create_translation_object(obj, language)
            logger.info("Cloned: %s" % obj.absolute_url())
        except Exception as err:
            logger.info("Error cloning: %s" % obj.absolute_url())
            if err.message == 'Translation already exists':
                continue
            else:
                errors.append(obj)
                # import pdb; pdb.set_trace()

        if count % 200 == 0:
            logger.info("Processed %s objects" % count)
            transaction.commit()

    transaction.commit()
    logger.info("Errors")
    logger.info(errors)
    logger.info("Finished cloning for language %s" % language)

    return 'Finished cloning for language %s' % language


def admin_some_translated(site, items):
    """ Create a list of links to be tested (for translation) for each
        content type
    """
    items = int(items)
    catalog = site.portal_catalog
    portal_types = []
    links = {}
    fields = {}

    res = catalog.searchResults(path='/cca/en')
    count = -1
    for brain in res:
        count += 1
        logger.info(count)
        obj = brain.getObject()

        portal_type = obj.portal_type
        if portal_type not in portal_types:
            portal_types.append(portal_type)
            links[portal_type] = []

            # get behavior fields and values
            behavior_assignable = IBehaviorAssignable(obj)
            _fields = {}
            if behavior_assignable:
                behaviors = behavior_assignable.enumerateBehaviors()
                for behavior in behaviors:
                    for k, v in getFieldsInOrder(behavior.interface):
                        _fields.update({k: v})

            #  get schema fields and values
            for k, v in getFieldsInOrder(obj.getTypeInfo().lookupSchema()):
                _fields.update({k: v})

            fields[portal_type] = [(x, _fields[x]) for x in _fields]

        if len(links[portal_type]) < items:
            links[portal_type].append(obj.absolute_url())

    return {'Content types': portal_types, 'Links': links, 'fields': fields}


class PrepareTranslation(BrowserView):
    """ Clone the content to be available for a new translation
        Usage: /admin-prepare-translation?language=ro
    """

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        return execute_trans_script(getSite(), **kwargs)


class VerifyClonedLanguage(BrowserView):
    """ Use this view to check all links for a new cloned language
        Usage: /admin-verify-cloned?language=ro
    """

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        return verify_cloned_language(getSite(), **kwargs)


class VerifyTranslationFields(BrowserView):
    """ Use this view to check all links for a new cloned language
        Usage: /admin-verify-translation-fields?language=ro
    """

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        return verify_translation_fields(getSite(), **kwargs)


class TranslateStep1(BrowserView):
    """ Use this view to get a json files for all eng objects
        Usage: /admin-translate-step-1?limit=10&search_path=some-words-in-url
        Limit and search_path params are optional
    """

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        return translation_step_1(getSite(), self.request)


class TranslateStep2(BrowserView):
    """ Use this view to translate all json files to a language
        Usage: /admin-translate-step-2?language=ro&uid=ABCDEF
        uid is optional
    """

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        return translation_step_2(getSite(), self.request)


class TranslateStep3(BrowserView):
    """ Use this view to save the values from annotation in objects fields
        Usage: /admin-translate-step-3?language=ro&uid=ABCDEF
        uid is optional
    """

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        return translation_step_3(getSite(), self.request)


class TranslateStep4(BrowserView):
    """ Use this view to copy fields values that are language independent
        Usage: /admin-translate-step-4?language=ro&uid=ABCDEF
        uid is optional
    """

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        language = None
        uid = None
        if 'language' in kwargs:
            language = kwargs['language']
        if 'uid' in kwargs:
            uid = kwargs['uid']
        return translation_step_4(getSite(), language, uid)


class TranslationListTypeFields(BrowserView):
    """ Use this view to translate all json files to a language
        Usage: /admin-translate-step-2?language=ro
    """

    def __call__(self, **kwargs):
        return translation_list_type_fields(getSite())


class SomeTranslated(BrowserView):
    """ Prepare a list of links for each content type in order to verify
        translation
        Usage: /admin-some-translated?items=10
    """

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        return admin_some_translated(getSite(), **kwargs)


class RunTranslation(BrowserView):
    """ Translate the contents
        Usage:
        /admin-run-translation?language=it&version=1&skip=1200  -skip 1200 objs
        /admin-run-translation?language=it&version=1
    """

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        return initiate_translations(getSite(), **kwargs)


class RunTranslationSingleItem(BrowserView):
    """ Translate a single item
        Usage: item/admin-translate-this

        To be used for testing translation without waiting for all objects to
        be updated
    """

    def __call__(self, **kwargs):
        import pdb; pdb.set_trace()
        obj = self.context
        result = translate_obj(obj)
        transaction.commit()
        return result


class TranslationStatus(BrowserView):
    """ Display the the current versions for all translated objects
    """

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)

        if "version" in kwargs:
            return translations_status_by_version(getSite(), **kwargs)

        return translations_status(getSite(), **kwargs)


class TranslationStateViewlet(ViewletBase):
    """ Display the translation state
    """

    trans_wf_id = 'cca_translations_workflow'
    css_types = {
        'not_translated': 'error',
        'translation_not_approved': 'warning',
        'translation_approved': 'info',
    }

    def show_approve_button(self):
        context = self.context
        state, wf_state = self._get_current_wf_state(context)

        return state == 'translation_not_approved'

    def get_css_class(self):
        context = self.context
        css_class = "portalMessage {}"
        state, wf_state = self._get_current_wf_state(context)
        css_type = self.css_types.get(state, '')

        return css_class.format(css_type)

    def _get_current_wf_state(self, context=None):
        if context is None:
            context = self.context

        wftool = get_tool('portal_workflow')
        wf = None

        for _wf in wftool.getWorkflowsFor(context):
            if _wf.id != self.trans_wf_id:
                continue

            wf = _wf

        if not wf:
            return 'Translation state not found', None

        initial_state = wf.initial_state
        state = (wftool.getStatusOf('cca_translations_workflow', self.context)
                    or {})
        state = state.get("review_state", initial_state)
        wf_state = wf.states[state]

        return state, wf_state

    def get_status(self, context=None):
        state, wf_state = self._get_current_wf_state(context)
        title = wf_state and wf_state.title.strip() or state

        return title

    def get_transitions(self, context=None):
        if not context:
            context = self.context

        wftool = get_tool('portal_workflow')
        transitions = wftool.listActionInfos(object=context)

        return [t for t in transitions if t['allowed']]
