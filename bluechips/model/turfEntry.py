

class TurfEntry(object):
    def __init__(self, user=None, subject=None):
        self.user = user # pragma: nocover
        self.subject = subject # pragma: nocover
        
    def __repr__(self):
        return ('<Turf entry: %s bought %s at %s>' %
                (self.user, self.subject, self.entered_time)) # pragma: nocover

__all__ = ['TurfEntry']
