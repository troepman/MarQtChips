

class TurfEntry(object):
    def __init__(self, card=None, subject=None):
        self.card = card # pragma: nocover
        self.subject = subject # pragma: nocover
        
    def __repr__(self):
        return ('<Turf entry: %s bought %s at %s>' %
                (self.card, self.subject, self.entered_time)) # pragma: nocover

__all__ = ['TurfEntry']
