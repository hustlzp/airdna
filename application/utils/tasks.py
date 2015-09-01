# coding: utf-8

import os
import requests
import re
import subprocess
import celery
from tempfile import TemporaryFile
#from celery import Celery

from ..utils import cache

#celery = make_celery()

@celery.task()
def download_pdf_from_ncbi(dbname, uid):

    url = "http://www.ncbi.nlm.nih.gov/pmc/articles/PMC{0}/".format(uid)
    path = 'uploads/ncbi/{0}/{1}/'.format(dbname, uid)
    if not os.path.exists(path):
        os.makedirs(path)
    html_path = "{0}{1}".format(path, '1.html')
    pdf_path = "{0}{1}".format(path, '1.pdf')
    #if os.path.exists(html_path):
        #return open(html_path).read()
    #if not os.path.exists(pdf_path):
    s = requests.session()
    html = s.get(url).content
    try:
        url = re.findall(r'<link\s*rel=\"alternate\"\s*type=\"application/pdf\".*href=\"(?P<url>.+?)\".*/>', html)[0]
        if not url.startswith("http"):
            url = "http://www.ncbi.nlm.nih.gov" + url
        pdf = s.get(url).content
        f = open(pdf_path, 'w')
        f.write(pdf)
        f.close()
        print "download_pdf_from_ncbi succee"
    except Exception, e:
        print str(e)
        cache.cache.set('ncbi_%s_%s_pdf' % (dbname, uid), None)
        return False

    temp = TemporaryFile()
    temp.seek(0)
    temp.write(pdf)
    temp.seek(0)
    res = TemporaryFile()
    p = subprocess.Popen(['pdf2htmlEX', '/dev/stdin', html_path], stdin = temp ,stdout = res, stderr = subprocess.PIPE, shell = False)
    p.wait()
    res.seek(0)
    cache.cache.set('ncbi_%s_%s_pdf' % (dbname, uid), None)
    return True
