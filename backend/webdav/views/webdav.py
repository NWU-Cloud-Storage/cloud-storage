from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, PermissionDenied, NotFound
from rest_framework.response import Response
from .fs_dav_provider import FilesystemProvider
from defusedxml.lxml import _etree as etree
from . import utils


def send_multi_status_response(multistatusEL):

    # Hotfix for Windows XP
    # PROPFIND XML response is not recognized, when pretty_print = True!
    # (Vista and others would accept this).
    xml_data = utils.xml_to_bytes(multistatusEL, pretty_print=False)
    # If not, Content-Length is wrong!
    assert utils.is_bytes(xml_data), xml_data

    # headers = [
    #     ("Content-Type", "application/xml"),
    #     ("Date", utils.get_rfc1123_time()),
    #     ("Content-Length", str(len(xml_data))),
    # ]

    headers = {
        "Content-Type": "application/xml",
        "Date": utils.get_rfc1123_time(),
        "Content-Length": str(len(xml_data))
    }

    #    if 'keep-alive' in environ.get('HTTP_CONNECTION', '').lower():
    #        headers += [
    #            ('Connection', 'keep-alive'),
    #        ]

    # start_response("207 Multi-Status", headers
    # TODO data是xml吗？
    return Response(status=207, headers=headers, data=xml_data)


class WebDAVAPI(APIView):
    http_method_names = APIView.http_method_names + \
                        ['propfind', 'proppatch', 'lock', 'unlock', 'copy', 'move', 'mkcol']
    _davProvider = FilesystemProvider
    allow_propfind_infinite = True

    def profind(self, request, environ, path=None):
        """
        TODO: does not yet support If and If HTTP Conditions
        @see http://www.webdav.org/specs/rfc4918.html#METHOD_PROPFIND
        """
        path = '/' + path
        res = self._davProvider.get_resource_inst(path, environ)

        # RFC: By default, the PROPFIND method without a Depth header MUST act
        # as if a "Depth: infinity" header was included.
        http_depth = request.headers.get('Depth', 'infinity')

        # 暂不明客户端是怎么响应错误的，先按DRF的方式来写
        if http_depth not in ("0", "1", "infinity"):
            raise ParseError()
        if http_depth == 'infinity' and not self.allow_propfind_infinite:
            raise PermissionDenied()

        if res is None:
            raise NotFound()

        # TODO
        # self._evaluate_if_headers(res, environ)

        # Parse PROPFIND request
        # requestEL = util.parse_xml_body(environ, allow_empty=True)
        requestEL = etree.fromstring(request.body.decode())  # request body is a bytestring
        if requestEL is None:
            # An empty PROPFIND request body MUST be treated as a request for
            # the names and values of all properties.
            requestEL = etree.XML(
                "<D:propfind xmlns:D='DAV:'><D:allprop/></D:propfind>"
            )

        if requestEL.tag != "{DAV:}propfind":
            raise ParseError()

        propNameList = []
        propFindMode = None
        for pfnode in requestEL:
            if pfnode.tag == "{DAV:}allprop":
                if propFindMode:
                    # RFC: allprop and name are mutually exclusive
                    raise ParseError()
                propFindMode = "allprop"
            # TODO: implement <include> option
            #            elif pfnode.tag == "{DAV:}include":
            #                if not propFindMode in (None, "allprop"):
            #                    self._fail(HTTP_BAD_REQUEST,
            #                        "<include> element is only valid with 'allprop'.")
            #                for pfpnode in pfnode:
            #                    propNameList.append(pfpnode.tag)
            elif pfnode.tag == "{DAV:}name":
                if propFindMode:  # RFC: allprop and name are mutually exclusive
                    raise ParseError()
                propFindMode = "name"
            elif pfnode.tag == "{DAV:}prop":
                # RFC: allprop and name are mutually exclusive
                if propFindMode not in (None, "named"):
                    raise ParseError()
                propFindMode = "named"
                for pfpnode in pfnode:
                    propNameList.append(pfpnode.tag)

        # --- Build list of resource URIs

        reslist = res.get_descendants(depth=http_depth, add_self=True)
        #        if environ["wsgidav.verbose"] >= 3:
        #            pprint(reslist, indent=4)

        multistatusEL = utils.make_multistatus_el()
        responsedescription = []

        for child in reslist:

            if propFindMode == "allprop":
                propList = child.get_properties("allprop")
            elif propFindMode == "name":
                propList = child.get_properties("name")
            else:
                propList = child.get_properties("named", name_list=propNameList)

            href = child.get_href()
            utils.add_property_response(multistatusEL, href, propList)

        if responsedescription:
            etree.SubElement(
                multistatusEL, "{DAV:}responsedescription"
            ).text = "\n".join(responsedescription)

        return send_multi_status_response(multistatusEL)
