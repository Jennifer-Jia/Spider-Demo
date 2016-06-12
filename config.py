# -*- coding: utf-8 -*-
request_pool_size = 5

# request
start_url = '/'
allowed_domains = 'm.sohu.com'
url_head = 'http://' + allowed_domains
url_404 = 'http://m.sohu.com/404_2.html'
request_timeout = 10

# redis
redis_host = 'localhost'
redis_port = 6379
redis_db = 0

# recorder
hash_mod = 7
node_list = range(hash_mod)
