#!/usr/bin/env python

""" The rows of an relation db is a set comprised of Tuples. Each
Tuple is a set of name-value pairs, which are called attributes. Every
Tuple in a relation has the same attribute names (which are also the
same as the heading). Unlike Python tuples, the order of Tuple
attributes is insignificant: they form a set."""

class TupleBase(object):

    """Methods here are independent of the representation of the
    tuple. Any class that implements tuple may extend itself by
    inheriting this class.
    
    Methods that a subclass is expected to implement are documented
    here by stubs.
    
    The goal is to minimize the number of methods that depend on a
    particular implementation."""
    
    @classmethod
    def from_set(cls,content): raise NotImplemented

    @property
    def degree(self): raise NotImplemented

    @property
    def names(self):
        return tuple(sorted(n for (n,_) in self))

    @property
    def values(self):
        return tuple(v for (_,v) in (sorted(self)))
        
    def to_pytuple(self):
        return tuple(getattr(self,name) for name in self.names)

    def __iter__(self):
        """Generates a sequence of Python tuples, each of the form (name,value)."""
        raise NotImplemented

    def __repr__(self):
        t = '{name}={value}'
        body = ','.join(t.format(name=x,value=repr(y)) for (x,y) in sorted(self))
        return "{klass}({body})".format(klass=self.__class__.__name__,body=body)

    def __getattr__(self,name):
        assert not name.startswith('_'), 'attributes names may not start with _'
        for n,value in self:
            if n == name:
                return value
        raise AttributeError, '{} is not an attribute'.format(name)

    def __eq__(self,other): raise NotImplemented
    def __gt__(self,other): raise NotImplemented
    def __lt__(self,other): raise NotImplemented
    def __ne__(self,other): return not self == other
    def __ge__(self,other): return not self < other
    def __le__(self,other): return not self > other

    def __hash__(self):
        # needed because we make sets of Tuples
        raise NotImplemented

    def project(self,*names):
        extra = set(names) - set(self.names)
        if extra:
            msg = 'unknown attributes: %s' % ','.join(extra)
            raise AttributeError, msg
        d = dict((n,v) for n,v in self if n in names)
        return self.__class__(**d)
        
    def __or__(self,other): raise NotImplemented

    def rename(self,**kw):
        extra = set(kw.keys()) - set(self.names)
        if extra:
            msg = 'unknown attributes: %s' % ','.join(extra)
            raise AttributeError, msg
        if len(set(kw.values())) < len(kw.values()):
            raise TypeError, 'name collision %s' % (kw,)
        new_content = frozenset((kw.get(n,n),v) for (n,v) in self)
        names = set(n for (n,_) in new_content)
        if len(names) != len(new_content):
            raise TypeError,'common attribute names have different values'
        return self.__class__.from_set(new_content)

    def extend(self,**kw):
        extra = set(kw.keys()) & set(self.names)
        if extra:
            msg = 'duplicate attributes: %s' % ','.join(extra)
            raise TypeError, msg
        new_content = set(self) # unfreeze
        for k,f in kw.items():
            x = (k,f(self))
            new_content.add(x)
        return self.__class__.from_set(frozenset(new_content))

    def to_pytuple(self):
        return tuple(getattr(self,name) for name in self.names)

class Tuple(TupleBase):
    
    def __init__(self,**kw):
        keys = kw.keys()
        assert len(keys) == len(set(keys)), "duplicate attribute name"
        del keys
        self.content = frozenset(kw.iteritems())

    @classmethod
    def from_set(cls,content):
        t = cls()
        t.content = content
        return t

    @property
    def degree(self): return len(self.content)
    def __iter__(self): return iter(self.content)
    def __eq__(self,other): return self.content == other.content
    def __gt__(self,other): return self.content > other.content
    def __lt__(self,other): return self.content < other.content
    def __hash__(self): return hash(self.content)

    def __or__(self,other):
        new_content = self.content | other.content
        names = set(n for (n,_) in new_content)
        if len(names) != len(new_content):
            raise TypeError,'common attribute names have different values'
        return self.__class__.from_set(new_content)

def demo():
    t1 = Tuple(sno='S1',sname='Smith',status=20,city='London')
    print t1.city
    print t1.degree
    print t1.names
    print t1.values
    print t1.to_pytuple()
    print t1.rename(city='town',sname='customer')
    print t1.extend(since=lambda r: '1980') # function on tuple. here constant function
    print t1.project('sname','city')

if __name__ == '__main__':
    demo()
