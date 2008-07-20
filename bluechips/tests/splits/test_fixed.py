from unittest import TestCase
from bluechips.tests import *
from bluechips import model
from bluechips.model import meta
from bluechips.model.types import Currency
from decimal import Decimal

class TestSplitFixed(TestCase):
    def test_simpleSplit(self):
        """
        Test simply splitting a $100 expenditure amongst 4 people
        """
        createUsers(4)
        
        e = model.Expenditure()
        e.spender = meta.Session.query(model.User).first()
        e.amount = Currency("100.00")
        meta.Session.save(e)
        e.even_split()
        meta.Session.commit()
        
        for s in meta.Session.query(model.Split).\
                filter(model.Split.expenditure==e):
            self.assertEqual(s.share, Currency("25.00"))
        
        deleteExpenditures()
        deleteUsers()
    
    def test_uneven(self):
        """
        Test that expenditures can be split non-evenly
        """
        createUsers(2)
        
        users = meta.Session.query(model.User).all()
        
        e = model.Expenditure()
        e.spender = users[0]
        e.amount = Currency("100.00")
        meta.Session.save(e)
        
        split_dict = {users[0]: Decimal("20"),
                      users[1]: Decimal("80")}
        
        amount_dict = {users[0]: Currency("20"),
                       users[1]: Currency("80")}
        
        e.split(split_dict)
        meta.Session.commit()
        
        for s in meta.Session.query(model.Split):
            self.assertEqual(s.share, amount_dict[s.user])
        
        deleteExpenditures()
        deleteUsers()
    
    def test_unevenBadTotal(self):
        """
        Test that transactions get split up properly when the uneven
        split shares don't add to 100%
        """
        createUsers(2)
        
        users = meta.Session.query(model.User).all()
        
        e = model.Expenditure()
        e.spender = users[0]
        e.amount = Currency("100.00")
        meta.Session.save(e)
        
        split_dict = {users[0]: Decimal(10),
                      users[1]: Decimal(15)}
        
        amount_dict = {users[0]: Currency("40"),
                       users[1]: Currency("60")}
        
        e.split(split_dict)
        meta.Session.commit()
        
        for s in meta.Session.query(model.Split):
            self.assertEqual(s.share, amount_dict[s.user])
        
        deleteExpenditures()
        deleteUsers()
