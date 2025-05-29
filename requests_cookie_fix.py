import re


def fix_cookie_settings(headers):
    """
    A Set-Cookie header with multiple cookies will fail to parse
    so split those up into multiple Set-Cookie headers (one per cookie).

    The Max-Age attribute on cookies should be an int. It can fail
    to parse if its a float. Floating point max ages have been seen
    in the wild, so convert those to int so they will parse.
    """
    setcookies = headers.get_all('Set-Cookie')
    if setcookies != None:
        del headers['Set-Cookie']
        for setcookie in setcookies:
            # remove comma from expires, so split(',') will work
            setcookie = re.sub('expires=(...),', r'expires=\1', setcookie)
            for newcookie in setcookie.split(','):
                newcookie = newcookie.strip()
                newcookie = re.sub(r'Max-Age=(\d+)\.\d+', r'Max-Age=\1', newcookie)
                headers.add_header('Set-Cookie', newcookie)

def mock_res_init(self, headers):
    fix_cookie_settings(headers)
    self._headers = headers

def patch_requests(requests):
    requests.cookies.MockResponse.__init__ = mock_res_init

import requests
patch_requests(requests)
