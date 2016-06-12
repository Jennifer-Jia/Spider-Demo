# Spider-Demo
A web spider to check page availability

You need use redis to record url. The setting of redis in config.py.

In config.py you can set parameter.

options:  
      -h                show this help message and exit  <br/>
      --clear-url       clear url record befor crawl<br/>
      --mv              set mv<br/>

example:  
      python spider.py<br/>
      python spider.py --clear-url  <br/>
      python spider.py --mv 2<br/>
