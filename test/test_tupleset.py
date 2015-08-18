#! /usr/bin/env python

import unittest

import sys
sys.path.insert(0,'../')
from relbis.TupleSet import TupleSet
from relbis.Tuple import Tuple

t = TupleSet([
    Tuple(i=0,x=2,y=1),
    Tuple(i=1,x=4,y=2),
    Tuple(i=2,x=6,y=3),
    Tuple(i=3,x=8,y=1),
    Tuple(i=4,x=10,y=2),
    Tuple(i=5,x=12,y=3),
    Tuple(i=6,x=14,y=1)])

xy = TupleSet([
    Tuple(x=2,y=1),
    Tuple(x=4,y=2),
    Tuple(x=6,y=3),
    Tuple(x=8,y=1),
    Tuple(x=10,y=2),
    Tuple(x=12,y=3),
    Tuple(x=14,y=1)])

x = TupleSet([
    Tuple(x=2),
    Tuple(x=4),
    Tuple(x=6),
    Tuple(x=8),
    Tuple(x=10),
    Tuple(x=12),
    Tuple(x=14)])

y = TupleSet([
    Tuple(y=1),
    Tuple(y=2),
    Tuple(y=3)])

ch = TupleSet([
    Tuple(a='a'),
    Tuple(a='b'),
    Tuple(a='c')])

zh = TupleSet([
    Tuple(a='c'),
    Tuple(a='d'),
    Tuple(a='e')])

q = TupleSet([
    Tuple(i=0,c='a'),
    Tuple(i=1,c='b'),
    Tuple(i=2,c='c'),
    Tuple(i=3,c='d'),
    Tuple(i=4,c='e')])

w = TupleSet([
    Tuple(i=0,d='b'),
    Tuple(i=1,d='c'),
    Tuple(i=2,d='d'),
    Tuple(i=3,d='e'),
    Tuple(i=4,d='f')])

class test_tupleset(unittest.TestCase):
    
    def test_set_ops(self):
        e = TupleSet([])
        ab = TupleSet([Tuple(a='b')])
        ac = TupleSet([Tuple(a='c')])
        abc = TupleSet([Tuple(a='b'),Tuple(a='c')])

        self.failUnless(e|e == e)
        self.failUnless(e|x == x == x|e) # correct?
        self.failUnless(x|x == x)
        self.failUnless(ab|ac == ac|ab)
        self.failUnless(ab|abc == abc)

    def test_project(self):
        self.failUnless(t.project('i','x','y') == t)
        self.failUnless(t.project('x') == x)
        self.failUnless(t.project('x','y') == xy)
        self.failUnless(t.project() == TupleSet([Tuple()]))

    def test_extend(self):
        r = TupleSet([
            Tuple(y=3,z=30),
            Tuple(y=1,z=10),
            Tuple(y=2,z=20)])

        self.failUnless(y.extend(z=lambda tup: tup.y*10) == r)

    def test_rename(self):
        r = TupleSet([Tuple(j=0,x=2,y=1),
                      Tuple(j=3,x=8,y=1),
                      Tuple(j=6,x=14,y=1),
                      Tuple(j=5,x=12,y=3),
                      Tuple(j=2,x=6,y=3),
                      Tuple(j=4,x=10,y=2),
                      Tuple(j=1,x=4,y=2)])

        self.failUnless(t.rename(i='j') == r)
        # for i in t.rename(i='I',x='X',y='Y'): print i

    def test_allbut(self):
        self.failUnless(t.allbut('i') == xy)
        self.failUnless(t.allbut('i','y') == x)
        self.failUnless(t.allbut('i','x','y') == t.project())

    def test_restrict(self):
        def even(n): return n % 2 == 0
        def odd(n): return not even(n)
        # print t.restrict(lambda row: even(row.i))
        # print t.restrict(lambda row: even(row.i) and row.x > 8)
        self.failUnless(t.restrict(lambda row: False) == TupleSet([]))
        self.failUnless(t.restrict(lambda row: True) == t)

    def test_cross(self):
        self.failUnless(y.cross(ch) == ch.cross(y))

    def test_join(self):
        r = TupleSet([
            Tuple(c='a',d='b'),
            Tuple(c='b',d='c'),
            Tuple(c='c',d='d'),
            Tuple(c='d',d='e'),
            Tuple(c='e',d='f')])
        self.failUnless(q.join(w).allbut('i') == r)

        
if __name__ == '__main__':
    unittest.main()
