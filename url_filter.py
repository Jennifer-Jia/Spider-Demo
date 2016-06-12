# -*- coding: utf-8 -*-

import re
import config


def is_url_match(url):
    pattern = re.compile(r'^(/[a-zA-Z0-9\._-]+)+')
     
    match = pattern.match(url)
    if match:
        return True
    else:
        return False

def is_url_match_page(pre_url, url):
    if url.startswith('?') and 'page=' in url:
        return True
    else:
        return False 
    
def url_filter(pre_url, url_list):
    urls = []
    for url in url_list:
        if not url:
            continue
        if url.startswith(config.url_head):
            new_url = url[len(config.url_head):]
            urls.append(new_url)
        elif is_url_match(url):
            urls.append(url)
        elif is_url_match_page(pre_url, url):
            new_url = '%s%s' % (pre_url,url)
            urls.append(url)

    return urls







