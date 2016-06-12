# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
from url_filter import url_filter


class TagAHTMLParser(HTMLParser):  

    def __init__(self):   
        HTMLParser.__init__(self)   
        self.links = []   

    def handle_starttag(self, tag, attrs):   
        if tag == "a":   
            if len(attrs) == 0:   
                pass   
            else:   
                for (variable, value) in attrs:   
                    if variable == "href":   
                        self.links.append(value)   

          
def parser(url, html_code):
    """Parse html code, draw out url.
    Args:
        url: A url checked.
        html_code: Html code.
    Returns:
        parsed url.
    """
    hp = TagAHTMLParser()
    hp.feed(html_code)   
    hp.close()
    new_urls = url_filter(url, hp.links)
    new_urls = [u.encode('utf8') for u in new_urls]
    return new_urls







