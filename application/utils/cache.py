# coding: utf-8

from flask.ext.cache import Cache

cache = {}

def init_cache(app):
    if app.production: 
        cache = Cache(app,config={'CACHE_TYPE': 'memcached', 'CACHE_MEMCACHED_SERVERS': app.config.get('CACHE_MEMCACHED_SERVERS', ['127.0.0.1:11211'])})
    else:
        cache = Cache(app, config = {'CACHE_TYPE': 'simple'})
    return cache
