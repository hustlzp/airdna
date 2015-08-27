# coding: utf-8


import json
from urllib import urlencode
from urllib2 import urlopen

from flask import render_template, Blueprint, request
from flask.ext.sqlalchemy import Pagination
from ..utils.ncbi import NCBISearch, NCBIFetch

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
        #data = urlopen(SUMMARY_URL, urlencode({"db": kwargs.get("db", "pubmed"), "id": ulist, 'retmode': 'json'})).read()
        result["data"] = NCBIFetch(**{"db": kwargs.get("db", "pmc"), "id": ulist})
        #for x in data["result"]["uids"]:
            #x = data["result"][x]
            #result["data"].append({
                #"uid": x["uid"],
                #"pub_date": x["epubdate"],
                #"author": x["authors"][0]["name"],
                #"title": x["title"],
                #"pub_journal": x["fulljournalname"],
                #"pub_page": x["elocationid"],
                #'db_name': kwargs.get("db", "pubmed"),
                #})
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
    return render_template("site/searchNCBI.html", data = data)
