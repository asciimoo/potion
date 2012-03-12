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

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime, Boolean, PickleType
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pickle import dumps, loads
from potion.common import cfg

engine = create_engine(cfg.get('database', 'connection'))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.metadata.bind = engine
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users'
    user_id       = Column(Integer, primary_key=True)
    name          = Column(String(511))
    password      = Column(String(511))
    is_active     = Column(Boolean)

class Query(Base):
    __tablename__ = 'queries'
    query_id      = Column(Integer, primary_key=True)
    query_string  = Column(String(8191))
    name          = Column(String(511))
    counter       = Column(Integer)
    user_id       = Column(Integer, ForeignKey('users.user_id'))
    user          = relationship('User',
                        backref=backref('queries', lazy='dynamic'))

    def __init__(self, query_string, name='', user_id=0):
        self.query_string   = query_string
        self.name           = name
        self.user_id        = user_id
        self.counter        = 1

    def __repr__(self):
        return '[%s] \'%s\'(%d)' % (self.name, self.query_string, self.user_id)



class Source(Base):
    __tablename__ = 'sources'
    source_id     = Column(Integer, primary_key=True)
    name          = Column(String(511), unique=True)
    address       = Column(Text(), unique=True)
    is_public     = Column(Boolean)
    source_type   = Column(String(63))
    updated       = Column(DateTime)
    modified      = Column(DateTime)
    user_id       = Column(Integer, ForeignKey('users.user_id'))
    user          = relationship('User',
                        backref=backref('sources', lazy='dynamic'))
    attributes    = Column(PickleType(comparator=dict.__eq__))

    def __init__(self, name, source_type, address, is_public=True, attributes={}):
        self.name           = name
        self.address        = address
        self.source_type    = source_type
        self.updated        = datetime(1970, 1, 1)
        self.is_public      = is_public
        self.attributes     = attributes

    def getAttrs(self):
        return loads(self.attributes)

    def setAttrs(self, attrs, replace=False):
        if replace:
            self.attributes = dumps(attrs)
            return
        a = loads(self.attributes)
        a.update(attrs)
        self.attributes = dumps(a)

    def __repr__(self):
        return '[S(Pub:%s)] %s %r %s\n' % (str(self.is_public), self.name, self.attributes, self.address)

class Item(Base):
    __tablename__ = 'items'
    item_id       = Column(Integer, primary_key=True)
    source_id     = Column(Integer, ForeignKey('sources.source_id'))
    source        = relationship('Source',
                      backref=backref('items', lazy='dynamic'))
    parent_id     = Column(Integer, ForeignKey('items.item_id'))
    added         = Column(DateTime())
    name          = Column(String(1023))
    content       = Column(Text)
    url           = Column(Text)
    archived      = Column(Boolean)
    attributes    = Column(PickleType(comparator=dict.__eq__))

    def __init__(self, name, content, url='', attributes={}):
        self.name           = name
        self.content        = content
        self.added          = datetime.now()
        self.archived       = False
        self.url            = url
        self.attributes     = attributes

    def __repr__(self):
        return '[I] %r' % (self.name)

    @staticmethod
    def toJSON(item):
        return {'name'          : item.name
               ,'id'            : item.item_id
               ,'content'       : item.content
               ,'date'          : item.date.strftime('%Y.%m.%d %H:%M:%S')
               ,'source_name'   : item.source.name
               ,'source_id'     : item.source_id
               }


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    if 0:
        a = Source('dnet blog',     'feed','http://techblog.vsza.hu/atom.xml',        attributes={'etag': 'lipsum'})
        b = Source('stef blog',     'feed','http://www.ctrlc.hu/~stef/blog/atom.xml', attributes={'etag': 'lipsum'})
        c = Source('xkcd',          'feed','http://xkcd.com/rss.xml')
        d = Source('lo0 secblog',   'feed','http://www.lo0.ro/feed/')
        e = Source('buherablog',    'feed','http://buhera.blog.hu/rss')
        db_session.add(a)
        db_session.add(b)
        db_session.add(c)
        db_session.add(d)
        db_session.add(e)
        db_session.commit()
        print Source.query.all()
