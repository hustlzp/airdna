# coding: utf-8


#import json
#from urllib import urlencode
#from urllib2 import urlopen

from flask import render_template, Blueprint, request, g
from flask.ext.sqlalchemy import Pagination
from ..utils.ncbi import NCBISearch, NCBIFetch
from ..utils import cache
from ..utils.cache import CACHE_USER_SEARCH_DICT, CACHE_KEYS_ALL, CACHE_KEY_USER,\
        CACHE_USER_SEARCH_LIST


bp = Blueprint('search', __name__)


def handle(**kwargs):

    HOST = "http://eutils.ncbi.nlm.nih.gov"
    SEARCH_URL = "{0}/entrez/eutils/esearch.fcgi/".format(HOST)
    SUMMARY_URL = "{0}/entrez/eutils/esummary.fcgi".format(HOST)

    search_args = {
            'db': kwargs.get("db", "pmc"),
            'term': kwargs.get("term", 'PD1'),
            'retstart': (int(kwargs.get("page", 1)) - 1) * 10,
            'retmax': '10',
            'retmode': 'json',
            'sort': 'pub+date',
            }
    result = {"data": [], "totalCount": 0, "retstart": 0, "retmax": 10}
    try:
        data = NCBISearch(**search_args)
        result["totalCount"] = int(data["esearchresult"]["count"])
        result["retstart"] = int(data["esearchresult"]["retstart"])
        result["retmax"] = 10
        ulist = ",".join(data["esearchresult"]["idlist"])
        result["data"] = NCBIFetch(**{"db": kwargs.get("db", "pmc"), "id": ulist})
    except:
        pass
    return Pagination(None, int(kwargs.get("page", 0)), 10, result["totalCount"], result["data"])
    

@bp.route('/search/', methods=['GET'])
def search():

    search_args = {
            'db': request.args.get("db", "pubmed"),
            'term': request.args.get("query", 'PD1'),
            'retstart': request.args.get("retstart", 0),
            'retmode': 'json',
            'page': request.args.get("page", 1),
            }
    data = handle(**search_args)
    if g.user:
        mc = cache.cache
        term = search_args["term"]
        mc.sadd(CACHE_KEYS_ALL, term)
        mc.sadd(CACHE_KEY_USER.format(key = term), g.user.id)
        mc.hset(CACHE_USER_SEARCH_LIST.format(user = g.user.id), term, 0)

        if int(search_args["page"]) == 1:
            uid = [x["uid"] for x in data.items]
            mc.hset(CACHE_USER_SEARCH_DICT.format(user = g.user.id), term, set(uid))

    return render_template("site/searchNCBI.html", data = data)
