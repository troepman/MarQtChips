"""
Handle turfjes
"""

import logging

from datetime import date

from bluechips.lib.base import *
from bluechips.lib.permissions import BlueChipResident

from pylons import request, response, app_globals as g
from pylons.decorators import validate
from pylons.decorators.secure import authenticate_form
from pylons.controllers.util import abort
from authkit.authorize.pylons_adaptors import authorize

from formencode import Schema, validators

import webhelpers.paginate

import csv
from cStringIO import StringIO

log = logging.getLogger(__name__)


class TurfController(BaseController):
    def index(self):
       return self.overview()
    
    def overview(self):
       c.turfEntries = meta.Session.query(model.TurfEntry).\
           filter(model.TurfEntry.user == request.environ['user']).\
           order_by(model.TurfEntry.entered_time.desc()).limit(10).all();
       return render('/turf/index.mako')

    def history(self):
       p = 0
       own = 1
       if 'page' in request.params:
         p = int(request.params['page'])
       if 'own' in request.params:
         own = int(request.params['own'])

       c.own = own;

       if own == 1:
         c.turfEntries = webhelpers.paginate.Page(meta.Session.query(model.TurfEntry).\
         filter(model.TurfEntry.user == request.environ['user']).\
           order_by(model.TurfEntry.entered_time.desc()),\
           page = p,\
           items_per_page = 20,
           own = own)
       else:
         c.turfEntries = webhelpers.paginate.Page(meta.Session.query(model.TurfEntry).\
           order_by(model.TurfEntry.entered_time.desc()),\
           page = p,\
           items_per_page = 20,
           own = own)
       return render('/turf/history.mako')
    
    @authorize(BlueChipResident())
    def delete(self, id=None):
       if id is None:
         abort(404)
     
       meta.Session.delete(meta.Session.query(model.TurfEntry).get(id));
       meta.Session.commit();
      
       h.flash('Turf entry verwijderd');
       
       return h.redirect_to('/turf/history');    

    def export(self):

      turfEntries = meta.Session.query(model.TurfEntry).all();
      response.headers['Content-Type'] = 'text/csv'
      response.headers['Content-Disposition'] = 'attachment; filename=\"export.csv\"'
      s = StringIO()
      writer = csv.writer(s)
      writer.writerow(['datetime', 'user', 'subject']);
      for turfEntry in turfEntries:
        writer.writerow([turfEntry.entered_time, turfEntry.user.username, turfEntry.subject])
      return s.getvalue();    
