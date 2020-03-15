from defusedxml.lxml import _etree as etree

_ElementType = etree._Element
use_lxml = True

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_ACCEPTED = 202
HTTP_NON_AUTHORITATIVE_INFO = 203
HTTP_NO_CONTENT = 204
HTTP_RESET_CONTENT = 205
HTTP_PARTIAL_CONTENT = 206
HTTP_MULTI_STATUS = 207
HTTP_IM_USED = 226

HTTP_MULTIPLE_CHOICES = 300
HTTP_MOVED = 301
HTTP_FOUND = 302
HTTP_SEE_OTHER = 303
HTTP_NOT_MODIFIED = 304
HTTP_USE_PROXY = 305
HTTP_TEMP_REDIRECT = 307
HTTP_BAD_REQUEST = 400
HTTP_PAYMENT_REQUIRED = 402
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405
HTTP_NOT_ACCEPTABLE = 406
HTTP_PROXY_AUTH_REQUIRED = 407
HTTP_REQUEST_TIMEOUT = 408
HTTP_CONFLICT = 409
HTTP_GONE = 410
HTTP_LENGTH_REQUIRED = 411
HTTP_PRECONDITION_FAILED = 412
HTTP_REQUEST_ENTITY_TOO_LARGE = 413
HTTP_REQUEST_URI_TOO_LONG = 414
HTTP_MEDIATYPE_NOT_SUPPORTED = 415
HTTP_RANGE_NOT_SATISFIABLE = 416
HTTP_EXPECTATION_FAILED = 417
HTTP_UNPROCESSABLE_ENTITY = 422
HTTP_LOCKED = 423
HTTP_FAILED_DEPENDENCY = 424
HTTP_UPGRADE_REQUIRED = 426

HTTP_INTERNAL_ERROR = 500
HTTP_NOT_IMPLEMENTED = 501
HTTP_BAD_GATEWAY = 502
HTTP_SERVICE_UNAVAILABLE = 503
HTTP_GATEWAY_TIMEOUT = 504
HTTP_VERSION_NOT_SUPPORTED = 505
HTTP_INSUFFICIENT_STORAGE = 507
HTTP_NOT_EXTENDED = 510


ERROR_DESCRIPTIONS = {
    HTTP_OK: "200 OK",
    HTTP_CREATED: "201 Created",
    HTTP_NO_CONTENT: "204 No Content",
    HTTP_NOT_MODIFIED: "304 Not Modified",
    HTTP_BAD_REQUEST: "400 Bad Request",
    HTTP_FORBIDDEN: "403 Forbidden",
    HTTP_METHOD_NOT_ALLOWED: "405 Method Not Allowed",
    HTTP_NOT_FOUND: "404 Not Found",
    HTTP_CONFLICT: "409 Conflict",
    HTTP_PRECONDITION_FAILED: "412 Precondition Failed",
    HTTP_RANGE_NOT_SATISFIABLE: "416 Range Not Satisfiable",
    HTTP_MEDIATYPE_NOT_SUPPORTED: "415 Media Type Not Supported",
    HTTP_LOCKED: "423 Locked",
    HTTP_FAILED_DEPENDENCY: "424 Failed Dependency",
    HTTP_INTERNAL_ERROR: "500 Internal Server Error",
    HTTP_NOT_IMPLEMENTED: "501 Not Implemented",
    HTTP_BAD_GATEWAY: "502 Bad Gateway",
}


def make_multistatus_el():
    """Wrapper for etree.Element, that takes care of unsupported nsmap option."""
    if use_lxml:
        return etree.Element("{DAV:}multistatus", nsmap={"D": "DAV:"})
    return etree.Element("{DAV:}multistatus")


def get_http_status_code(v):
    """Return HTTP response code as integer, e.g. 204."""
    if hasattr(v, "value"):
        return int(v.value)  # v is a DAVError
    else:
        return int(v)


def split_namespace(clarkName):
    """Return (namespace, localname) tuple for a property name in Clark Notation.

    Namespace defaults to ''.
    Example:
    '{DAV:}foo'  -> ('DAV:', 'foo')
    'bar'  -> ('', 'bar')
    """
    if clarkName.startswith("{") and "}" in clarkName:
        ns, localname = clarkName.split("}", 1)
        return (ns[1:], localname)
    return ("", clarkName)


def make_sub_element(parent, tag, nsmap=None):
    """Wrapper for etree.SubElement, that takes care of unsupported nsmap option."""
    if use_lxml:
        return etree.SubElement(parent, tag, nsmap=nsmap)
    return etree.SubElement(parent, tag)


