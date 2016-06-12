# -*- coding: utf-8 -*-
import requests
import config


headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
} 

class HttpHelper(object):
    """docstring for HttpHelper"""
    def __init__(self):
        super(HttpHelper, self).__init__()
        self.cookies = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            }
        self.timeout = config.request_timeout

    def set_cookies(self, cookies):
        self.cookies = cookies

    def get(self, url):
        if self.cookies:
            return requests.get(url, headers=self.headers, cookies=self.cookies, timeout=self.timeout)
        else:
            return requests.get(url, headers=self.headers, timeout=self.timeout)

h_helper = HttpHelper()


def load_cookies(url):
    new_url = make_url(url)
    r = h_helper.get(new_url)
    h_helper.set_cookies(r.cookies)

def http_get(url):
    """Send a http request.
    """
    new_url = make_url(url)
    r = h_helper.get(new_url)
    status_code = parser_respond_status(r)
    return r, status_code

def make_url(url):
    """Format url.
    """
    if url.startswith('/'):
        return '%s%s' % (config.url_head, url)
    else:
        return '%s/%s' % (config.url_head, url)

def parser_respond_status(r):
    status_code = r.status_code
        
    if status_code == 200 and len(r.history) > 1:
        last_r = r.history[-1]
        r_location = last_r.headers.get('location')
        if not r_location.startswith(config.url_head):
            status_code = 302
        elif r_location == config.url_404:
            status_code = 404

    return status_code
