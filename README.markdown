POTION
======

### Description

Potion (aka f33dme-ng) is a flask+sqlalchemy based feed/item reader.

### Dependencies

*   2.5 <= python < 3
*   python-sqlalchemy
*   python-feedparser
*   python-flask
*   flask-wtf
*   python-opml (optional)

### Installation

1.  install dependencies (`easy_install sqlalchemy feedparser flask flask-wtf opml`)
2.  clone source: `git clone git@github.com:asciimoo/potion.git && cd potion`
3.  copy potionrc_sample to ./.potionrc or ~/.potionrc or /etc/potion.cfg: `cp potionrc_sample ~/.potionrc`
4.  edit your config (set your secret_key!)
5.  run `PYTHONPATH=$(pwd) python potion/models.py` to init db
6.  run `PYTHONPATH=$(pwd) python potion/webapp.py` to start the application

### Usage

*   run `PYTHONPATH=$(pwd) python potion/sources/feed.py` to fetch new feed items

### License

potion is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

potion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with potion. If not, see < http://www.gnu.org/licenses/ >.

(C) 2012- by Adam Tauber, <asciimoo@gmail.com>

