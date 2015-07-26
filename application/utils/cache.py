# coding: utf-8

from flask.ext.cache import Cache

cache = {}

def init_cache(app):
    cache = Cache(app,config={'CACHE_TYPE': 'simple'})
    return cache
