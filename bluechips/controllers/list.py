""" Handle shopping list page """

import logging

from datetime import date, datetime

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

class ListEntrySchema(AuthFormSchema):
    "Check new entry."
    allow_extra_field=False
    subject=validators.String()

class ListController(BaseController):
    def index(self):
       return self.overview()
    
    def overview(self):
       items = meta.Session.query(model.ListEntry).filter(model.listEntries.c.checker_id==None).\
           order_by(model.ListEntry.createdTime.desc()).all();
       if (len(items) < 20): # fill a bit
         items_extra = meta.Session.query(model.ListEntry).filter(model.listEntries.c.checker_id.isnot(None)).\
           order_by(model.ListEntry.createdTime.desc()).all()[:20-len(items)];
         items.extend(items_extra);
      
       c.listEntries = items;

       return render('/list/index.mako')

    @authorize(BlueChipResident())
    @validate(schema=ListEntrySchema(), form='index')
    @authenticate_form
    def add(self):
       le = model.ListEntry()
       le.subject = self.form_result['subject'];
       le.creater = request.environ['user'];
 #      print(le);

       meta.Session.add(le);
       meta.Session.commit();

       return h.redirect_to('/list');

    @authorize(BlueChipResident())
    def check(self, id):
     
       if (id==None):
         return abort(404);

       entry = meta.Session.query(model.ListEntry).get(id);      
       entry.checker = request.environ['user'];
       entry.checkedTime = datetime.utcnow();
#       print(entry);
      
       meta.Session.commit();

       return h.redirect_to('/list');    

    @authorize(BlueChipResident())
    def uncheck(self, id):
       if (id==None):
         return abort(404);
        
       entry = meta.Session.query(model.ListEntry).get(id);
       entry.checker = None;
        
       meta.Session.commit();

       return h.redirect_to('/list');
