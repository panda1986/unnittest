import json
import eventlet, eventlet.green.urllib2
from bravo_constants import Errors

tag = "bravo_utility"

'''
never use the system json.loads directly.
'''
def json_loads(s):
    return json.loads(s, encoding="utf-8");

def bravo_http_get(url, ignore_error = False):
    (code, data, msg) = http_get(url, ignore_error);

    if not Errors.is_success(code):
        return (code, None, msg);

    # check common json pattern.
    if not Errors.valid_msg(data):
        code = Errors.system_json_pattern;
        desc = "bravo json pattern check error, url=%s, code=%d, data=%s"%(url, code, data);
        if not ignore_error:
            msg = '%s, http_request+get+error %s' % (tag, desc);
        return (code, None, msg);

    code = data["code"];
    if not Errors.is_success(code):
        desc = "bravo json indicates error, url=%s, code=%d, data=%s"%(url, code, data);
        if not ignore_error:
            msg = '%s, http_request+get+error %s' % (tag, desc);
        return (code, None, msg);

    # use the data in json pattern instead.
    data = data["data"];

    return (code, data, msg);

def http_get(url, ignore_error = False):
    (code, data, msg) = (Errors.success, None, '');

    conn = None;
    try:
        conn = eventlet.green.urllib2.urlopen(url=str(url));
        res = conn.read();
    except Exception, ex:
        code = Errors.system_network_http_get;
        desc = "http get error, url=%s, code=%d, ex=%s"%(url, code, ex);
        if not ignore_error:
            msg = '%s, http_request+get+error %s' % (tag, desc)
        return (code, data, msg);
    finally:
        if conn:
            #conn.close();
            pass;

    try:
        data = json_loads(res);
    except Exception, ex:
        code = Errors.system_network_json_parse;
        desc = "parse http response to json error, url=%s, code=%d, res=%s, ex=%s"%(url, code, res, ex);
        if not ignore_error:
            msg = '%s, http_request+get+error %s' % (tag, desc)
        return (code, data, msg);

    return (code, data, msg);