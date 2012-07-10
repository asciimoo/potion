#!/usr/bin/env python

# This file is part of potion.
#
#  potion is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  potion is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with potion. If not, see <http://www.gnu.org/licenses/>.
#
# (C) 2012- by Adam Tauber, <asciimoo@gmail.com>

from flask import Flask, request, render_template, redirect, flash
from potion.models import db_session, Item, Source, Query
from potion.common import cfg
from flask.ext.wtf import Form, TextField, Required, SubmitField
from potion.helpers import Pagination


menu_items  = (('/'                 , 'home')
              ,('/doc'              , 'documentation')
              ,('/sources'          , 'sources')
              ,('/queries'          , 'queries')
              ,('/top'              , 'top '+cfg.get('app', 'items_per_page'))
              ,('/all'              , 'all')
              )

app = Flask(__name__)
app.secret_key = cfg.get('app', 'secret_key')

class SourceForm(Form):
    #name, address, source_type, is_public=True, attributes={}
    name                    = TextField('Name'      , [Required()])
    source_type             = TextField('Type'      , [Required()])
    address                 = TextField('Address'   , [Required()])
    submit                  = SubmitField('Submit'  , [Required()])


@app.context_processor
def contex():
    global menu_items, cfg, query
    return {'menu'              : menu_items
           ,'cfg'               : cfg
           ,'query'             : ''
           ,'path'              : request.path
           ,'menu_path'         : request.path
           ,'unarchived_count'  : Item.query.filter(Item.archived==False).count()
           ,'item_count'        : Item.query.count()
           }

def parse_query(q):
    return q.get('query')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'
                          ,sources  = Source.query.all()
                          )

def get_unarchived_ids(items):
    return [item.item_id for item in items if item.archived == False]

@app.route('/doc', methods=['GET'])
def doc():
    return 'TODO'

@app.route('/top', methods=['GET'])
@app.route('/top/<int:page_num>', methods=['GET'])
def top(page_num=0):
    limit = int(cfg.get('app', 'items_per_page'))
    offset = limit*page_num
    items = Item.query.filter(Item.archived==False).order_by(Item.added).limit(limit).offset(offset).all()
    pagination = Pagination(page_num, limit, Item.query.filter(Item.archived==False).count())
    return render_template('flat.html'
                          ,items        = items
                          ,pagination   = pagination
                          ,unarchiveds  = get_unarchived_ids(items)
                          ,menu_path    = '/top' #preserve menu highlight when paging
                          )

@app.route('/sources', methods=['GET', 'POST'])
def sources():
    form = SourceForm(request.form)
    if request.method == 'POST' and form.validate():
        s = Source(form.name.data, form.source_type.data, form.address.data)
        db_session.add(s)
        db_session.commit()
        flash('Source "%s" added' % form.name.data)
        return redirect(request.referrer or '/')
    return render_template('sources.html'
                          ,form     = form
                          ,sources  = Source.query.all()
                          ,mode     = 'add'
                          )

@app.route('/sources/<int:s_id>', methods=['GET', 'POST'])
def source_modify(s_id=0):
    source=Source.query.get(s_id)
    form=SourceForm(obj=source)
    if request.method == 'POST' and form.validate():
        source.name=form.name.data
        source.source_type=form.source_type.data
        source.address=form.address.data
        db_session.add(source)
        db_session.commit()
        flash('Source "%s" modified' % form.name.data)
        return redirect('/sources')
    return render_template('sources.html'
                          ,form     = form
                          ,sources  = Source.query.all()
                          ,mode     = 'modify'
                          ,menu_path= '/sources' #preserve menu highlight when paging
                          )

@app.route('/sources/delete/<int:s_id>', methods=['GET'])
def del_source(s_id):
    Source.query.filter(Source.source_id==s_id).delete()
    flash('Source removed')
    return redirect(request.referrer or '/')

@app.route('/all')
def all():
    items = Item.query.all()
    return render_template('flat.html'
                          ,items        = items
                          ,unarchiveds  = get_unarchived_ids(items)
                          )

@app.route('/queries', methods=['GET'])
def queries():
    items = []
    return render_template('queries.html'
                          ,queries      = Query.query.all()
                          ,items        = items
                          )

@app.route('/query', methods=['POST'])
def query_redirect():
    q_str = request.form.get('query')
    return redirect('/query/'+q_str)

@app.route('/query/<path:q_str>', methods=['GET'])
def do_query(q_str):
    return 'TODO ' + q_str

@app.route('/archive', methods=['POST'])
@app.route('/archive/<int:id>', methods=['GET'])
def archive(id=0):
    if request.method=='POST':
        try:
            ids = map(int, request.form.get('ids', '').split(','))
        except:
            flash('Bad params')
            return redirect(request.referrer or '/')
    elif id==0:
        flash('Nothing to archive')
        return redirect(request.referrer or '/')
    else:
        ids=[id]
    db_session.query(Item).filter(Item.item_id.in_(ids)).update({Item.archived: True}, synchronize_session='fetch')
    db_session.commit()
    flash('Successfully archived items: %d' % len(ids))
    return redirect(request.referrer or '/')

@app.route('/opml', methods=('GET',))
def opml():
    return render_template('opml.xml'
                           ,sources = Source.query.filter(Source.source_type=='feed').all()
                           )

@app.route('/opml/import', methods=['GET'])
def opml_import():
    url = request.args.get('url')
    if not url:
        return 'Missing url'
    import opml
    try:
        o = opml.parse(url)
    except:
        return 'Cannot parse opml file %s' % url

    def import_outline_element(o):
        for f in o:
            if hasattr(f,'xmlUrl'):
                s = Source(f.title,'feed',f.xmlUrl)
                db_session.add(s)
            else:
                import_outline_element(f)

    import_outline_element(o) 
    db_session.commit()
    flash('import successed')
    return redirect(request.referrer or '/')


if __name__ == "__main__":
    app.run(debug        = cfg.get('server', 'debug')
           ,use_debugger = cfg.get('server', 'debug')
           ,port         = int(cfg.get('server', 'port'))
           )
