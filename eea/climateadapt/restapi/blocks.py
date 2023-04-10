from eea.climateadapt.tiles.search_acecontent import AceTileMixin
from plone.restapi.behaviors import IBlocks
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest


@implementer(IBlockFieldSerializationTransformer)
@adapter(IBlocks, IBrowserRequest)
class SearchAceContentBlockSerializer(object):
    order = 100
    block_type = "searchAceContent"

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, block):

        ace = AceTileMixin()
        ace.context = self.context
        ace.request = self.request
        ace.data = block
        ace.current_lang = 'en'

        block['_v_results'] = ace.sections()
        print('sections', block)

        # portal_transforms = api.portal.get_tool(name="portal_transforms")
        # raw_html = block.get("html", "")
        # data = portal_transforms.convertTo(
        #     "text/x-html-safe", raw_html, mimetype="text/html"
        # )
        # html = data.getData()
        # block["html"] = html

        return block
