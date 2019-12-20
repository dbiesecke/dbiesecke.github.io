# -*- coding: utf-8 -*-
import cookielib

#from kennethreitz module "requests"
def create_cookie(name, value, **kwargs):
    """Make a cookie from underspecified parameters.
            By default, the pair of `name` and `value` will be set for the domain ''
            and sent on every request (this is sometimes called a "supercookie").
            """
    result = dict(
        version=0,
        name=name,
        value=value,
        port=None,
        domain='',
        path='/',
        secure=False,
        expires=None,
        discard=True,
        comment=None,
        comment_url=None,
        rest={'HttpOnly': None},
        rfc2109=False, )

    badargs = set(kwargs) - set(result)
    if badargs:
        err = 'create_cookie() got unexpected keyword arguments: %s'
        raise TypeError(err % list(badargs))
    result.update(kwargs)
    result['port_specified'] = bool(result['port'])
    result['domain_specified'] = bool(result['domain'])
    result['domain_initial_dot'] = result['domain'].startswith('.')
    result['path_specified'] = bool(result['path'])
    return cookielib.Cookie(**result)


def check_cookies(cookie_jar):
    for entry in cookie_jar:
        if entry.expires > 2**32-1:
            entry.expires = 2**32-1
