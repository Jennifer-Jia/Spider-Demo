# -*- coding: utf-8 -*-
import hashlib
import redis
import config


c_pool = redis.ConnectionPool(host=config.redis_host, 
                                port=config.redis_port, 
                                db=config.redis_db)
redis_db = redis.Redis(connection_pool=c_pool)

url_new_key = 'url_new_%d'
url_doing_key = 'url_doing_%d'
url_done_key = 'url_done_%d'
err_retry_count = 'err_retry_count_%d'

connect = {
            0: redis_db,
            1: redis_db,
            2: redis_db,
            3: redis_db,
            4: redis_db,
            5: redis_db,
            6: redis_db,
            7: redis_db,
        }


def get_redis_db(node):
    """Get redis node instance.
    Args:
        node: The number of node.
    Returns:
        A redis instance
    """
    return connect[node]

def get_node(url):
    """Transform url to node number.
    Args:
        url: A url need check.
    Returns:
        The number of node.
    """
    m = hashlib.md5()
    m.update(url)
    return long(m.hexdigest(), 16) % config.hash_mod

def generate_key(key, url=None, node=None):
    assert url != None or node != None
    if node == None:
        node = get_node(url)
    return key % node

def add_url_new(urls):
    """Record url when found new url.
    Args:
        urls: It is a list, the item is url.
    """
    if not urls:
        return

    url_dict = {}
    for url in urls:
        node = get_node(url)
        if node not in url_dict:
            url_dict[node] = [url]
        else:
            url_dict[node].append(url)

    for node, urls in url_dict.iteritems():
        p = get_redis_db(node).pipeline()
        for url in urls:
            p.sismember(generate_key(url_done_key, node=node), url)
        r = p.execute()
        new_urls = [urls[index] for index, v in enumerate(r) if not v]
        if new_urls:
            get_redis_db(node).sadd(generate_key(url_new_key, node=node), *new_urls)

def add_url_done(url):
    """Record the url is checked.
    """
    node = get_node(url)
    get_redis_db(node).smove(generate_key(url_doing_key, node=node), 
                            generate_key(url_done_key, node=node), 
                            url)

def get_url_new(node=0, num=1):
    """Record the url is checked.
    Args:
        node: The number of node.
        num: The number of url that want get.
    Returns:
        It is a list, the item is url.
    """
    max_len = get_redis_db(node).scard(generate_key(url_new_key, node=node))
    get_len = min(max_len, num)
    urls = get_redis_db(node).srandmember(generate_key(url_new_key, node=node), get_len)
    if not urls:
        return []

    p = get_redis_db(node).pipeline()
    for url in urls:
        if not url:
            continue

        p.smove(generate_key(url_new_key, node=node), 
                generate_key(url_doing_key, node=node), 
                url)
    p.execute()
    return urls

def move_doing2new(url):
    """Record the url which is need to retry.
    Returns:
        Is url need retry. True - need; False - not need.
    """

    node = get_node(url)
    retry_count = get_redis_db(node).hincrby(generate_key(err_retry_count, node=node), url, 1)
    if retry_count <= 3:
        get_redis_db(node).smove(url_doing_key, url_new_key, url)
        return True
    else:
        p = get_redis_db(node).pipeline()
        p.smove(generate_key(url_doing_key, node=node),
                generate_key(url_done_key, node=node), 
                url)
        p.hdel(generate_key(err_retry_count, node=node), url)
        p.execute()
        return False

def all_url_doing():
    """Load all url which is in checking. 
    Returns:
        It is a list, the item is url.
    """
    all_url = set([])
    for node in config.node_list:
        all_url = all_url | get_redis_db(node).smembers(generate_key(url_doing_key, node=node))

    return list(all_url)

def clean_record():
    redis_db.flushdb()




