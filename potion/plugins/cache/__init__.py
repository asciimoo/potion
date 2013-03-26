
from lxml.html import fragments_fromstring, tostring, HtmlElement
import urllib
from potion.common import cfg
from os.path import exists

def insert_item(item):
    """docstring for item_insert"""
    frag = fragments_fromstring(item.content)
    for e in frag:
        if not type(e) == HtmlElement:
            continue
        for i in e.xpath('//img'):
            f = '/'+i.attrib['src'].replace('http://', '').replace('/','_').split('?')[0]
            if exists(cfg.get('cache', 'dir')+f):
                continue
            try:
                urllib.urlretrieve(i.attrib['src'], cfg.get('cache', 'dir')+f)
                i.attrib['src'] = cfg.get('cache', 'url')+f
            except:
                # TODO
                pass

    c = ''
    for i in frag:
        if type(i) == HtmlElement:
            c += unicode(tostring(i))
        else:
            c += i

    item.content = c
    return item
