# Spider-Demo
A web spider to check page availability

You need use redis to record url. The setting of redis in config.py.

In config.py you can set parameter.

options:  
      -h                show this help message and exit  
      --clear-url       clear url record befor crawl
      --mv              set mv

example：
      python spider.py
      python spider.py --clear-url       
      python spider.py --mv 2
