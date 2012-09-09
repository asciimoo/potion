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


from potion.models import db_session, Source, Item

def add(source_name, item_name, content, url=None, attributes=None):
    if not attributes: attributes = {}
    source = db_session.query(Source).filter(Source.name==source_name).first() or Source(name=source_name, source_type='cmdline', address='/query/_%s' % source_name)
    item = Item(item_name, content, url=url, attributes=attributes)
    db_session.add(source)
    source.items.append(item)
    db_session.commit()
    return item

def argparser():
    import argparse
    argp = argparse.ArgumentParser(description='potion command line item creator')
    argp.add_argument('-s', '--source-name'
                     ,help      = 'source name'
                     ,metavar   = 'SOURCE'
                     ,action    = 'store'
                     ,type      = str
                     )
    argp.add_argument('-n', '--item-name'
                     ,metavar   = 'ITEM'
                     ,help      = 'item name'
                     ,action    = 'store'
                     ,type      = str
                     )
    argp.add_argument('-c', '--content'
                     ,metavar   = 'CONTENT'
                     ,help      = 'content string'
                     ,action    = 'store'
                     ,type      = str
                     )
    argp.add_argument('-u', '--url'
                     ,metavar   = 'URL'
                     ,help      = 'url of item - default is ""'
                     ,default   = ''
                     ,action    = 'store'
                     ,type      = str
                     )
    return vars(argp.parse_args())

def main():
    args = argparser()
    if not args.get('source_name') or not args.get('item_name') or not args.get('content'):
        from sys import exit, stderr
        stderr.write('[!] missing arguments\n')
        exit(0)
    return add(**args)


if __name__ == '__main__':
    main()
