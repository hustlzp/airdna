# coding: utf-8

import redis
from flask.ext.cache import Cache


CACHE_USER_SEARCH_DICT = "search_{user}_result"  #记录每个用户搜索过的关键字，搜到的结果
CACHE_USER_SEARCH_LIST = "search_{user}_list"  #记录每个用户搜索过的关键字
CACHE_KEYS_ALL = "search_all"   #记录所有用户搜索过的关键字
CACHE_KEY_USER = "search_{key}" #记录搜过此关键字的用户



cache = {}

def init_cache(app):
    global cache
    cache = redis.Redis()
    #if app.production: 
        ##cache = Cache(app,config={'CACHE_TYPE': 'memcached', 'CACHE_MEMCACHED_SERVERS': app.config.get('CACHE_MEMCACHED_SERVERS', ['127.0.0.1:11211'])})
        #cache = redis.Redis()
    #else:
        ##cache = Cache(app, config = {'CACHE_TYPE': 'simple'})
        #cache = Cache(app,config={'CACHE_TYPE': 'memcached', 'CACHE_MEMCACHED_SERVERS': app.config.get('CACHE_MEMCACHED_SERVERS', ['127.0.0.1:11211'])})
    return cache
