import json
import eventlet, eventlet.green.urllib2
from bravo_constants import Errors

tag = "bravo_utility"

'''
never use the system json.loads directly.
'''
def json_loads(s):
    return json.loads(s, encoding="utf-8");

'''
never use the system json.dumps directly.
'''
def json_dumps(obj):
    return json.dumps(obj, ensure_ascii=False, encoding="utf-8");

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
        msg = "%s, http_request+get url=%s" % (tag, url)
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

def bravo_http_post(url, json_data, timeout=None, method="POST"):
    (code, data, msg) = http_post(url, json_data, timeout, method);

    if not Errors.is_success(code):
        return (code, None, msg);

    # check common json pattern.
    if not Errors.valid_msg(data):
        code = Errors.system_json_pattern;
        desc = "bravo json pattern check error, url=%s, code=%d, data=%s"%(url, code, data);
        msg = '%s, http_request+post+error %s' % (tag, desc);
        return (code, None, msg);

    code = data["code"];
    if not Errors.is_success(code):
        desc = "bravo json indicates error, url=%s, code=%d, data=%s"%(url, code, data);
        msg = '%s, http_request+post+error %s' % (tag, desc);
        return (code, None, msg);

    # use the data in json pattern instead.
    data = data["data"];

    return (code, data, msg);

def http_post(url, json_data=None, timeout=None, method="POST", headers=None):
    (code, data, msg) = (Errors.success, None, "");

    if headers is None:
        headers = {};
        headers["Content-Type"] = "application/json;charset=utf-8";
        headers["Accept"] = "application/json";

    conn = None;
    try:
        # never use system default block request, use eventlet instead.
        if json_data:
            req = eventlet.green.urllib2.Request(url=str(url), data=str(json_data), headers=headers);
        else:
            req = eventlet.green.urllib2.Request(url=str(url), headers=headers);
        req.get_method = lambda: method;

        if timeout:
            conn = eventlet.green.urllib2.urlopen(req, timeout=timeout);
        else:
            conn = eventlet.green.urllib2.urlopen(req);
        res = conn.read();
        msg = "%s, http_request+post method=%s, url=%s, res=%s"%(tag, method, url, res);
    except Exception, ex:
        code = Errors.system_network_http_post;
        msg= "%s, http_request+post+error http post error, method=%s, "\
              "url=%s, code=%d, exception=%s"%(tag, method, url, code, ex)
        return (code, data, msg);
    finally:
        if conn:
            #conn.close();
            pass;

    try:
        if not res.startswith('{'):
            # remove the jsonp content for ums response
            data = res[res.index('({') + 1: -1]
        else:
            data = json_loads(res);
    except Exception, ex:
        code = Errors.system_network_json_parse;
        msg = "%s, http_request+post+error parse http response to json error, method=%s, "\
              "url=%s, code=%d, res=%s, exception=%s"%(tag, method, url, code, res, ex)
        return (code, data, msg);

    return (code, data, msg);