

class Card(object):
    def __init__(self, user=None, serial=0, description=None):
        self.serial = serial # pragma: nocover
        self.user = user # pragma: nocover
        self.description = description # pragma: nocover
        
    def __repr__(self):
        return ('<Card: card(%s) is of: %s described as: %s>' %
                (self.serial, self.user, self.description)) # pragma: nocover

__all__ = ['Card']
