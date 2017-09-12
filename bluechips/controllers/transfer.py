"""
Handle transfers
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


class TransferSchema(AuthFormSchema):
    "Validate a transfer."
    allow_extra_fields = False
    debtor_id = validators.Int(not_empty=True)
    creditor_id = validators.Int(not_empty=True)
    amount = model.types.CurrencyValidator(not_empty=True)
    description = validators.UnicodeString()
    date = validators.DateConverter()
 

class TransferController(BaseController):
    def index(self):
       return self.edit()
    
    def edit(self, id=None):
        c.users = get_users()
        if id is None:
            c.title = 'Add a New Transfer'
            c.transfer = model.Transfer()
            c.transfer.debtor_id = request.environ['user'].id
            c.transfer.date = date.today()
        else:
            c.title = 'Edit a Transfer'
            c.transfer = meta.Session.query(model.Transfer).get(id)
            if c.transfer is None:
                abort(404)
        return render('/transfer/index.mako')
    
    @redirect_on_get('edit')
    @validate(schema=TransferSchema(), form='edit')
    @authenticate_form
    def update(self, id=None):
        if id is None:
            t = model.Transfer()
            meta.Session.add(t)
            op = 'created'
        else:
            t = meta.Session.query(model.Transfer).get(id)
            if t is None:
                abort(404)
            op = 'updated'
        
        update_sar(t, self.form_result)
	with meta.Session.no_autoflush:
	    deb = meta.Session.query(model.User).get(t.debtor_id);
	    cred = meta.Session.query(model.User).get(t.creditor_id);
	    setattr(t, "debtor", deb);
	    setattr(t, "creditor", cred);
        meta.Session.commit()
       
        show = ('Transfer of %s from %s to %s %s.' %
                (t.amount, t.debtor, t.creditor, op))
        h.flash(show)

        # Send email notification to involved users if they have an email set.
        print("New transfer created")
        return h.redirect_to('/')

    def delete(self, id):
        c.title = 'Delete a Transfer'
        c.transfer = meta.Session.query(model.Transfer).get(id)
        if c.transfer is None:
            abort(404)

        return render('/transfer/delete.mako')

    @redirect_on_get('delete')
    @authenticate_form
    def destroy(self, id):
        t = meta.Session.query(model.Transfer).get(id)
        if t is None:
            abort(404)

        if 'delete' in request.params:
            meta.Session.delete(t)

            show = ("Transfer of %s from %s to %s deleted." %
                    (t.amount, t.debtor, t.creditor))
            h.flash(show)

            print("Transfer deleted")	    
	    meta.Session.commit();
        return h.redirect_to('/')
