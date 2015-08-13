# coding: utf-8


import json
from urllib import urlencode
from urllib2 import urlopen


HOST = "http://eutils.ncbi.nlm.nih.gov"
SEARCH_URL = "{0}/entrez/eutils/esearch.fcgi/".format(HOST)
SUMMARY_URL = "{0}/entrez/eutils/esummary.fcgi".format(HOST)


def NCBISearch(**kwargs):

    search_args = {
            'db': kwargs.get("db", "pubmed"),
            'term': kwargs.get("term", 'PD1'),
            'retstart': kwargs.get("retstart", 0),
            'retmode': 'json',
            'sort': kwargs.get('sort', 'pub+date'),
            }
    try:
        data = urlopen(SEARCH_URL, urlencode(search_args)).read()
        data = json.loads(data)
    except:
        data = {}

    return data

def NCBISummary(**kwargs):
    search_args = {
            'db': kwargs.get("db", "pubmed"),
            'id': kwargs.get("id", ''),
            'retmode': 'json',
            }
    try:
        data = urlopen(SUMMARY_URL, urlencode(search_args)).read()
        data = json.loads(data)
    except:
        data = {}
    return data
