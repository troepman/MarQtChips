"""
Calculate the total state of the books
"""

from bluechips import model
from bluechips.model import meta

from bluechips.model.types import Currency

import sqlalchemy

class DirtyBooks(Exception):
    """
    If the books don't work out, raise this
    """
    pass

def debts():
    # In this scheme, negative numbers represent money the house owes
    # the user, and positive numbers represent money the user owes the
    # house
    users = meta.Session.query(model.User)
    
    debts_dict = dict((u, Currency(0)) for u in users)
    
    # First, credit everyone for expenditures they've made
    total_expenditures = meta.Session.query(model.Expenditure).all()
    for expenditure in total_expenditures:
        debts_dict[expenditure.spender] -= expenditure.amount
    
    # Next, debit everyone for expenditures that they have an
    # investment in (i.e. splits)
    
    total_splits = meta.Session.query(model.Split).all()    
    for split in total_splits:
        debts_dict[split.user] +=  split.share
    
    # Finally, move transfers around appropriately
    #
    # To keep this from getting to be expensive, have SQL sum up
    # transfers for us
    
    transfers = meta.Session.query(model.Transfer).all();
    
    for transfer in transfers:
        debts_dict[transfer.debtor] -= transfer.amount
        debts_dict[transfer.creditor] += transfer.amount
    
    return debts_dict

def settle(debts_dict):
    # This algorithm has been shamelessly stolen from Nelson Elhage's
    # <nelhage@mit.edu> implementation for our 2008 summer apartment.
    
    debts_list = [dict(who=user, amount=amount) for user, amount in \
                      debts_dict.iteritems()]
    #debts_list.sort(reverse=True, key=(lambda x: abs(x['amount'])))
    
    owes_list = [debt for debt in debts_list if debt['amount'] > 0]
    owed_list = [debt for debt in debts_list if debt['amount'] < 0]
    
    settle_list = []
    
    while len(owes_list) > 0 and len(owed_list) > 0:
        owes_list.sort(reverse=True, key=(lambda x: abs(x['amount'])))
        owed_list.sort(reverse=True, key=(lambda x: abs(x['amount'])))

        owes = owes_list[0]
        owed = owed_list[0]
        
        sum = owes['amount'] + owed['amount']
        if sum == 0:
            # Perfect balance!
            owes_list.pop(0)
            owed_list.pop(0)
            val = owes['amount']
        elif sum > 0:
            # person in owes still owes money
            owes['amount'] += owed['amount']
            owed_list.pop(0)
            val = -owed['amount']
        else:
            # person in owed is owed more than owes has to give
            owed['amount'] += owes['amount']
            owes_list.pop(0)
            val = owes['amount']
        
        settle_list.append((owes['who'], owed['who'], val))
    
    if len(owes_list) > 0:
        raise DirtyBooks, ("People still owe money", owes_list)
    if len(owed_list) > 0:
        raise DirtyBooks, ("People are still owed money", owed_list)
    
    return settle_list

__all__ = ['debts', 'settle']
