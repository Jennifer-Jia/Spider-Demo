# -*- coding: utf-8 -*-

import gevent
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
from gevent import Timeout
import logging  
import logging.config 
import sys
import getopt
import time
import random
import requests
import config
from http_helper import http_get, load_cookies
from parser import parser as parser_text
from recoder import (add_url_new, add_url_done, get_url_new, 
                move_doing2new, all_url_doing, clean_record)


logging.config.fileConfig('logging.conf')    
logger = logging.getLogger('main') 


POOL_SIZE = config.request_pool_size
pool = Pool(POOL_SIZE)


def load_page(url):
    """Load page, recoder url which is new found, recoder url which is done
    """
    timeout = Timeout(random.uniform(30,40))
    timeout.start()
    try:
        r, status_code = http_get(url)
        if status_code == 302:
            add_url_done(url)
            return
        elif status_code != 200:
            logger.info('[url] %s, [status_code] %s' % (url, status_code))
            add_url_done(url)
            return

        data = r.text  
    except Timeout, e:
        is_retry = move_doing2new(url)
        if not is_retry:
            logger.info('[url] %s, [err_last_retry] %s' % (url, e))
        else:
            logger.info('[url] %s, [err_retry] %s' % (url, e))
        timeout.cancel()
        return
    except Exception, e:
        is_retry = move_doing2new(url)
        if not is_retry:
            logger.info('[url] %s [err_last_retry] %s' % (url, e))
        else:
            logger.info('[url] %s [err_retry] %s' % (url, e))
        timeout.cancel()
        return
    finally:
        timeout.cancel()


    new_urls = parser_text(url, data)
    add_url_new(new_urls)
    add_url_done(url)

def run():
    n = 0
    s = time.time()

    url_doing = all_url_doing()
    if not url_doing:
        load_page(config.start_url)
    else:
        print n, time.time() - s
        n += len(url_doing)
        for url in url_doing:
            pool.spawn(load_page, url)


    while 1:
        is_end = True
        for node in config.node_list:
            new_urls = get_url_new(node=node, num=POOL_SIZE*10)
            print n, time.time() - s
            n += len(new_urls)
            if len(new_urls) != 0:
                is_end = False
                for url in new_urls:
                    pool.spawn(load_page, url)

        if is_end:
            break

def usage():
    print """options:  
      -h                show this help message and exit  
      --clear-url       clear url record befor crawl
      --mv              set mv
    """

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['clear-url', 'mv='])
    clear_url = False
    mv = None
    for op, value in opts:
        if op == '--clear-url':
            clear_url = True
        elif op == '--mv':
            mv = value
        elif op == '-h':
            usage()
            sys.exit()

    if clear_url:
        clean_record()

    if mv:
        load_cookies('%s?mv=%s' % (config.start_url, mv))

    run()


