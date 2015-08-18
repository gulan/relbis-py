#!/usr/bin/env python2

# TODO
# ----
# virtual Integer relation
# n-ary operations
# grouping, display: 2-d blocks

"""
The relational model describes a relation as header and a body. Header
is a set of (name,type), where name is distinct.  The body is a set of
rows, where each row is a set (name,value). The names are distinct and
are the same as those in the header. The value is a single instance of
the type. (We do not permit NULLs in this pure model.)

The above description is in terms of sets, tuples and
constraints. There is no defined order to either rows or header tuple
comprising the header.

Relation:
    Header:
        Tuple (frozenset of attribute):
            attribute: (name,value)  # value is a Python type
    Body:
        TupleSet (frozenset of Tuple):
            Tuple (frozenset of attribute):
                attribute: (name,value)

relation.create(('x','y','z'),(int,int,int),[(1,2,3),(3,4,7),...])
"""

from decimal import Decimal
import display
from Tuple import Tuple
from TupleSet import TupleSet

class Header(Tuple):
    """Reuse Tuple code but distinguish the type."""
    pass

class RelationBase(object):

    """
    We permit ourselves to know that a relation has a header and a body.

      * do not iterate over attributes of a Tuple
      * do not directly iterate over rows of the TupleSet.    
    """
    
    @classmethod
    def create(cls,names,types,rows):
        header = Header(**dict(zip(names,types)))
        recs = list(Tuple(**dict(zip(names,r))) for r in rows)
        return cls(header,*recs)
        
    @classmethod
    def load(cls,path):
        # TBD: pass in fh, not path
        def read_data(fh):
            for line in fh:
                rec = line.strip()
                if not rec:             # blank line
                    continue
                if rec.startswith('#'): # comment
                    continue
                if rec.startswith('$'): # explict EOF for testing
                    break
                yield tuple(r.strip() for r in rec.split('|'))
                
        with open(path) as data:
            d = read_data(data)
            names = d.next()
            types = [eval(t) for t in d.next()] # security problem
            x = [zip(types,row) for row in d]
            rows = [[f(v)for (f,v) in row] for row in x]
            return cls.create(names,types,rows)

    @property
    def names(self): raise NotImplemented

    @property
    def count(self): return len(list(self))
    
    def __repr__(self):
        return "{klass}({header},{rows})".format(
            klass=self.__class__.__name__,
            header=repr(self.header),
            rows=map(repr,self))

    def __str__(self):
        g = list(row.to_pytuple() for row in self)
        return '\n'.join(display.display(g,self.names))

    def __iter__(self): raise NotImplemented

    def project(self,*names):
        """Keep only those columns in names"""
        if names:
            new_header = self.header.project(*names)
            new_body = self.body.project(*names)
            return self.__class__(new_header,*new_body)
        else:
            return self.__class__(Header()) # DUM
    
    def allbut(self,*names):
        """complement of 'project'"""
        ns = set(self.names) - set(names)
        return self.project(*ns)

    # def matching(self,other): pass
    # def not_matching(self,other): pass
    # def xunion(self,other): pass
    # def image(self,other): pass
    
    def restrict(self,predicate):
        """Discard all rows for which the predicate is false"""
        new_body = self.body.restrict(predicate)
        return self.__class__(self.header,*new_body)

    def cross(self,other):
        common = set(self.names) & set(other.names)
        assert not common, "column names are not disjoint"
        new_header = self.header | other.header
        # new_body = frozenset(x|y for (x,y) in self.pairs(other))
        new_body = self.body.cross(other)
        return self.__class__(new_header,*new_body)

    def join(self,other):
        new_header = self.header | other.header
        new_body = self.body.join(other)
        return self.__class__(new_header,*new_body)

    def extend(self,**kw): # kw: name -> type,(row -> value)
        """Add a new computed column for each name in kw.keys(). The
        value of the attribute is computed as a function on the row of
        that attribute. Because this is Python, we can provide any
        callable object for the 'function'."""
        types = dict((k,lambda _:v[0]) for (k,v) in kw.iteritems())
        cons = dict((k,v[1]) for (k,v) in kw.iteritems())
        new_header = self.header.extend(**types)
        new_body = self.body.extend(**cons)
        return self.__class__(new_header,*new_body)

    def union(self,other):
        if set(self.names) != set(other.names):
            raise TypeError, 'different headers on attempted set op'
        new_body = self.body | other.body
        return self.__class__(self.header,*new_body)

    def intersect(self,other):
        if set(self.names) != set(other.names):
            raise TypeError, 'different headers on attempted set op'
        new_body = self.body & other.body
        return self.__class__(self.header,*new_body)

    def difference(self,other):
        if set(self.names) != set(other.names):
            raise TypeError, 'different headers on attempted set op'
        new_body = self.body - other.body
        return self.__class__(self.header,*new_body)

    def rename(self,**kw):
        new_header = self.header.rename(**kw)
        new_body = self.body.rename(**kw)
        return self.__class__(new_header,*new_body)

    def __eq__(self,other):
        if self.header != other.header:
            raise TypeError, 'different headers on attempted set op'
        return self.body == other.body

    def __ne__(self,y):
        return not self == y

    def __gt__(self,other):
        if self.header != other.header:
            raise TypeError, 'different headers on attempted set op'
        return self.body > other.body

    # def __le__(self,y):
    #     return not self > y

    # def __lt__(self,y):
    #     if self.header != other.header:
    #         raise TypeError, 'different headers on attempted set op'
    #     return self < y

    def __ge__(self,y):
        return not self < y

    def sum(self,selector):
        return self.body.sum(selector)

    def ave(self,selector):
        return self.body.ave(selector)

    def min(self,selector):
        return self.body.min(selector)

    def max(self,selector):
        return self.body.max(selector)

    def all(self,selector):
        return self.body.all(selector)

    def any(self,selector):
        return self.body.any(selector)

class Relation(RelationBase):

    def __init__(self,header,*rows):
        self.header = header
        self.body = TupleSet(rows)
        
    @property
    def names(self): return self.header.names
    
    @property
    def types(self): return self.header.values
    
    @property
    def rows(self): return list(t.values for t in self)
    
    def __iter__(self):
        return iter(self.body)

DUM = Relation(Header())
DEE = Relation(Header(),Tuple())

def demo():
    pass

if __name__ == '__main__':
    demo()
