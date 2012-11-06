#!/usr/bin/env python

# this file is part of potion.
#
#  potion is free software: you can redistribute it and/or modify
#  it under the terms of the gnu affero general public license as published by
#  the free software foundation, either version 3 of the license, or
#  (at your option) any later version.
#
#  potion is distributed in the hope that it will be useful,
#  but without any warranty; without even the implied warranty of
#  merchantability or fitness for a particular purpose.  see the
#  gnu affero general public license for more details.
#
#  you should have received a copy of the gnu affero general public license
#  along with potion. if not, see <http://www.gnu.org/licenses/>.
#
# (c) 2012- by adam tauber, <asciimoo@gmail.com>


from sys import path
from os.path import realpath, dirname
path.append(realpath(dirname(realpath(__file__))+'/../../'))

import re

from feedparser import parse
from datetime import datetime
from urlparse import urlparse, urlunparse
from itertools import ifilterfalse, imap
import urllib
import urllib2
import httplib
from lxml import etree
from io import StringIO

from potion.common import cfg
from potion.models import db_session, Source, Item
from potion import proxy

user_agent = cfg.get('fetcher', 'user_agent')

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', user_agent)]

# removes annoying UTM params to urls.
utmRe=re.compile('utm_(source|medium|campaign|content)=')
def urlSanitize(url):
    # handle any redirected urls from the feed, like
    # ('http://feedproxy.google.com/~r/Torrentfreak/~3/8UY1UySQe1k/')
    us=httplib.urlsplit(url)
    if us.scheme=='http':
        conn = httplib.HTTPConnection(us.netloc, timeout=3)
        req = urllib.quote(url[7+len(us.netloc):])
    elif us.scheme=='https':
        conn = httplib.HTTPSConnection(us.netloc)
        req = urllib.quote(url[8+len(us.netloc):])
    #conn.set_debuglevel(9)
    headers={'User-Agent': user_agent}
    conn.request("HEAD", req,None,headers)
    res = conn.getresponse()
    conn.close()
    if res.status in [301, 304]:
        url = res.getheader('Location')
    # removes annoying UTM params to urls.
    pcs=urlparse(urllib.unquote_plus(url))
    tmp=list(pcs)
    tmp[4]='&'.join(ifilterfalse(utmRe.match, pcs.query.split('&')))
    return urlunparse(tmp).decode('utf-8')

def fetchFeed(url):
    try:
        return opener.open(url, timeout=5)
    except:
        print '[EE] cannot fetch %s' % url
        return ''


def parseFeed(feed):
    counter = 0
    #modified = feed['modified'].timetuple() if feed.get('modified') else None
    f = None
    f = parse(fetchFeed(feed.address)
             ,etag      = feed.attributes.get('etag')
             ,modified  = feed.attributes.get('modified')
             )
    if not f:
        print '[EE] cannot parse %s - %s' % (feed.name, feed.address)
        return counter
    #print '[!] parsing %s - %s' % (feed.name, feed.url)
    try:
        if feed.attributes['etag'] != f.etag:
            return
    except KeyError:
        pass

    try:
        feed.attributes['etag'] = f.etag
    except AttributeError:
        pass

    try:
        feed.attributes['modified'] = f.modified
    except AttributeError:
        pass

    d = feed.updated
    for item in reversed(f['entries']):
        if 'links' in item:
            original_url = unicode(item['links'][0]['href'])
        else:
            original_url = unicode(item['link'])

        # checking duplications
        if db_session.query(Item). \
                filter(Item.source_id==feed.source_id). \
                filter(Item.original_url==original_url).first():
            continue

        try:
           u = urlSanitize(original_url)
        except:
           u = ''

        try:
            tmp_date = datetime(*item['updated_parsed'][:6])
        except:
            tmp_date = datetime.now()

        # title content updated
        try:
            c = ''.join([x.value for x in item.content])

        except:
            c = u'[EE] No content found, plz check the feed (%s) and fix me' % feed.name
            for key in ['media_text', 'summary', 'description', 'media:description']:
                if item.has_key(key):
                    c = item[key]
                    break

        #fixing malformed html
        html=etree.parse(StringIO(c), etree.HTMLParser(recover=True, remove_blank_text=True))
        c=''
        for e in html.xpath('//body/*'):
            c+=etree.tostring(e)

        t = item.get('title','[EE] Notitle')

        # date as tmp_date?!
        feed.items.append(Item(t, c, original_url, url=u, attributes={'date':tmp_date}))
        db_session.commit()
        counter += 1
    feed.updated = d
    db_session.commit()
    #feed.save()
    return counter

if __name__ == '__main__':
    counter = sum(imap(parseFeed, Source.query.filter(Source.source_type=='feed').all()))
    print '[!] %d item added' % counter
