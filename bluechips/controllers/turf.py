"""
Handle turfjes
"""

import logging

from datetime import date

from bluechips.lib.base import *

from pylons import request, app_globals as g
from pylons.decorators import validate
from pylons.decorators.secure import authenticate_form
from pylons.controllers.util import abort

from formencode import Schema, validators

from mailer import Message

log = logging.getLogger(__name__)


class TurfController(BaseController):
    def index(self):
       return self.overview()
    
    def overview(self):
       c.turfEntries = meta.Session.query(model.TurfEntry).\
           filter(model.TurfEntry.user == request.environ['user']).\
           limit(10).all();
       return render('/turf/index.mako')
    
