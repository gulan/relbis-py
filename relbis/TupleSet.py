#!/usr/bin/env python

import display

class TupleSet(frozenset):

    """Set operations over a set of uniform tuples"""

    @property
    def names(self):
        if self:
            return list(self)[0].names
        else:
            return []

    @property
    def values(self):
        if self:
            return list(self)[0].values
        else:
            return []
    
    def X__str__(self):
        g = list(row.to_pytuple() for row in self)
        return '\n'.join(display.display(g,self.names))

    def project(self,*names):
        return self.__class__(row.project(*names) for row in self)
    
    def allbut(self,*names):
        # complement of 'project'
        ns = set(self.names) - set(names)
        return self.project(*ns)

    # def matching(self,other): pass
    # def not_matching(self,other): pass
    # def xunion(self,other): pass
    # def image(self,other): pass
    
    def restrict(self,predicate):
        return self.__class__(row for row in self if predicate(row))

    def pairs(self,other): # private
        return ((x,y) for x in self for y in other)

    def cross(self,other):
        # Unlike the mathmatical cartesian product, we do a union of
        # the the pairs. The tuple class will complain about any name
        # collisions.
        return self.__class__(x|y for (x,y) in self.pairs(other))

    def join(self,other):
        common = set(self.names) & set(other.names)
        def p(left,right):
            return all(getattr(left,n) == getattr(right,n) for n in common)
        new = (x|y for (x,y) in self.pairs(other) if p(x,y))
        return self.__class__(new)

    def extend(self,**kw):
        return self.__class__(row.extend(**kw) for row in self)

    def rename(self,**kw):
        return self.__class__(row.rename(**kw) for row in self)

    def sum(self,selector):
        return sum(selector(r) for r in self)

    def ave(self,selector):
        s = sum(selector(r) for r in self)
        return s/len(self)

    def min(self,selector):
        return min(selector(r) for r in self)

    def max(self,selector):
        return max(selector(r) for r in self)

    def all(self,selector):
        return all(selector(r) for r in self)

    def any(self,selector):
        return any(selector(r) for r in self)
