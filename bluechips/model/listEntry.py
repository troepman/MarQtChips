

class ListEntry(object):
    def __init__(self, subject=None, creater=None, checker=None):
        self.creater = creater # pragma: nocover
        self.subject = subject # pragma: nocover
        self.checker = checker # pragma: nocover
        
    def __repr__(self):
        return ('<List entry %s created by: %s at %s; checked by %s at %s>' %
                (self.subject, self.creater, self.createdTime, self.checker, self.checkedTime)) # pragma: nocover

__all__ = ['ListEntry']
