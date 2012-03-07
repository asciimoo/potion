POTION
======

### Description

Potion (aka f33dme-ng) is a flask+sqlalchemy based feed/item reader.

### Dependencies

*   2.5 <= python < 3
*   python-flask
*   python-sqlalchemy
*   python-feedparser

### Installation

1.  install dependencies
2.  copy potionrc_sample to .potionrc or /etc/potion.cfg and edit it
3.  run `PYTHONPATH=$(pwd) python potion/models.py` to init db
4.  run `PYTHONPATH=$(pwd) python potion/webapp.py` to start the application

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

