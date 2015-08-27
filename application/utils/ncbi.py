# coding: utf-8


import json
from urllib import urlencode
from urllib2 import urlopen
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


HOST = "http://eutils.ncbi.nlm.nih.gov"
SEARCH_URL = "{0}/entrez/eutils/esearch.fcgi/".format(HOST)
SUMMARY_URL = "{0}/entrez/eutils/esummary.fcgi".format(HOST)
FETCH_URL = "{0}/entrez/eutils/efetch.fcgi".format(HOST)


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
        data = []
    return data

def NCBIFetch(**kwargs):
    search_args = {
            'db': kwargs.get("db", "pubmed"),
            'id': kwargs.get("id", ''),
            'retmode': 'xml',
            }
    result = []
    try:
        data = urlopen(FETCH_URL, urlencode(search_args)).read()
        xmltree = ET.fromstring(data)
        for et in xmltree.findall("PubmedArticle"):
            try:
                temp = {
                    "title": et.find("MedlineCitation/Article/ArticleTitle").text,
                    "uid": et.find("MedlineCitation/PMID").text,
                    "author": "{0} {1}".format(et.find("MedlineCitation/Article/AuthorList/Author/LastName").text, et.find("MedlineCitation/Article/AuthorList/Author/Initials").text),
                    "pub_date": " ".join([x.text for x in et.find("MedlineCitation/Article/Journal/JournalIssue/PubDate").getchildren()]),
                    "pub_journal": et.find("MedlineCitation/Article/Journal/Title").text,
                    #"pub_journal": et.find("front/journal-meta/journal-title-group/journal-title").text,
                    "pub_page": getattr(et.find("MedlineCitation/Article/ELocationID"), "text", ""),
                    'db_name': kwargs.get("db", "pubmed"),
                    "abstract": "".join(["<p>%s</p>" % x.text for x in et.findall("MedlineCitation/Article/Abstract/AbstractText")]), 
                    }
                try:
                    pmcid = et.find("PubmedData/ArticleIdList/ArticleId[@IdType='pmc']").text
                    temp["in_pmc"] = True
                    temp["pmc_uid"] = pmcid[3:]
                except:
                    temp["in_pmc"] = False
                    pass
                result.append(temp)
            except Exception, e:
                print str(e)
                continue
    except Exception, e:
        print str(e)
        pass
    return result
