"""
Calculate the current state of the books
"""

import logging

from bluechips.lib.base import *
from bluechips.lib.permissions import BlueChipResident

import sqlalchemy
from sqlalchemy import orm

from authkit.authorize.pylons_adaptors import authorize

from pylons import request
from pylons.decorators import validate
from pylons.decorators.secure import authenticate_form

from formencode import validators, Schema, FancyValidator, Invalid

log = logging.getLogger(__name__)


class EmailSchema(AuthFormSchema):
    "Validate email updates."
    allow_extra_fields = False
    new_email = validators.Email()


class UniqueUsername(FancyValidator):
    def _to_python(self, value, state):
        u = meta.Session.query(model.User).\
            filter(model.User.username == value).\
            first()
        if u:
            raise Invalid(
                'That username already exists',
                value, state)
        return value


class NewUserSchema(AuthFormSchema):
    "Validate new users."
    allow_extra_fields = False
    username = UniqueUsername(not_empty=True)
    password = validators.String(if_missing=None)
    confirm_password = validators.String(if_missing=None)
    name = validators.String(not_empty=False)
    resident = validators.StringBoolean(not_empty=True)
    chained_validators = [
        validators.FieldsMatch('password', 'confirm_password'),
        ]

class CardSchema(AuthFormSchema):
    "Validate card updates."
    allow_extra_field = False
    description = validators.String();


class UserController(BaseController):
    def index(self):
	d = meta.Session.query(model.Card).\
        filter(model.cards.c.user_id==request.environ['user'].id).\
        filter(model.cards.c.valid==1).all()
	#raise exception("Ij hoofd: " + str(d));
	c.cards = d;
        return render('/user/index.mako')

    def email(self):
        c.title = 'User Settings'
        return render('/user/email.mako')

    @validate(schema=EmailSchema(), form='index')
    @authenticate_form
    def update(self):
        new_email = self.form_result['new_email']
        request.environ['user'].email = new_email
        meta.Session.commit()
        if new_email is None:
            h.flash("Removed email address.")
        else:
            h.flash("Updated email address to '%s'." % new_email)
        return h.redirect_to('/')

    @authorize(BlueChipResident())
    def new(self):
        c.title = 'Register a New User'
        return render('/user/new.mako')

    @authorize(BlueChipResident())
    @validate(schema=NewUserSchema(), form='new')
    @authenticate_form
    def create(self):
        u = model.User(username=self.form_result['username'],
                       resident=self.form_result['resident'])

        if self.form_result['name']:
            u.name = self.form_result['name']
        else:
            u.name = self.form_result['username']

        if self.form_result['password'] is not None:
            u.password = self.form_result['password']

        meta.Session.add(u)
        meta.Session.commit()

        h.flash('Successfully created new user %s' % u.username)
        return h.redirect_to('/')

    def edit_card(self, id=None):
        
        if id is None:
            # first delete all other new cards to prevent collision
            cs = meta.Session.query(model.Card).filter(model.cards.c.serial == 0).all();
            for c1 in cs:
                 meta.Session.delete(c1);
            meta.Session.commit();
            n = model.Card()
            n.valid = 1;
            n.user = request.environ['user']
            meta.Session.add(n)
            meta.Session.commit()
            c.title = 'New card'
            c.card = n;
            return render('user/card.mako')
        else:
            n = meta.Session.query(model.Card).get(id)
            c.card = n;
            c.title = 'Edit card'
        return render('user/card.mako')

    @validate(schema=CardSchema(), form='edit_card')
    @authenticate_form
    def update_card(self, id):
        if id is None:
            abort(404)

        n = meta.Session.query(model.Card).get(id)
        n.description = self.form_result['description'];
        
        meta.Session.commit()

        h.flash('Card has been updated')
        return h.redirect_to('/user')

    def remove_card(self, id=None):
        if id is None:
            abort(404)
        n = meta.Session.query(model.Card).get(id)
        n.valid = 0
        n.serial = -1;
        meta.Session.commit();
        h.flash('Card has been removed from your account')
        return h.redirect_to('/user')
	
    def check_serial(self, id):
        raise ValueError(id)
        if id is None:
             abort(404);
        n = meta.Session.query(model.Card).get(id)
        return n.serial