def is_etree_element(obj):
    return isinstance(obj, _ElementType)


def get_http_status_string(v):
    """Return HTTP response string, e.g. 204 -> ('204 No Content').
    The return string always includes descriptive text, to satisfy Apache mod_dav.

    `v`: status code or DAVError
    """
    code = get_http_status_code(v)
    try:
        return ERROR_DESCRIPTIONS[code]
    except KeyError:
        return "{} Status".format(code)


def to_unicode(s, encoding="utf8"):
    """Convert data to native str type (bytestring on Py2 and unicode on Py3)."""
    if type(s) is bytes:
        s = str(s, encoding)
    elif type(s) is not str:
        s = str(s)
    return s


def to_unicode_safe(s):
    """Convert a binary string to Unicode using UTF-8 (fallback to ISO-8859-1)."""
    try:
        u = to_unicode(s, "utf8")
    except ValueError:
        u = to_unicode(s, "ISO-8859-1")
    return u


def add_property_response(multistatusEL, href, propList):
    """Append <response> element to <multistatus> element.

    <prop> node depends on the value type:
      - str or unicode: add element with this content
      - None: add an empty element
      - etree.Element: add XML element as child
      - DAVError: add an empty element to an own <propstatus> for this status code

    @param multistatusEL: etree.Element
    @param href: global URL of the resource, e.g. 'http://server:port/path'.
    @param propList: list of 2-tuples (name, value)
    """
    # Split propList by status code and build a unique list of namespaces
    nsCount = 1
    nsDict = {}
    nsMap = {}
    propDict = {}

    for name, value in propList:
        status = "200 OK"
        if isinstance(value, DAVError):
            status = get_http_status_string(value)
            # Always generate *empty* elements for props with error status
            value = None

        # Collect namespaces, so we can declare them in the <response> for
        # compacter output
        ns, _ = split_namespace(name)
        if ns != "DAV:" and ns not in nsDict and ns != "":
            nsDict[ns] = True
            nsMap["NS{}".format(nsCount)] = ns
            nsCount += 1

        propDict.setdefault(status, []).append((name, value))

    # <response>
    responseEL = make_sub_element(multistatusEL, "{DAV:}response", nsmap=nsMap)

    #    log("href value:{}".format(string_repr(href)))
    #    etree.SubElement(responseEL, "{DAV:}href").text = toUnicode(href)
    etree.SubElement(responseEL, "{DAV:}href").text = href
    #    etree.SubElement(responseEL, "{DAV:}href").text = compat.quote(href, safe="/" + "!*'(),"
    #       + "$-_|.")

    # One <propstat> per status code
    for status in propDict:
        propstatEL = etree.SubElement(responseEL, "{DAV:}propstat")
        # List of <prop>
        propEL = etree.SubElement(propstatEL, "{DAV:}prop")
        for name, value in propDict[status]:
            if value is None:
                etree.SubElement(propEL, name)
            elif is_etree_element(value):
                propEL.append(value)
            else:
                # value must be string or unicode
                #                log("{} value:{}".format(name, string_repr(value)))
                #                etree.SubElement(propEL, name).text = value
                etree.SubElement(propEL, name).text = to_unicode_safe(value)
        # <status>
        etree.SubElement(propstatEL, "{DAV:}status").text = "HTTP/1.1 {}".format(status)


def xml_to_bytes(element, pretty_print=False):
    """Wrapper for etree.tostring, that takes care of unsupported pretty_print
    option and prepends an encoding header."""
    if use_lxml:
        xml = etree.tostring(
            element, encoding="UTF-8", xml_declaration=True, pretty_print=pretty_print
        )
    else:
        xml = etree.tostring(element, encoding="UTF-8")
        if not xml.startswith(b"<?xml "):
            xml = b'<?xml version="1.0" encoding="utf-8" ?>\n' + xml

    assert xml.startswith(b"<?xml ")  # ET should prepend an encoding header
    return xml


def is_bytes(s):
    """Return True for bytestrings (for str on Py2 and bytes on Py3)."""
    return isinstance(s, str)


from email.utils import formatdate
def get_rfc1123_time(secs=None):
    """Return <secs> in rfc 1123 date/time format (pass secs=None for current date)."""
    # GC issue #20: time string must be locale independent
    return formatdate(timeval=secs, localtime=False, usegmt=True)